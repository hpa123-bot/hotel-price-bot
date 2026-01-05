from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Application
from scraper import get_price
from db import get_hotels, update_price

scheduler = BackgroundScheduler()

def start_scheduler(app: Application):
    scheduler.add_job(
        check_prices,
        "interval",
        hours=6,
        args=[app],
        id="price_check",
        replace_existing=True
    )
    scheduler.start()

def check_prices(app: Application):
    hotels = get_hotels()

    for hotel_id, chat_id, url, last_price in hotels:
        new_price = get_price(url)

        if new_price and new_price < last_price:
            app.bot.send_message(
                chat_id=chat_id,
                text=f"💸 Price dropped!\n\nOld: ${last_price}\nNew: ${new_price}\n{url}"
            )
            update_price(hotel_id, new_price)