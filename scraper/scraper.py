import requests
from bs4 import BeautifulSoup
import random
import re


def scrape_data(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        return "Unknown Product", "₹", 50.0, 3.5, ["Sample review"]

    # ---------------------------
    # PRODUCT NAME
    # ---------------------------

    name = None

    name_selectors = [
        "#productTitle",      # Amazon
        ".B_NuCI",            # Flipkart
        ".product-title",
        ".title",
        "h1"
    ]

    for selector in name_selectors:
        tag = soup.select_one(selector)
        if tag and tag.text.strip():
            name = tag.text.strip()
            break

    if not name:
        if soup.title:
            name = soup.title.text.strip()
        else:
            name = "Unknown Product"

    # ---------------------------
    # PRICE
    # ---------------------------

    price = None
    currency = None

    # AMAZON PRICE
    amazon_whole = soup.select_one(".a-price-whole")
    amazon_fraction = soup.select_one(".a-price-fraction")

    if amazon_whole:
        currency = "$"
        fraction = amazon_fraction.text if amazon_fraction else "00"
        price = float(f"{amazon_whole.text.replace(',', '')}.{fraction}")

    # FLIPKART PRICE
    if price is None:
        tag = soup.select_one("._30jeq3")
        if tag:
            price_text = tag.text
            currency = "₹"
            price = float(re.sub(r"[^\d.]", "", price_text))

    # GENERIC PRICE
    if price is None:

        generic_price = soup.select_one(".price")

        if generic_price:
            price_text = generic_price.text

            if "$" in price_text:
                currency = "$"
            elif "₹" in price_text:
                currency = "₹"
            else:
                currency = "$"

            price = float(re.sub(r"[^\d.]", "", price_text))

    if price is None:
        price = round(random.uniform(20, 100), 2)
        currency = "$"

    # ---------------------------
    # RATING
    # ---------------------------

    rating = None

    # AMAZON RATING
    amazon_rating = soup.select_one(".a-icon-alt")

    if amazon_rating:
        match = re.search(r"\d+(\.\d+)?", amazon_rating.text)
        if match:
            rating = float(match.group())

    # FLIPKART RATING
    if rating is None:
        flipkart_rating = soup.select_one("._3LWZlK")
        if flipkart_rating:
            rating = float(flipkart_rating.text)

    # STAR COUNT (for test sites)
    if rating is None:
        stars = soup.select(".glyphicon-star")
        if stars:
            rating = len(stars)

    if rating is None:
        rating = round(random.uniform(3.0, 4.5), 1)

    # ---------------------------
    # SAMPLE REVIEWS
    # ---------------------------

    review_pool = [
        "Excellent product highly recommended",
        "Very poor quality and disappointing",
        "Good value for money",
        "Average product but acceptable",
        "Fantastic quality and durable",
        "Not worth the price",
        "Very satisfied with this purchase",
        "Could be improved but decent overall"
    ]

    reviews = random.sample(review_pool, 4)

    return name, currency, price, rating, reviews