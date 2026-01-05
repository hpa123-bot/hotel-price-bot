import os
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import uvicorn
from web import app as web_app

from scraper import get_price
from storage import (
    init_db,
    add_hotel,
    get_all,
    get_by_chat,
    update_price,
    remove_by_id,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))

SUPPORTED_SITES = ("booking.com", "hotels.com", "expedia.com")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏨 Hotel Price Tracker Bot\n\n"
        "/track <url>\n"
        "/list\n"
        "/remove <number>\n\n"
        "Dashboard:\n"
        "Open the web app URL"
    )


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /track <hotel url>")
        return

    url = context.args[0]

    if not any(site in url for site in SUPPORTED_SITES):
        await update.message.reply_text("❌ Unsupported website.")
        return

    price = get_price(url)
    if price is None:
        await update.message.reply_text("❌ Could not detect price.")
        return

    add_hotel(update.effective_chat.id, url, price)
    await update.message.reply_text(f"✅ Tracking added at ${price}")


async def list_hotels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hotels = get_by_chat(update.effective_chat.id)
    if not hotels:
        await update.message.reply_text("📭 No tracked hotels.")
        return

    msg = "📋 Tracked hotels:\n\n"
    for i, h in enumerate(hotels, start=1):
        msg += f"{i}. ${h['last_price']} — {h['url']}\n\n"

    await update.message.reply_text(msg)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /remove <number>")
        return

    success = remove_by_id(update.effective_chat.id, int(context.args[0]))
    await update.message.reply_text("🗑️ Removed" if success else "❌ Invalid number")


async def check_prices(bot_app):
    for h in get_all():
        new_price = get_price(h["url"])
        if new_price is None:
            continue

        if new_price < h["last_price"]:
            await bot_app.bot.send_message(
                chat_id=h["chat_id"],
                text=(
                    "💸 Price dropped!\n\n"
                    f"Old: ${h['last_price']}\n"
                    f"New: ${new_price}\n\n"
                    f"{h['url']}"
                )
            )
            update_price(h["id"], new_price)


async def start_web():
    config = uvicorn.Config(
        web_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    init_db()

    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("track", track))
    bot_app.add_handler(CommandHandler("list", list_hotels))
    bot_app.add_handler(CommandHandler("remove", remove))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_prices, "interval", minutes=60, args=[bot_app])
    scheduler.start()

    await asyncio.gather(
        bot_app.run_polling(),
        start_web(),
    )


if __name__ == "__main__":
    asyncio.run(main())
