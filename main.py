import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from scraper import get_booking_price
from storage import update_price


from storage import init_db, add_hotel, list_hotels

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send:\n"
        "/add <hotel url>\n"
        "/list"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /add <hotel url>")
        return

    url = context.args[0]
    add_hotel(update.effective_chat.id, url)
    await update.message.reply_text("✅ Hotel added!")


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hotels = list_hotels(update.effective_chat.id)

    if not hotels:
        await update.message.reply_text("No hotels tracked yet.")
        return

    msg = "📋 Tracked hotels:\n"
    for hid, url, price in hotels:
        msg += f"{hid}. {url}\n"

    await update.message.reply_text(msg)


def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("check", check))


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    hotels = list_hotels(chat_id)

    if not hotels:
        await update.message.reply_text("No hotels saved yet.")
        return

    message = "🔍 Price check results:\n"

    for hotel_id, url, last_price in hotels:
        price = get_booking_price(url)

        if price is None:
            message += f"\n❌ Could not fetch price:\n{url}\n"
            continue

        if last_price is None:
            message += f"\n💰 ${price} (first check)\n{url}\n"
        elif price < last_price:
            message += f"\n📉 PRICE DROPPED: ${last_price} → ${price}\n{url}\n"
        elif price > last_price:
            message += f"\n📈 Price increased: ${last_price} → ${price}\n{url}\n"
        else:
            message += f"\n➡️ No change: ${price}\n{url}\n"

        update_price(hotel_id, price)

    await update.message.reply_text(message)


    print("🤖 Bot running...")
    app.run_polling()   # ← IMPORTANT: no await, no asyncio.run


if __name__ == "__main__":
    main()
