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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_features (
        user_id TEXT PRIMARY KEY,
        total_watch_seconds INTEGER NOT NULL
    )
""")

connection.commit()
connection.close()

def process_event(event):
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
            
            cursor.execute("""
            INSERT INTO user_features (
                user_id,
                total_watch_seconds
            )
            VALUES (?, ?)
            
            ON CONFLICT(user_id)
            DO UPDATE SET
                total_watch_seconds = user_features.total_watch_seconds + excluded.total_watch_seconds
            """,
            (event.user_id, event.watch_seconds))
        
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
           
def get_user_features(user_id):
    with sqlite3.connect("reeltime.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        cursor.execute("""SELECT * FROM user_features
                       WHERE user_id = ?
                       """, 
                       (user_id,))
        row = cursor.fetchone()
        
        return row
    