CREATE DATABASE market_sentiment;

USE market_sentiment;

CREATE TABLE product_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    price FLOAT,
    sentiment_score FLOAT,
    decision VARCHAR(20),
    analysis_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);