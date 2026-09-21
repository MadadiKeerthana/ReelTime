from datetime import datetime, timezone

from features import watch_seconds_7d

def test_watch_seconds_7d():
    events = [
    {
        "timestamp": "2026-09-13T12:00:00+00:00",
        "watch_seconds": 100
    },
    {
        "timestamp": "2026-09-14T12:00:00+00:00",
        "watch_seconds": 200
    },
    {
        "timestamp": "2026-09-18T12:00:00+00:00",
        "watch_seconds": 300
    },
    {
        "timestamp": "2026-09-21T12:00:00+00:00",
        "watch_seconds": 400
    },
    {
        "timestamp": "2026-09-22T12:00:00+00:00",
        "watch_seconds": 500
    }
]
    as_of = datetime(
        2026, 9, 21, 12, 0, 0,
        tzinfo=timezone.utc
    )
    
    assert watch_seconds_7d(events, as_of) == 900

    