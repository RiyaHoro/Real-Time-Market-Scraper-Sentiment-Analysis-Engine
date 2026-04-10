import requests
from bs4 import BeautifulSoup

def scrape_data(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    price_tag = soup.find("p", class_="price_color")

    if price_tag:
        price = float(price_tag.text.replace("£",""))
    else:
        price = 25.0

    reviews = [
        "Amazing product very useful",
        "Pretty good overall",
        "Quality is great",
        "Not bad but could improve"
    ]

    return price, reviews