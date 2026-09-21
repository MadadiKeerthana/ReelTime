import sqlite3

from features import watch_seconds_7d

DATABASE_PATH = "reeltime.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    
    return connection

def initialize_database():
    with get_connection() as connection:
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
                total_watch_seconds INTEGER NOT NULL,
                event_count INTEGER NOT NULL DEFAULT 0,
                watch_seconds_7d INTEGER NOT NULL DEFAULT 0
            )
        """)

def process_event(event):
    try:
        with get_connection() as connection:
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
                total_watch_seconds,
                event_count
            )
            VALUES (?, ?, 1)
            
            ON CONFLICT(user_id)
            DO UPDATE SET
                total_watch_seconds = user_features.total_watch_seconds + excluded.total_watch_seconds,
                event_count = user_features.event_count + excluded.event_count
            """,
            (event.user_id, event.watch_seconds))
        
        return True
    
    except sqlite3.IntegrityError:
        return False

def get_events_for_user(user_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM viewing_events WHERE user_id = ?",
                       (user_id,)
                       )
        
        rows = cursor.fetchall()
        
        return rows
           
def get_user_features(user_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute("""SELECT * FROM user_features
                       WHERE user_id = ?
                       """, 
                       (user_id,))
        row = cursor.fetchone()
        
        return row

def backfill_user_features():
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute("""
        SELECT 
            user_id,
            SUM(watch_seconds),
            COUNT(*)
        FROM viewing_events
        GROUP BY user_id
        """)

        rows = cursor.fetchall()
        
        for user_id, total_watch_seconds, count in rows:
            cursor.execute("""
            INSERT INTO user_features (
                user_id,
                total_watch_seconds,
                event_count
            )
            VALUES (?, ?, ?)
            
            ON CONFLICT(user_id)
            DO UPDATE SET
            event_count = excluded.event_count,
            total_watch_seconds = excluded.total_watch_seconds
            """,
            (user_id, total_watch_seconds, count))
            
def recompute_7d_feature(user_id, as_of):
    events = get_events_for_user(user_id)
    total = watch_seconds_7d(events, as_of)
    
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE user_features
        SET watch_seconds_7d = ?
        WHERE user_id = ? """,
        (total, user_id))
    
def recompute_all_7d_features(as_of):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT user_id
        FROM user_features
        """)
        
        rows = cursor.fetchall()
        
    for (user_id,) in rows:
        recompute_7d_feature(user_id, as_of)
