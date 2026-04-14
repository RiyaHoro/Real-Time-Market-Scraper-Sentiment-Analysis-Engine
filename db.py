import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("mysql_user"),
        password=os.getenv("mysql_password"),
        database="market_sentiment"
    )