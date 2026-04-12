import subprocess
from scraper import scrape_product
import mysql.connector

price, reviews = scrape_product()

review_string = "|".join(reviews)

result = subprocess.run(
    ["Rscript", "../r/sentiment.R", review_string],
    capture_output=True,
    text=True
)

sentiment_score = float(result.stdout.strip())

print("Sentiment:", sentiment_score)

# save to database

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

cursor.execute(query, ("Book", price.replace("£",""), sentiment_score))

conn.commit()

print("Data stored successfully")