import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.error import TelegramError
from aiohttp import web

# === ENV VARIABLES ===
TOKEN = os.environ.get("BOT_TOKEN")  # your bot token
CHAT_ID = os.environ.get("CHAT_ID")  # chat ID where bot sends messages

if not TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID not set in environment variables!")

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

# === YOUR JOBS ===
async def send_message():
    try:
        await bot.send_message(chat_id=CHAT_ID, text="Hello! This is a scheduled message.")
        print("Message sent successfully.")
    except TelegramError as e:
        print(f"Failed to send message: {e}")

# Add job every 10 minutes as example
scheduler.add_job(send_message, "interval", minutes=10)

# === DUMMY HTTP SERVER FOR KOYEB HEALTH CHECK ===
async def handle(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", handle)

async def start_webserver():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("Dummy HTTP server started on port 8000")

# === START EVERYTHING ===
async def main():
    await start_webserver()  # health check server
    scheduler.start()        # start scheduler
    print("Scheduler started. Bot is running...")
    # Keep the app alive
    while True:
        await asyncio.sleep(3600)

# Run the asyncio loop
if __name__ == "__main__":
    asyncio.run(main())