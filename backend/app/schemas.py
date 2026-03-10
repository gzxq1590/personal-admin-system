# Pydanticモデルを定義するためのBaseModelをインポート
from pydantic import BaseModel
# 日時を扱うためのdatetimeをインポート
from datetime import datetime
# 型ヒントのためのOptional, List, Dictをインポート
from typing import Optional, List, Dict

# --- ToDoタスク関連のスキーマ ---

# Taskの基本となるスキーマ
class TaskBase(BaseModel):
    title: str  # タスクのタイトル
    description: Optional[str] = None  # タスクの説明（任意）
    status: str = "todo"  # タスクのステータス（デフォルトは "todo"）

# Taskを作成する際のスキーマ
class TaskCreate(TaskBase):
    pass  # TaskBaseの全フィールドを継承

# データベースから読み込んだTaskを表すスキーマ
class Task(TaskBase):
    id: int  # タスクの一意なID
    created_at: datetime  # タスクの作成日時

    # ORMモデルからPydanticモデルへの変換を有効にする設定
    class Config:
        from_attributes = True

# --- ドキュメント関連のスキーマ ---

# Documentの基本となるスキーマ
class DocumentBase(BaseModel):
    filename: str  # ファイル名
    file_type: str  # ファイルタイプ (例: "pdf", "docx")
    meta_data: Optional[str] = None  # メタデータ（任意）

# Documentを作成する際のスキーマ
class DocumentCreate(DocumentBase):
    pass  # DocumentBaseの全フィールドを継承

# データベースから読み込んだDocumentを表すスキーマ
class Document(DocumentBase):
    id: int  # ドキュメントの一意なID
    upload_date: datetime  # アップロード日時

    # ORMモデルからPydanticモデルへの変換を有効にする設定
    class Config:
        from_attributes = True

# --- 経費関連のスキーマ ---

# Expenseの基本となるスキーマ
class ExpenseBase(BaseModel):
    title: str  # 経費の項目名
    amount: float  # 金額
    category: str  # カテゴリ

# Expenseを作成する際のスキーマ
class ExpenseCreate(ExpenseBase):
    pass  # ExpenseBaseの全フィールドを継承

# データベースから読み込んだExpenseを表すスキーマ
class Expense(ExpenseBase):
    id: int  # 経費の一意なID
    date: datetime  # 発生日

    # ORMモデルからPydanticモデルへの変換を有効にする設定
    class Config:
        from_attributes = True

# --- ダッシュボード関連のスキーマ ---

# ダッシュボードのサマリー情報を表すスキーマ
class DashboardSummary(BaseModel):
    tasks_count: int  # タスクの総数
    unprocessed_docs: int  # 未処理ドキュメントの数
    total_expenses: float  # 経費の合計金額

# Taskのステータスを更新するためのスキーマ
class TaskUpdateStatus(BaseModel):
    status: str  # 新しいステータス

# Eventの基本となるスキーマ
class EventBase(BaseModel):
    title: str  # イベントのタイトル
    date: datetime  # イベントの日時

# Eventを作成する際のスキーマ
class EventCreate(EventBase):
    pass # EventBaseの全フィールドを継承

# データベースから読み込んだEventを表すスキーマ
class Event(EventBase):
    id: int # イベントの一意なID

    # ORMモデルからPydanticモデルへの変換を有効にする設定
    class Config:
        from_attributes = True

# ダッシュボードAPIのレスポンス全体を表すスキーマ
class DashboardResponse(BaseModel):
    summary: DashboardSummary  # サマリー情報
    upcoming_events: List[Event]  # 今後のイベントリスト
