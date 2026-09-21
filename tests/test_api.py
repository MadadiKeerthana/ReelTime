from fastapi.testclient import TestClient

import database
from main import app

def test_event_ingestion_and_feature_serving(tmp_path, monkeypatch):
    test_db = tmp_path / "test_reeltime.db"
    
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        str(test_db)
    )
    
    with TestClient(app) as client:
        response = client.post(
            "/events",
            json={
                "event_id": "api_event_1",
                "user_id": "api_user",
                "title_id": "movie_1",
                "genre": "Action",
                "watch_seconds": 250,
                "timestamp": "2026-09-21T12:00:00+00:00"
            }
        )
        
        assert response.status_code == 200
        assert response.json() == {"status": "saved"}
        
        response = client.get("/features/api_user")
        
        assert response.json()["total_watch_seconds"] == 250
        assert response.json()["event_count"] == 1