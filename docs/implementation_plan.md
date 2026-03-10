# 事務管理システム実装計画（修正版）

共有されたGeminiリンクに基づき、個人利用に特化した「シンプルで可読性重視」の事務管理システムを構築します。

## ユーザーレビューが必要な項目

> [!IMPORTANT]
> ユーザーのフィードバックに基づき、以下の方針で進めます：
> 1. **技術スタック**: バックエンドは Python (FastAPI) + SQLite、フロントエンドは **Vue.js** を使用します。
> 2. **デザイン**: ガラスモーフィズムをやめ、**シンプルで可読性を最優先**したモダンなデザインを採用します。
> 3. **品質管理**:
>    - **TDD (Test-Driven Development)**: ユニットレベルの単体テストは実装前に行います。
>    - **BDD (Behavior-Driven Development)**: 機能面（ユースケース）の検証は振る舞いに基づいて行います。

## 提案される変更点

### プロジェクト構造
```text
/backend  - FastAPI, SQLAlchemy, Alembic, pytest (TDD)
/frontend - Vue 3 (Vite), TailwindCSS (シンプルデザイン用), Vitest/Playwright (BDD)
```

### バックエンド (Python/FastAPI)
- **TDDサイクル**: 最初にテスト（`tests/`）を書き、それをパスするように `main.py`, `models.py`, `schemas.py` を実装します。
- **機能**: ダッシュボード、ドキュメント管理、タスク管理のAPI。

### フロントエンド (Vue.js)
- **BDD検証**: アプリケーションの各画面（`Dashboard`, `Documents`, `Tasks`）の正常な遷移と操作をテストコードで定義してから実装します。
- **デザイン**: 落ち着いた配色と十分なコントラスト、明快なタイポグラフィを採用します。

---

## 検証プラン

### ユニットテスト (TDD)
- `pytest` を使用し、DB操作やロジックの単体テストを網羅します。

### 機能テスト (BDD)
- `behave` (Python) またはフロントエンドの `Playwright` などのツールを使用し、ユーザーシナリオに沿ったテストを実行します。

