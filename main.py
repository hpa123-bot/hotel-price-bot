import os
import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scraper import get_price
from storage import add_hotel, get_all, get_by_chat, update_price


BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


SUPPORTED_SITES = ("booking.com", "hotels.com", "expedia.com")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏨 Hotel Price Tracker Bot\n\n"
        "Commands:\n"
        "/track <hotel URL>\n"
        "/list\n\n"
        "Supported sites:\n"
        "- Booking.com\n"
        "- Hotels.com\n"
        "- Expedia"
    )


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage:\n/track <hotel url WITH dates>"
        )
        return

    url = context.args[0]

    if not any(site in url for site in SUPPORTED_SITES):
        await update.message.reply_text(
            "❌ Unsupported website."
        )
        return

    price = get_price(url)

    if price is None:
        await update.message.reply_text(
            "❌ Could not detect price.\n"
            "Make sure dates & currency are included."
        )
        return

    add_hotel(update.effective_chat.id, url, price)

    await update.message.reply_text(
        f"✅ Tracking added\nPrice: ${price}"
    )


async def list_hotels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hotels = get_by_chat(update.effective_chat.id)

    if not hotels:
        await update.message.reply_text(
            "📭 You are not tracking any hotels."
        )
        return

    msg = "📋 Tracked hotels:\n\n"
    for i, h in enumerate(hotels, start=1):
        msg += f"{i}. ${h['last_price']} — {h['url']}\n\n"

    await update.message.reply_text(msg)


async def check_prices(app):
    for item in get_all():
        new_price = get_price(item["url"])

        if new_price is None:
            continue

        if new_price < item["last_price"]:
            await app.bot.send_message(
                chat_id=item["chat_id"],
                text=(
                    "💸 Price dropped!\n\n"
                    f"Old: ${item['last_price']}\n"
                    f"New: ${new_price}\n\n"
                    f"{item['url']}"
                )
            )
            update_price(item, new_price)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))
    app.add_handler(CommandHandler("list", list_hotels))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_prices,
        "interval",
        minutes=60,
        args=[app],
    )
    scheduler.start()

    print("🤖 Bot running...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
