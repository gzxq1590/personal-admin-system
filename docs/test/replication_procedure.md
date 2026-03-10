# プロジェクト再現手順 (Replication Procedure)

本プロジェクトの環境構築およびテスト実行を再現するための手順とコマンドを以下にまとめます。

## 1. バックエンドのセットアップ
バックエンドは Python (FastAPI) で構成されています。

```powershell
# バックエンドディレクトリへ移動
cd Pj01/backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
.\venv\Scripts\Activate.ps1

# 依存ライブラリのインストール
pip install fastapi uvicorn sqlalchemy pydantic pytest httpx
```

## 2. データベースの初期化
初回起動時に SQLite データベース (`office_management.db`) が自動的に作成されます。

## 3. テストの実行 (TDD)
ユニットテストおよび結合テストを実行するコマンドです。

```powershell
# 仮想環境が有効な状態で
$env:PYTHONPATH="."
pytest -v app/tests/test_main.py app/tests/test_docs.py app/tests/test_models.py
```

## 4. エビデンスの出力
試験ログ（エビデンス）をファイルに出力する場合：

```powershell
# 既にある場合は削除して新規作成
if (Test-Path test_results) { Remove-Item -Recurse -Force test_results }
mkdir test_results
pytest -v app/tests/test_main.py app/tests/test_docs.py app/tests/test_models.py > test_results/pytest_evidence.txt 2>&1
```

## 5. サーバーの起動
```powershell
# APIサーバーの起動 (ポート 8000)
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

---

## 6. フロントエンドのセットアップ
フロントエンドは Vue 3 (Vite) で構成されています。

```powershell
# フロントエンドディレクトリへ移動
cd Pj01/frontend

# 依存ライブラリのインストール
npm install

# 開発サーバーの起動 (ポート 5173)
npm run dev
```
