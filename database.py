import sqlite3

connection = sqlite3.connect("reeltime.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS viewing_events (
        event_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title_id TEXT NOT NULL,
        genre TEXT NOT NULL,
        watch_seconds INTEGER NOT NULL,
        timestamp TEXT NOT NULL
    )
""")

connection.commit()

connection.close()