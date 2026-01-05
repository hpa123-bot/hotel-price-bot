import os
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import start, track, list_hotels
from scheduler import check_prices

TOKEN = os.environ["BOT_TOKEN"]

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("track", track))
app.add_handler(CommandHandler("list", list_hotels))

scheduler = AsyncIOScheduler()
scheduler.add_job(check_prices, "interval", hours=6, args=[app])
scheduler.start()

app.run_polling()