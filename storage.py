import sqlite3

DB_PATH = "hotels.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            last_price REAL
        )
    """)

    conn.commit()
    conn.close()


def add_hotel(chat_id, url):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO hotels (chat_id, url, last_price) VALUES (?, ?, NULL)",
        (chat_id, url),
    )
    conn.commit()
    conn.close()


def list_hotels(chat_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, url, last_price FROM hotels WHERE chat_id = ?",
        (chat_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
