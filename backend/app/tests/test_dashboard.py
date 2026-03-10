import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Event, Task, Document
from datetime import datetime

client = TestClient(app)

def test_get_dashboard_dynamic():
    db = SessionLocal()
    # 既存データをクリア
    db.query(Event).delete()
    db.query(Task).delete()
    db.query(Document).delete()
    
    # テストデータ投入
    db.add(Event(title="動的予定1", date=datetime(2026, 3, 5)))
    db.add(Task(title="タスク1", status="todo"))
    db.add(Document(filename="doc1.pdf", file_type="PDF"))
    db.commit()
    db.close()

    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["tasks_count"] == 1
    assert data["summary"]["unprocessed_docs"] == 1
    assert len(data["upcoming_events"]) == 1
    assert data["upcoming_events"][0]["title"] == "動的予定1"

def test_create_event():
    response = client.post("/api/events", json={
        "title": "新規イベント",
        "date": "2026-03-20T10:00:00"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "新規イベント"

def test_delete_event():
    db = SessionLocal()
    ev = Event(title="削除待ち", date=datetime.now())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    ev_id = ev.id
    db.close()

    response = client.delete(f"/api/events/{ev_id}")
    assert response.status_code == 200
    
    response = client.get("/api/dashboard")
    assert not any(e["id"] == ev_id for e in response.json()["upcoming_events"])
