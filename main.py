import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from aiohttp import web

# -----------------------
# Bot Configuration
# -----------------------
TOKEN = os.environ["BOT_TOKEN"]  # Make sure this is set in Koyeb secrets
CHAT_ID = os.environ.get("CHAT_ID")  # Optional: use if you send messages on start

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()
scheduler.start()
print("Scheduler started. Bot is running...")

# Example scheduled task
def example_task():
    print("Running scheduled task...")
    # Example: send a message to your chat
    if CHAT_ID:
        asyncio.create_task(bot.send_message(chat_id=CHAT_ID, text="Hello from the bot!"))

# Schedule every minute (adjust as needed)
scheduler.add_job(example_task, 'interval', minutes=1)

# -----------------------
# Dummy HTTP server for Koyeb health check
# -----------------------
async def handle_health(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.add_routes([web.get("/", handle_health)])

# -----------------------
# Run bot & server concurrently
# -----------------------
web.run_app(app, host="0.0.0.0", port=8000)