from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from database import get_user_features, initialize_database, process_event
from models.viewing_event import ViewingEvent

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/events")
def create_event(event: ViewingEvent):  
    saved = process_event(event)
    return {"status": "saved"} if saved else {"status": "duplicate"}

@app.get("/features/{user_id}")
def serve_user_features(user_id: str):
    features = get_user_features(user_id)
    if features is None:
        raise HTTPException(
            status_code=404,
            detail="User features not found"
        )
    return dict(features)
