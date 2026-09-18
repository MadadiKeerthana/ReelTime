from datetime import datetime

from pydantic import BaseModel, Field

class ViewingEvent(BaseModel):
    event_id: str
    user_id: str
    title_id: str
    genre: str
    watch_seconds: int = Field(gt=0)
    timestamp: datetime