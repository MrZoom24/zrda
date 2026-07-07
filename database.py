import sqlite3
from datetime import date

DB_FILE = "zrda.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS seasons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season_index INTEGER NOT NULL,
            season_length INTEGER NOT NULL,
            block_length INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        )
        """
    )
    conn.commit()
    conn.close()

def save_season(season_length, block_length):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(season_index) FROM seasons")
    last_index = cursor.fetchone()[0]
    next_index = 1 if last_index is None else last_index + 1

    cursor.execute("UPDATE seasons SET is_active = 0 WHERE is_active = 1")

    cursor.execute(
        """
        INSERT INTO seasons (season_index, season_length, block_length, start_date, is_active)
        VALUES (?, ?, ?, ?, 1)
        """,
        (next_index, season_length, block_length, str(date.today())),
    )
    conn.commit()
    conn.close()
    return next_index

def get_active_season():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seasons WHERE is_active = 1")
    row = cursor.fetchone()
    conn.close()
    return row

if __name__ == "__main__":
    init_db()
    print("Database initialized - zrda.db created.")