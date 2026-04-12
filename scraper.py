import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_data(url):

    if "flipkart" in url:
        return scrape_flipkart(url)

    elif "webscraper.io" in url:
        return scrape_testsite(url)

    else:
        return scrape_generic(url)


# -----------------------------
# FLIPKART SCRAPER
# -----------------------------

def scrape_flipkart(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # PRODUCT NAME
    name = "Flipkart Product"
    name_tag = soup.select_one(".B_NuCI")

    if name_tag:
        name = name_tag.text.strip()

    # PRICE
    currency = "₹"
    price = 0

    price_tag = soup.select_one("._30jeq3, .Nx9bqj")

    if price_tag:
        price_text = re.sub(r"[^\d]", "", price_tag.text)

        try:
            price = float(price_text)
        except:
            price = 0

    # RATING
    rating = 0

    rating_tag = soup.select_one("._3LWZlK")

    if rating_tag:
        try:
            rating = float(rating_tag.text.strip())
        except:
            rating = 0

    # TEXT FOR SENTIMENT
    reviews = []

    for tag in soup.select("._1mXcCf, p")[:6]:

        text = tag.text.strip()

        if len(text) > 30:
            reviews.append(text)

    if not reviews:
        reviews = ["Product description available but limited sentiment data"]

    return name, currency, price, rating, reviews


# -----------------------------
# TEST SITE SCRAPER
# -----------------------------

def scrape_testsite(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # -----------------
    # PRODUCT NAME
    # -----------------

    name = "Test Product"

    name_tag = soup.select_one(".card-title")

    if name_tag:
        name = name_tag.text.strip()

    # -----------------
    # PRICE
    # -----------------

    currency = "$"
    price = 0

    price_tag = soup.select_one(".price")

    if price_tag:
        price_text = re.sub(r"[^\d.]", "", price_tag.text)

        try:
            price = float(price_text)
        except:
            price = 0

    # -----------------
    # RATING
    # -----------------

    rating = 0

    review_tag = soup.select_one('[itemprop="reviewCount"]')

    if review_tag:
        try:
            reviews_count = int(review_tag.text.strip())

            # simple approximation: convert review count to rating
            rating = min(5, round(reviews_count / 2))

        except:
            rating = 0

    # -----------------
    # DESCRIPTION
    # -----------------

    desc_tag = soup.select_one(".description")

    reviews = []

    if desc_tag:
        reviews.append(desc_tag.text.strip())

    if not reviews:
        reviews = ["Average product"]

    return name, currency, price, rating, reviews
def scrape_generic(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.title.text.strip() if soup.title else "Unknown Product"

    currency = "$"
    price = 0
    rating = 0

    reviews = []

    for tag in soup.select("p")[:6]:

        text = tag.text.strip()

        if len(text) > 30:
            reviews.append(text)

    if not reviews:
        reviews = ["Limited product description available"]

    return name, currency, price, rating, reviews