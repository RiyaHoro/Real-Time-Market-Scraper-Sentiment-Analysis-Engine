import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scraper.scraper import scrape_data
from sentiment.sentiment import analyze_sentiment
from database.db import connect_db


st.set_page_config(page_title="MarketLens", layout="wide")

st.title("Real-Time Market Sentiment Engine")

url = st.text_input("Enter Product Page URL")


def decision(price, sentiment, rating):

    score = (sentiment * 0.6) + ((rating / 5) * 0.4)

    if score > 0.6:
        return "BUY RECOMMENDED"
    elif score > 0.3:
        return "HOLD"
    else:
        return "DO NOT BUY"


def save_result(name, price, rating, sentiment, decision):

    db = connect_db()
    cursor = db.cursor()

    query = """
    INSERT INTO product_analysis
    (product_name, price, rating, sentiment_score, decision)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (name, price, rating, sentiment, decision))

    db.commit()


if st.button("Analyze Product"):

    name, currency, price, rating, reviews = scrape_data(url)

    sentiment = analyze_sentiment(reviews)

    recommendation = decision(price, sentiment, rating)

    save_result(name, price, rating, sentiment, recommendation)

    st.subheader("Product Analysis")

    st.write(f"**Product:** {name}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Price", f"{currency}{price}")
    col2.metric("Rating", round(rating, 1))
    col3.metric("Sentiment Score", round(sentiment, 2))
    col4.metric("Recommendation", recommendation)

    st.success(recommendation)

    db = connect_db()

    df = pd.read_sql("SELECT * FROM product_analysis", db)

    df["analysis_time"] = pd.to_datetime(df["analysis_time"])

    df_product = df[df["product_name"].str.contains(name, case=False, na=False)]

    df_product = df_product.sort_values("analysis_time")

    st.subheader("Market Analysis")

    colA, colB = st.columns(2)

    # GRAPH 1: Sentiment Trend
    with colA:

        fig1, ax1 = plt.subplots()

        ax1.plot(df_product["analysis_time"], df_product["sentiment_score"], marker="o")

        ax1.set_title("Sentiment Trend Over Time")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Sentiment Score")
        plt.style.use("ggplot")

        plt.xticks(rotation=45)

        st.pyplot(fig1)

    # GRAPH 2: Price vs Sentiment
    with colB:

        fig2, ax2 = plt.subplots()

        ax2.scatter(df_product["price"], df_product["sentiment_score"])

        ax2.set_title("Price vs Sentiment")
        ax2.set_xlabel("Price")
        ax2.set_ylabel("Sentiment Score")
        plt.style.use("ggplot")
        st.pyplot(fig2)