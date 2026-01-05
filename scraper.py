import requests
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def get_booking_price(html: str):
    match = re.search(r'"grossPrice":\{"value":([0-9.]+)', html)
    return float(match.group(1)) if match else None


def get_hotels_price(html: str):
    # Hotels.com often embeds price like: "leadAmount":123
    match = re.search(r'"leadAmount":\s*([0-9.]+)', html)
    return float(match.group(1)) if match else None


def get_expedia_price(html: str):
    # Expedia embeds "displayPrice":{"amount":123}
    match = re.search(r'"amount":\s*([0-9.]+)', html)
    return float(match.group(1)) if match else None


def get_price(url: str) -> float | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return None

        html = r.text.lower()

        if "booking.com" in url:
            return get_booking_price(html)

        if "hotels.com" in url:
            return get_hotels_price(html)

        if "expedia.com" in url:
            return get_expedia_price(html)

        return None

    except Exception:
        return None
