# coding: utf-8
"""
データベース接続に関する設定を管理するモジュール。

このファイルでは、SQLAlchemyを使用してデータベースへの接続設定、
セッションの作成、およびモデルのベースクラスの定義を行います。
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースファイルのパス
# ここでは、プロジェクトルートに `office_management.db` という名前の
# SQLiteデータベースファイルを作成します。
SQLALCHEMY_DATABASE_URL = "sqlite:///./office_management.db"

# データベースエンジンを作成します。
# `connect_args={"check_same_thread": False}` は、
# SQLiteを使用する際に、複数のスレッドからのアクセスを許可するための設定です。
# FastAPIの非同期処理と連携するために必要となります。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# データベースセッションを管理するための `SessionLocal` クラスを作成します。
# `autocommit=False` と `autoflush=False` は、
# データベースへの変更を自動的にコミット・反映しない設定です。
# これにより、開発者が明示的に `commit()` を呼び出すまで変更が永続化されなくなります。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemyのモデル（テーブル）を定義するためのベースクラスです。
# これを継承して、各モデルクラスを作成します。
Base = declarative_base()
