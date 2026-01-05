import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from db import init_db, add_hotel
from scraper import get_price
from tracker import start_scheduler

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏨 Hotel Price Bot\n\n"
        "/track <url> – start tracking a hotel\n"
        "/help – show commands"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/track <url>\n/help"
    )

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /track <hotel_url>")
        return

    url = context.args[0]
    price = get_price(url)

    if price is None:
        await update.message.reply_text("❌ Couldn't find a price on that page.")
        return

    add_hotel(update.effective_chat.id, url, price)

    await update.message.reply_text(
        f"✅ Tracking started\nCurrent price: ${price}"
    )

def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("track", track))

    start_scheduler(app)

    print("🤖 Bot running with scheduler")
    app.run_polling()

if __name__ == "__main__":
    main()
