import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_dashboard():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "tasks_count" in data["summary"]
    assert "upcoming_events" in data
