tracked = []


def add_hotel(chat_id, url, price):
    tracked.append({
        "chat_id": chat_id,
        "url": url,
        "last_price": price,
    })


def get_by_chat(chat_id):
    return [h for h in tracked if h["chat_id"] == chat_id]


def get_all():
    return tracked


def update_price(item, new_price):
    item["last_price"] = new_price
