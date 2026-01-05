import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_price(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    price_tag = soup.find("span", class_=re.compile("price"))
    if not price_tag:
        return None

    price = re.sub(r"[^\d]", "", price_tag.text)
    return float(price)