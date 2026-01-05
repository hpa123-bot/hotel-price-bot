import sqlite3

DB_NAME = "hotels.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            url TEXT,
            last_price REAL
        )
    """)
    conn.commit()
    conn.close()

def add_hotel(chat_id, url, price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO hotels (chat_id, url, last_price) VALUES (?, ?, ?)",
        (chat_id, url, price)
    )
    conn.commit()
    conn.close()

def get_hotels():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, chat_id, url, last_price FROM hotels")
    rows = c.fetchall()
    conn.close()
    return rows

def update_price(hotel_id, new_price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE hotels SET last_price = ? WHERE id = ?",
        (new_price, hotel_id)
    )
    conn.commit()
    conn.close()