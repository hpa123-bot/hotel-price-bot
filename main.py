import os
import sys
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot
from telegram.error import TelegramError
import requests
from bs4 import BeautifulSoup

# ----------------------------
# Environment Variables
# ----------------------------
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN environment variable not set!")
    sys.exit(1)

bot = Bot(token=TOKEN)

# ----------------------------
# Job Functions
# ----------------------------
def check_hotels():
    try:
        # Example: replace with your real hotel scraping/check logic
        url = "https://example.com"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Do your scraping here...
        message = "Hotel prices checked!"
        print(message)  # Logs for Koyeb dashboard
        # Example: send message to your Telegram
        bot.send_message(chat_id="YOUR_CHAT_ID", text=message)
    except TelegramError as e:
        print(f"Telegram error: {e}")
    except Exception as e:
        print(f"Error in job: {e}")

# ----------------------------
# Scheduler Setup
# ----------------------------
scheduler = AsyncIOScheduler()
# Example: run every 10 minutes
scheduler.add_job(check_hotels, IntervalTrigger(minutes=10))

async def main():
    scheduler.start()
    print("Scheduler started. Bot is running...")
    # Keep the container alive
    while True:
        await asyncio.sleep(60)

# ----------------------------
# Start the Bot
# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())