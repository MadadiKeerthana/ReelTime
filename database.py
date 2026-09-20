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

def save_event(event):
    try:
        with sqlite3.connect("reeltime.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO viewing_events (
                    event_id, 
                    user_id, 
                    title_id,
                    genre,
                    watch_seconds,
                    timestamp) Values 
                    (?, ?, ?, ?, ?, ?)""",
                    (event.event_id, 
                    event.user_id, 
                    event.title_id, 
                    event.genre,
                    event.watch_seconds,
                    event.timestamp.isoformat())
            )  
        return True
    
    except sqlite3.IntegrityError:
        return False

def get_events_for_user(user_id):
    with sqlite3.connect("reeltime.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM viewing_events WHERE user_id = ?",
                       (user_id,)
                       )
        
        rows = cursor.fetchall()
        
        return rows

