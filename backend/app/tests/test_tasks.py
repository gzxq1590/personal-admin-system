import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Task

client = TestClient(app)

def test_get_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    response = client.post("/api/tasks", json={
        "title": "新規タスク",
        "description": "新規内容",
        "status": "todo"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "新規タスク"
    assert data["id"] is not None

def test_update_task_status():
    db = SessionLocal()
    # 既存データをクリア
    db.query(Task).delete()
    task = Task(title="検証タスク", description="テスト内容", status="todo")
    db.add(task)
    db.commit()
    db.refresh(task)
    task_id = task.id
    db.close()

    # ステータスを in_progress に更新
    response = client.patch(f"/api/tasks/{task_id}/status", json={"status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"

def test_update_task_full():
    db = SessionLocal()
    task = Task(title="更新前", description="内容前", status="todo")
    db.add(task)
    db.commit()
    db.refresh(task)
    task_id = task.id
    db.close()

    response = client.put(f"/api/tasks/{task_id}", json={
        "title": "更新後",
        "description": "内容後",
        "status": "done"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新後"
    assert data["status"] == "done"

def test_delete_task():
    db = SessionLocal()
    task = Task(title="削除対象", status="todo")
    db.add(task)
    db.commit()
    db.refresh(task)
    task_id = task.id
    db.close()

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    
    # 削除後の確認
    response = client.get(f"/api/tasks")
    assert not any(t["id"] == task_id for t in response.json())
