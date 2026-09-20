from database import get_events_for_user

def total_watch_seconds(events):
    total = 0
    for event in events:
        total += event["watch_seconds"]
    
    return total

def compute_user_features(user_id):
    events = get_events_for_user(user_id)
    
    return {
        "user_id": user_id,
        "total_watch_seconds": total_watch_seconds(events)
    }
    