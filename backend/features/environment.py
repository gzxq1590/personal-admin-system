from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Expense

def before_all(context):
    # テストクライアントの初期化
    context.client = TestClient(app)

def before_scenario(context, scenario):
    # シナリオごとにDBをクリーンアップ（簡易版：Expenseテーブルのみ全削除）
    db = SessionLocal()
    db.query(Expense).delete()
    db.commit()
    db.close()
