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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            habit_type TEXT NOT NULL,
            point_value INTEGER NOT NULL,
            FOREIGN KEY (season_id) REFERENCES seasons (id)
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
    season_id = cursor.lastrowid
    conn.close()
    return season_id, next_index

def get_active_season():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seasons WHERE is_active = 1")
    row = cursor.fetchone()
    conn.close()
    return row

def save_habit(season_id, name, point_value, habit_type="binary"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO habits (season_id, name, habit_type, point_value)
        VALUES (?, ?, ?, ?)
        """,
        (season_id, name, habit_type, point_value),
    )
    conn.commit()
    conn.close()

def get_habits_for_season(season_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE season_id = ?", (season_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database initialized - zrda.db created.")