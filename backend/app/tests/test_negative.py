from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_delete_event_not_found():
    response = client.delete("/api/events/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_update_document_not_found():
    response = client.put(
        "/api/documents/99999",
        json={"filename": "存在しない", "file_type": "PDF"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_delete_document_not_found():
    response = client.delete("/api/documents/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_update_task_not_found():
    response = client.put(
        "/api/tasks/99999",
        json={"title": "存在しない", "status": "todo"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task_status_not_found():
    response = client.patch(
        "/api/tasks/99999/status",
        json={"status": "done"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task_not_found():
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_expense_not_found():
    response = client.put(
        "/api/expenses/99999",
        json={"title": "存在しない", "amount": 1000, "category": "テスト"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_delete_expense_not_found():
    response = client.delete("/api/expenses/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"
