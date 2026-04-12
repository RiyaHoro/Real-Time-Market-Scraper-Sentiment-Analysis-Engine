create database market_engine;
use market_engine;
CREATE TABLE product_data (
id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(200),
price FLOAT,
sentiment FLOAT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);