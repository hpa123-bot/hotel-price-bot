import requests
from bs4 import BeautifulSoup

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    # ⚠️ THIS WILL BE SITE-SPECIFIC
    price_tag = soup.select_one(".price")

    if not price_tag:
        return None

    price_text = price_tag.get_text(strip=True)
    price = float(price_text.replace("$", "").replace(",", ""))
    return price