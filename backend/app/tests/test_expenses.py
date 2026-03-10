from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_expense():
    response = client.post(
        "/api/expenses",
        json={"title": "テスト経費", "amount": 1000.5, "category": "消耗品費"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テスト経費"
    assert data["amount"] == 1000.5
    assert data["category"] == "消耗品費"
    assert "id" in data
    assert "date" in data

def test_get_expenses():
    response = client.get("/api/expenses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_expense():
    # 既存の経費を取得
    expenses = client.get("/api/expenses").json()
    expense_id = expenses[0]["id"]
    
    response = client.put(
        f"/api/expenses/{expense_id}",
        json={"title": "更新経費", "amount": 500, "category": "交際費"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新経費"
    assert data["amount"] == 500

def test_delete_expense():
    expenses = client.get("/api/expenses").json()
    expense_id = expenses[0]["id"]
    
    response = client.delete(f"/api/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Expense deleted"
    
    # 削除されたことを確認
    remaining = client.get("/api/expenses").json()
    assert not any(e["id"] == expense_id for e in remaining)
