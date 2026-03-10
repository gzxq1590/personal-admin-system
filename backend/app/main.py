# coding: utf-8
"""
このアプリケーションのメインファイルです。

FastAPIアプリケーションを定義し、APIのエンドポイント（ルーティング）を設定します。
CORSミドルウェア、データベースセッション管理、および各APIエンドポイントの
具体的な処理ロジックが含まれています。
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database
from datetime import date
from sqlalchemy import extract, func

# データベースの初期化
# models.pyで定義したテーブルがなければ、データベース内に作成する
models.Base.metadata.create_all(bind=database.engine)

# FastAPIアプリケーションのインスタンスを作成
# `title` は、APIドキュメント（/docs）に表示されるタイトルです。
app = FastAPI(title="事務管理システム API")

# DBセッションを取得するための依存関係
def get_db():
    """
    データベースセッションを取得するためのDI（依存性注入）関数。

    リクエストごとに新しいセッションを生成し、そのリクエストが処理を終えた後に
    セッションをクローズします。`yield` を使うことで、API関数の実行中に
    セッションを渡し、処理が終わったら `finally` ブロックで確実にクローズできます。
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORSミドルウェアの設定
# フロントエンドアプリケーション（例: http://localhost:5173）からの
# APIリクエストを許可するために必要です。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では、実際のフロントエンドのURLに制限することが推奨されます。
    allow_credentials=True,
    allow_methods=["*"],  # "GET", "POST", "PUT", "DELETE" などのHTTPメソッドを許可
    allow_headers=["*"],  # "Content-Type", "Authorization" などのHTTPヘッダーを許可
)

# --- ダッシュボード API ---

@app.get("/api/dashboard", response_model=schemas.DashboardResponse, summary="ダッシュボード情報取得")
async def get_dashboard(db: Session = Depends(get_db)):
    """
    ダッシュボードに必要なサマリー情報を集約して取得します。

    - **未完了のタスク数**: ステータスが "done" 以外のタスクの総数。
    - **未処理のドキュメント数**: 現在登録されているドキュメントの総数（ロジックは要件に応じて変更）。
    - **当月の経費合計**: 現在の月の経費の合計金額。
    - **直近のイベント**: 日付が未来のイベントを近い順に5件まで。
    """
    # 未完了のタスク数を取得
    tasks_count = db.query(models.Task).filter(models.Task.status != "done").count()
    
    # 未処理のドキュメント数を取得（この例では単純に全件数を取得）
    unprocessed_docs = db.query(models.Document).count()
    
    # 当月の経費合計を取得
    today = date.today()
    # `func.sum` を使ってデータベース側で合計を計算させ、効率化を図ります。
    # `total_expenses` が `None` になる場合（経費が0件の場合）を考慮し、`0.0` を設定します。
    total_expenses = db.query(func.sum(models.Expense.amount)).filter(
        extract('year', models.Expense.date) == today.year,
        extract('month', models.Expense.date) == today.month
    ).scalar() or 0.0
    
    # 直近のイベントを取得 (今日以降のイベントを日付の昇順で5件まで)
    upcoming_events = db.query(models.Event).filter(models.Event.date >= today).order_by(models.Event.date.asc()).limit(5).all()
    
    return {
        "summary": {
            "tasks_count": tasks_count,
            "unprocessed_docs": unprocessed_docs,
            "total_expenses": float(total_expenses)
        },
        "upcoming_events": upcoming_events
    }

# --- イベント API ---

@app.post("/api/events", response_model=schemas.Event, status_code=201, summary="イベント新規作成")
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """
    新しいイベントを作成します。
    """
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/api/events/{event_id}", status_code=204, summary="イベント削除")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDのイベントを削除します。
    """
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="指定されたイベントが見つかりません。")
    db.delete(db_event)
    db.commit()
    # ステータスコード 204 (No Content) の場合、レスポンスボディは返さないのが一般的
    return 

# --- ドキュメント API ---

@app.get("/api/documents", response_model=List[schemas.Document], summary="ドキュメント一覧取得")
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ドキュメントの一覧を取得します（ページネーション対応）。
    """
    documents = db.query(models.Document).offset(skip).limit(limit).all()
    return documents

@app.post("/api/documents", response_model=schemas.Document, status_code=201, summary="ドキュメント新規作成")
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    """
    新しいドキュメントを作成します。
    """
    db_document = models.Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@app.put("/api/documents/{doc_id}", response_model=schemas.Document, summary="ドキュメント更新")
def update_document(doc_id: int, document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    """
    指定されたIDのドキュメントを更新します。
    """
    db_document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="指定されたドキュメントが見つかりません。")
    
    # `document` の各フィールドの値を `db_document` に設定
    for key, value in document.model_dump().items():
        setattr(db_document, key, value)
        
    db.commit()
    db.refresh(db_document)
    return db_document

@app.delete("/api/documents/{doc_id}", status_code=204, summary="ドキュメント削除")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDのドキュメントを削除します。
    """
    db_document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="指定されたドキュメントが見つかりません。")
    db.delete(db_document)
    db.commit()
    return

# --- タスク API ---

@app.get("/api/tasks", response_model=List[schemas.Task], summary="タスク一覧取得")
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    タスクの一覧を取得します（ページネーション対応）。
    """
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

@app.post("/api/tasks", response_model=schemas.Task, status_code=201, summary="タスク新規作成")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    新しいタスクを作成します。
    """
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/api/tasks/{task_id}", response_model=schemas.Task, summary="タスク更新")
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    指定されたIDのタスクを更新します。
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="指定されたタスクが見つかりません。")
    
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

@app.patch("/api/tasks/{task_id}/status", response_model=schemas.Task, summary="タスクステータス更新")
def update_task_status(task_id: int, task_update: schemas.TaskUpdateStatus, db: Session = Depends(get_db)):
    """
    指定されたIDのタスクのステータスのみを更新します。
    `PATCH` メソッドは、リソースの一部を更新するのに適しています。
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="指定されたタスクが見つかりません。")
        
    db_task.status = task_update.status
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/tasks/{task_id}", status_code=204, summary="タスク削除")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDのタスクを削除します。
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="指定されたタスクが見つかりません。")
    db.delete(db_task)
    db.commit()
    return

# --- 経費 API ---

@app.get("/api/expenses", response_model=List[schemas.Expense], summary="経費一覧取得")
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    経費の一覧を日付の降順で取得します（ページネーション対応）。
    """
    expenses = db.query(models.Expense).order_by(models.Expense.date.desc()).offset(skip).limit(limit).all()
    return expenses

@app.post("/api/expenses", response_model=schemas.Expense, status_code=201, summary="経費新規作成")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """
    新しい経費項目を作成します。
    """
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.put("/api/expenses/{expense_id}", response_model=schemas.Expense, summary="経費更新")
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """
    指定されたIDの経費項目を更新します。
    """
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="指定された経費が見つかりません。")
        
    for key, value in expense.model_dump().items():
        setattr(db_expense, key, value)
        
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/api/expenses/{expense_id}", status_code=204, summary="経費削除")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDの経費項目を削除します。
    """
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="指定された経費が見つかりません。")
    db.delete(db_expense)
    db.commit()
    return
