import sqlite3
from datetime import datetime, timezone

import database
from models.viewing_event import ViewingEvent


def test_duplicate_event_does_not_double_count(tmp_path, monkeypatch):
    test_db = tmp_path/"test_reeltime.db"
    
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        str(test_db)
    )
    
    database.initialize_database()
    
    event = ViewingEvent(
        event_id="duplicate_test_1",
        user_id="user_1",
        title_id="movie_1",
        genre="Action",
        watch_seconds=100,
        timestamp=datetime(
            2026, 9, 21, 12, 0, 0,
            tzinfo=timezone.utc
        )
    )
    
    first_result = database.process_event(event)
    second_result = database.process_event(event)
    features = database.get_user_features("user_1")
    
    assert first_result is True
    assert second_result is False
    assert features["total_watch_seconds"] == 100
    assert features["event_count"] == 1
    
    with sqlite3.connect(database.DATABASE_PATH) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT COUNT(*)
            FROM viewing_events
            WHERE event_id = ?
        """, ("duplicate_test_1",))
        
        raw_count = cursor.fetchone()[0]
        
    assert raw_count == 1
    
def test_recompute_7d_feature_expires_old_events(tmp_path, monkeypatch):
    test_db = tmp_path / "test_reeltime.db"
    
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        str(test_db)
    )

    database.initialize_database()
     
    event1 = ViewingEvent(
        event_id="window_event_1",
        user_id="window_user",
        title_id="movie_1",
        genre="Action",
        watch_seconds=200,
        timestamp=datetime(
            2026, 9, 14, 12, 0, 0,
            tzinfo=timezone.utc
        )
    )

    event2 = ViewingEvent(
        event_id="window_event_2",
        user_id="window_user",
        title_id="movie_2",
        genre="Comedy",
        watch_seconds=300,
        timestamp=datetime(
            2026, 9, 18, 12, 0, 0,
            tzinfo=timezone.utc
        )
    )

    event3 = ViewingEvent(
        event_id="window_event_3",
        user_id="window_user",
        title_id="movie_3",
        genre="Drama",
        watch_seconds=400,
        timestamp=datetime(
            2026, 9, 21, 12, 0, 0,
            tzinfo=timezone.utc
        )
    )
    
    database.process_event(event1)
    database.process_event(event2)
    database.process_event(event3)
    
    database.recompute_7d_feature(
        "window_user",
        datetime(2026, 9, 21, 12, 0, 0, tzinfo=timezone.utc)
    )
    
    features = database.get_user_features("window_user")
    
    assert features["total_watch_seconds"] == 900
    assert features["event_count"] == 3
    assert features["watch_seconds_7d"] == 900
    
    database.recompute_7d_feature(
        "window_user",
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    )
    
    features = database.get_user_features("window_user")
    
    assert features["total_watch_seconds"] == 900
    assert features["event_count"] == 3
    assert features["watch_seconds_7d"] == 700
        
    
    
    
    