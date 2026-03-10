import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Task, Document, Expense

# テスト用のインメモリデータベース
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_task():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    task = Task(title="テストタスク", description="テスト内容", status="todo")
    db.add(task)
    db.commit()
    db.refresh(task)
    
    assert task.id is not None
    assert task.title == "テストタスク"
    db.close()

def test_create_expense():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    expense = Expense(title="ランチ代", amount=1200.0, category="食費")
    db.add(expense)
    db.commit()
    db.refresh(expense)
    
    assert expense.id is not None
    assert expense.amount == 1200.0
    db.close()
