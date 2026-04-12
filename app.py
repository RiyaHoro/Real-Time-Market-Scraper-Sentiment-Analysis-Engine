import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scraper import scrape_data
from sentiment import analyze_sentiment
from db import connect_db

plt.style.use("ggplot")

st.set_page_config(page_title="MarketLens", layout="wide")

st.title("MarketLens — Real-Time Market Sentiment Engine")

url = st.text_input("Enter Product Page URL")


def decision(price, sentiment, rating):

    score = (sentiment * 0.7) + ((rating / 5) * 0.3)

    if score > 0.5:
        return "BUY RECOMMENDED"
    elif score > 0.2:
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
    sentiment = (sentiment + 1) / 2

    recommendation = decision(price, sentiment, rating)

    save_result(name, price, rating, sentiment, recommendation)

    st.subheader(f"Product: {name}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Price", f"{currency}{price}")
    col2.metric("Rating", rating)
    col3.metric("Sentiment Score", round(sentiment, 2))
    col4.metric("Recommendation", recommendation)

    confidence = abs(sentiment - 0.5) * 2

    st.progress(min(confidence, 1.0))
    st.write("Confidence Score:", round(confidence, 2))


    db = connect_db()

    df = pd.read_sql("SELECT * FROM product_analysis", db)

    df["analysis_time"] = pd.to_datetime(df["analysis_time"])

    df_recent = df.sort_values("analysis_time").tail(10)

    st.subheader("Market Analysis")

    colA, colB = st.columns(2)

    # Sentiment trend
    with colA:

        fig1, ax1 = plt.subplots()

        ax1.plot(df_recent["analysis_time"], df_recent["sentiment_score"], marker="o")

        ax1.set_title("Sentiment Trend Over Time")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Sentiment Score")

        plt.xticks(rotation=45)

        st.pyplot(fig1)

    # Price vs sentiment
    with colB:

        fig2, ax2 = plt.subplots()

        ax2.scatter(df_recent["price"], df_recent["sentiment_score"])

        ax2.set_title("Price vs Sentiment")
        ax2.set_xlabel("Price")
        ax2.set_ylabel("Sentiment Score")

        st.pyplot(fig2)