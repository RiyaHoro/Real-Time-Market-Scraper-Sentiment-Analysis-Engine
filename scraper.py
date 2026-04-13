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



# FLIPKART SCRAPER

def scrape_flipkart(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # PRODUCT NAME
    name = "Flipkart Product"
    name_tag = soup.select_one("h1.v1zwn21k")

    if name_tag:
        name = name_tag.text.strip()

    # PRICE
    currency = "₹"
    price = 0

    price_tag = soup.select_one("div._30jeq3, div.Nx9bqj, div._16Jk6d")

    if price_tag:
        price_text = re.sub(r"[^\d]", "", price_tag.text)

        try:
            price = float(price_text)
        except:
            price = 0

    # RATING
    rating = 0
    rating_tag = soup.select_one("div._3LWZlK")

    if rating_tag:
        try:
            rating = float(rating_tag.text.strip())
        except:
            rating = 0

    # REVIEWS
    reviews = []

    review_tags = soup.select("div.t-ZTKy div")

    for tag in review_tags[:6]:
        text = tag.text.strip()

        if len(text) > 20:
            reviews.append(text)

    if not reviews:
        reviews = ["No reviews found"]

    return name, currency, price, rating, reviews

# TEST SITE SCRAPER


def scrape_testsite(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # PRODUCT NAME
    name = "Test Product"

    name_tag = soup.select_one(".card-title")

    if name_tag:
        name = name_tag.text.strip()

    # PRICE
    currency = "$"
    price = 0

    price_tag = soup.select_one("h4.price")

    if price_tag:
        price_text = re.sub(r"[^\d.]", "", price_tag.text)

        try:
            price = float(price_text)
        except:
            price = 0

    # RATING
    rating = 0

    stars = soup.select(".ws-icon-star")

    if stars:
        rating = len(stars)

    # REVIEWS 
    reviews = []
    review_count = 0

    review_tag = soup.select_one('[itemprop="reviewCount"]')

    if review_tag:
        review_count = int(review_tag.text.strip())

    return name, currency, price, rating, reviews


# GENERIC SCRAPER


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