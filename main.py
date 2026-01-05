import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aiohttp import web

# === ENV VARIABLES ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set!")

# === CHAT ID STORAGE ===
CHAT_ID_FILE = "chat_id.txt"

def load_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            return int(f.read().strip())
    return None

def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))

# === BOT SETUP ===
chat_id = load_chat_id()
bot = Bot(token=TOKEN)

async def send_message():
    global chat_id
    if chat_id:
        try:
            await bot.send_message(chat_id=chat_id, text="Hello! This is a scheduled message.")
        except Exception as e:
            print(f"Failed to send message: {e}")
    else:
        print("No chat_id set yet. Waiting for user to send /start.")

# Telegram command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)
    await update.message.reply_text("Chat ID saved! You will start receiving scheduled messages.")

# HTTP server for Koyeb health check
async def handle(request):
    return web.Response(text="OK")

async def start_http_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("HTTP server running on port 8000 for health checks")

async def main():
    # Start scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, "interval", minutes=10)
    scheduler.start()
    print("Scheduler started")

    # Start Telegram bot
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start()
    print("Telegram bot started")

    # Start HTTP server
    await start_http_server()

    # Keep everything alive
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())