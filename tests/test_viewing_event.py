from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from models.viewing_event import ViewingEvent

def test_viewing_event_negative_watch_seconds():
    with pytest.raises(ValidationError):
        ViewingEvent(
            event_id="event_1",
            user_id="user_1",
            title_id="movie_1",
            genre="Action",
            watch_seconds=-100,
            timestamp=datetime(2026, 9, 21, 19, 0, 0, tzinfo=timezone.utc)
    )
         
def test_viewing_event_rejects_naive_timestamp():
    with pytest.raises(ValidationError):
        ViewingEvent(
            event_id="event_1",
            user_id="user_1",
            title_id="movie_1",
            genre="Action",
            watch_seconds=100,
            timestamp=datetime(2026, 9, 21, 12, 0, 0)
        )

def test_viewing_event_normalizes_timestamp_to_utc():
    eastern = timezone(timedelta(hours=-4))
    
    event = ViewingEvent(
        event_id="event_2",
        user_id="user_1",
        title_id="movie_1",
        genre="Action",
        watch_seconds=100,
        timestamp=datetime(2026, 9, 21, 15, 0, 0, tzinfo=eastern)
    )
    
    assert event.timestamp == datetime(2026, 9, 21, 19, 0, 0, tzinfo=timezone.utc)

    