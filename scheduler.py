from db import cursor, conn
from scraper import get_price

async def check_prices(app):
    cursor.execute(
        "SELECT rowid, chat_id, hotel_name, url, target_price, last_price FROM tracked_hotels"
    )
    rows = cursor.fetchall()

    for rowid, chat_id, name, url, target, last in rows:
        price = get_price(url)
        if not price:
            continue

        if last and price < last:
            await app.bot.send_message(
                chat_id,
                f"📉 Price Drop!\n{name}\nOld: ${last}\nNew: ${price}"
            )

        if price <= target:
            await app.bot.send_message(
                chat_id,
                f"🎉 TARGET HIT!\n{name} is now ${price}"
            )

        cursor.execute(
            "UPDATE tracked_hotels SET last_price=? WHERE rowid=?",
            (price, rowid)
        )
        conn.commit()