import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Document

client = TestClient(app)

def test_get_documents():
    response = client.get("/api/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_document_metadata():
    response = client.post("/api/documents", json={
        "filename": "test_contract.pdf",
        "file_type": "PDF",
        "meta_data": "契約書サンプル"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_contract.pdf"
    assert data["id"] is not None

def test_update_document_metadata():
    db = SessionLocal()
    doc = Document(filename="old_name.png", file_type="PNG", meta_data="古いメモ")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    doc_id = doc.id
    db.close()

    response = client.put(f"/api/documents/{doc_id}", json={
        "filename": "new_name.png",
        "file_type": "PNG",
        "meta_data": "更新されたメモ"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["meta_data"] == "更新されたメモ"

def test_delete_document():
    db = SessionLocal()
    doc = Document(filename="to_delete.txt", file_type="TXT")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    doc_id = doc.id
    db.close()

    response = client.delete(f"/api/documents/{doc_id}")
    assert response.status_code == 200
    
    # 削除後の確認
    response = client.get(f"/api/documents")
    assert not any(d["id"] == doc_id for d in response.json())
