# coding: utf-8
"""
データベースのテーブル構造を定義するモジュール。

このファイルでは、SQLAlchemyのORM（Object-Relational Mapper）を用いて、
アプリケーションで使用する各テーブルのスキーマをPythonクラスとして定義します。
それぞれのクラスがデータベース上の一つのテーブルに対応し、クラスの属性が
テーブルのカラムに対応します。
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Task(Base):
    """
    タスク情報を管理するテーブル (`tasks`) のモデル。
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, comment="タスクID")
    title = Column(String, index=True, comment="タスクのタイトル")
    description = Column(String, comment="タスクの詳細な説明")
    status = Column(String, default="todo", comment="タスクの進捗状況 (todo, in_progress, done)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="作成日時")

class Document(Base):
    """
    提出ドキュメント情報を管理するテーブル (`documents`) のモデル。
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, comment="ドキュメントID")
    filename = Column(String, comment="ファイル名")
    file_type = Column(String, comment="ファイル形式 (例: pdf, image)")
    upload_date = Column(DateTime(timezone=True), server_default=func.now(), comment="アップロード日")
    meta_data = Column(String, comment="柔軟性を持たせるためのJSON形式のメタデータ")

class Expense(Base):
    """
    経費情報を管理するテーブル (`expenses`) のモデル。
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, comment="経費ID")
    title = Column(String, comment="経費の項目名")
    amount = Column(Float, comment="金額")
    category = Column(String, comment="経費のカテゴリ (例: 交通費, 消耗品費)")
    date = Column(DateTime(timezone=True), server_default=func.now(), comment="支払日")

class Event(Base):
    """
    カレンダーイベント情報を管理するテーブル (`events`) のモデル。
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, comment="イベントID")
    title = Column(String, comment="イベントのタイトル")
    date = Column(DateTime(timezone=True), comment="イベントの開催日時")
