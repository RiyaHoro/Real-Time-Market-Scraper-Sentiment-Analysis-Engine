import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def scrape_product(url):

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.select_one(".title")

    price_tag = soup.select_one(".price")

    review_tags = soup.select(".review-text")

    title = title_tag.text.strip() if title_tag else "Unknown Product"

    price = price_tag.text.strip().replace("$","") if price_tag else "0"

    reviews = [r.text.strip() for r in review_tags]

    if not reviews:
        reviews = ["Average product", "Decent quality"]

    return title, price, reviews