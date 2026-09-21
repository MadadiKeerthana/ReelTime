from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

class ViewingEvent(BaseModel):
    event_id: str
    user_id: str
    title_id: str
    genre: str
    watch_seconds: int = Field(gt=0)
    timestamp: datetime
    
    @field_validator("timestamp")
    @classmethod
    def timestamp_must_have_timezone(cls, value):
        if value.tzinfo is None:
            raise ValueError("timestamp must include timezone information")

        return value.astimezone(timezone.utc)