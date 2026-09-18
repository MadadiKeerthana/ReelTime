from fastapi import FastAPI
from models.viewing_event import ViewingEvent

app = FastAPI()

@app.post("/events")
def create_event(event: ViewingEvent):
    return event
