import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scraper.scraper import scrape_data
from sentiment.sentiment import analyze_sentiment
from database.db import connect_db


st.set_page_config(page_title="MarketLens", layout="wide")

st.title("MarketLens — Market Sentiment Engine")

url = st.text_input("Enter Product URL")


def decision(price, sentiment, rating):

    score = (sentiment * 0.6) + ((rating / 5) * 0.4)

    if score > 0.6:
        return "BUY"
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

    name, price, rating, reviews = scrape_data(url)

    sentiment = analyze_sentiment(reviews)

    recommendation = decision(price, sentiment, rating)

    save_result(name, price, rating, sentiment, recommendation)

    st.subheader("Analysis Result")

    st.write("###", name)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Price", price)
    col2.metric("Rating", round(rating,1))
    col3.metric("Sentiment", round(sentiment,2))
    col4.metric("Recommendation", recommendation)

    db = connect_db()

    df = pd.read_sql("SELECT * FROM product_analysis", db)

    st.subheader("Sentiment Trend")

    fig, ax = plt.subplots()

    ax.plot(df["analysis_time"], df["sentiment_score"], marker="o")

    ax.set_xlabel("Time")
    ax.set_ylabel("Sentiment Score")
    ax.set_title("Sentiment Trend")

    st.pyplot(fig)