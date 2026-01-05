import sqlite3

conn = sqlite3.connect("hotels.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tracked_hotels (
    chat_id INTEGER,
    hotel_name TEXT,
    url TEXT,
    target_price REAL,
    last_price REAL
)
""")

conn.commit()