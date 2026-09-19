from fastapi import FastAPI

from database import save_event
from models.viewing_event import ViewingEvent

app = FastAPI()

@app.post("/events")
def create_event(event: ViewingEvent):
    saved = save_event(event)
    return {"status": "saved"} if saved else {"status": "duplicate"}
