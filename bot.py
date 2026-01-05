from telegram import Update
from telegram.ext import ContextTypes
from db import cursor, conn
from scraper import get_price

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏨 Hotel Price Tracker Bot\n\n"
        "Commands:\n"
        "/track <hotel_name> <url> <target_price>\n"
        "/list"
    )

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hotel_name = context.args[0]
        url = context.args[1]
        target_price = float(context.args[2])

        current_price = get_price(url)

        cursor.execute("""
        INSERT INTO tracked_hotels
        VALUES (?, ?, ?, ?, ?)
        """, (update.effective_chat.id, hotel_name, url, target_price, current_price))
        conn.commit()

        await update.message.reply_text(
            f"✅ Tracking {hotel_name}\n"
            f"Current price: ${current_price}\n"
            f"Target price: ${target_price}"
        )
    except Exception:
        await update.message.reply_text(
            "❌ Usage:\n"
            "/track HotelName BookingURL TargetPrice"
        )

async def list_hotels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "SELECT hotel_name, last_price, target_price FROM tracked_hotels WHERE chat_id=?",
        (update.effective_chat.id,)
    )
    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text("No hotels tracked.")
        return

    msg = "\n".join([f"{h}: ${lp} → ${tp}" for h, lp, tp in rows])
    await update.message.reply_text(msg)