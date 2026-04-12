import streamlit as st
import pandas as pd
import mysql.connector
from python.scraper import scrape_product
from python.sentiment_runner import get_sentiment
import matplotlib.pyplot as plt

st.title("Real-Time Market Sentiment Engine")

url = st.text_input("Enter Product Page URL")

if st.button("Analyze Product"):

    title, price, reviews = scrape_product(url)

    sentiment = get_sentiment(reviews)

    clean_price = float(price.replace("₹","").replace(",","").replace("$",""))

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="market_engine"
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO product_data(product_name,price,sentiment)
    VALUES (%s,%s,%s)
    """

    cursor.execute(query,(title,clean_price,sentiment))

    conn.commit()

    st.subheader("Product Analysis")

    st.write("Product:",title)
    st.write("Price:",clean_price)
    st.write("Sentiment Score:",sentiment)

    if sentiment > 0.2:
        st.success("BUY RECOMMENDED")
    else:
        st.error("NOT RECOMMENDED")

    df = pd.read_sql("SELECT * FROM product_data",conn)

    st.subheader("Price Trend")

    plt.figure()

    plt.plot(df["created_at"],df["price"],marker="o")

    st.pyplot(plt)


    st.subheader("Sentiment Trend")

    plt.figure()

    plt.plot(df["created_at"],df["sentiment"],marker="o")

    st.pyplot(plt)     