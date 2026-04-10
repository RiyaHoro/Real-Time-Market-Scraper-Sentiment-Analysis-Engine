import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scraper.scraper import scrape_data
from sentiment.sentiment import analyze_sentiment
from database.db import connect_db

st.set_page_config(page_title="MarketLens", layout="wide")

st.title("MarketLens — Market Sentiment Engine")

url = st.text_input("Enter Product URL")

def decision(price, sentiment):

    if sentiment > 0.2 and price < 50:
        return "BUY"

    return "NOT BUY"


def save_result(price, sentiment, decision):

    db = connect_db()
    cursor = db.cursor()

    query = """
    INSERT INTO product_analysis
    (product_name, price, sentiment_score, decision)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(query, ("Product", price, sentiment, decision))

    db.commit()


if st.button("Analyze Product"):

    price, reviews = scrape_data(url)

    sentiment = analyze_sentiment(reviews)

    recommendation = decision(price, sentiment)

    save_result(price, sentiment, recommendation)

    st.subheader("Analysis Result")

    col1, col2, col3 = st.columns(3)

    col1.metric("Price", price)
    col2.metric("Sentiment", round(sentiment,2))
    col3.metric("Recommendation", recommendation)

    db = connect_db()

    df = pd.read_sql("SELECT * FROM product_analysis", db)

    fig, ax = plt.subplots()

    ax.plot(df["analysis_time"], df["sentiment_score"])

    ax.set_title("Sentiment Trend")

    st.pyplot(fig)