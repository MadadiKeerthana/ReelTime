from fastapi import FastAPI

from database import save_event
from models.viewing_event import ViewingEvent
from features import compute_user_features

app = FastAPI()

@app.post("/events")
def create_event(event: ViewingEvent):
    saved = save_event(event)
    return {"status": "saved"} if saved else {"status": "duplicate"}

@app.get("/features/{user_id}")
def get_user_features(user_id: str):
    return compute_user_features(user_id)