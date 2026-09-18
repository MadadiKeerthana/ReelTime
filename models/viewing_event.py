from datetime import datetime

from pydantic import BaseModel

class ViewingEvent(BaseModel):
    event_id: str
    user_id: str
    title_id: str
    genre: str
    watch_seconds: int
    timestamp: datetime