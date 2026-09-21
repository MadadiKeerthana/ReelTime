from datetime import datetime, timedelta


def watch_seconds_7d(events, as_of):
    cutoff = as_of - timedelta(days=7)
    total = 0
    
    for event in events:
        timestamp = datetime.fromisoformat(event["timestamp"])
        
        if cutoff <= timestamp <= as_of:
            total += event["watch_seconds"]
        
    return total
