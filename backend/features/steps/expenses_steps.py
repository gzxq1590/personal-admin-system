from behave import given, when, then
from fastapi.testclient import TestClient

@given('経費データベースが初期化されている')
def step_impl(context):
    context.response = None
    context.created_expense_id = None

@when('以下の内容で経費を登録する:')
def step_impl_create_expense(context):
    row = context.table[0]
    payload = {
        "title": row["title"],
        "amount": float(row["amount"]),
        "category": row["category"]
    }
    context.response = context.client.post("/api/expenses", json=payload)
    if context.response.status_code == 200:
        context.created_expense_id = context.response.json().get("id")

@then('経費の登録が成功し、登録されたデータの "{key}" が "{value}" であること')
def step_impl_check_creation(context, key, value):
    assert context.response.status_code == 200, f"Status code is {context.response.status_code}"
    data = context.response.json()
    assert str(data[key]) == value, f"Expected {value}, got {data[key]}"

@then('APIで経費一覧を取得すると、作成した経費が含まれていること')
def step_impl_check_list(context):
    resp = context.client.get("/api/expenses")
    assert resp.status_code == 200
    expenses = resp.json()
    assert any(e["id"] == context.created_expense_id for e in expenses), "Created expense not found in list"

@given('以下の内容で経費がすでに登録されている:')
def step_impl_pre_create_expense(context):
    row = context.table[0]
    payload = {
        "title": row["title"],
        "amount": float(row["amount"]),
        "category": row["category"]
    }
    resp = context.client.post("/api/expenses", json=payload)
    assert resp.status_code == 200
    context.created_expense_id = resp.json().get("id")

@when('その経費の金額を "{new_amount}" に更新する')
def step_impl_update_expense(context, new_amount):
    assert context.created_expense_id is not None
    payload = {
        "title": "更新テスト用",
        "amount": float(new_amount),
        "category": "テスト"
    }
    context.response = context.client.put(f"/api/expenses/{context.created_expense_id}", json=payload)

@then('更新が成功し、データの "{key}" が "{value}" であること')
def step_impl_check_update(context, key, value):
    assert context.response.status_code == 200, f"Status code is {context.response.status_code}"
    data = context.response.json()
    if key == 'amount':
        assert float(data[key]) == float(value), f"Expected {value}, got {data[key]}"
    else:
        assert str(data[key]) == value, f"Expected {value}, got {data[key]}"

@when('その経費を削除する')
def step_impl_delete_expense(context):
    assert context.created_expense_id is not None
    context.response = context.client.delete(f"/api/expenses/{context.created_expense_id}")

@then('削除が成功すること')
def step_impl_check_delete(context):
    assert context.response.status_code == 200, f"Status code is {context.response.status_code}"

@then('APIで経費一覧を取得すると、その経費が含まれていないこと')
def step_impl_check_deleted_list(context):
    resp = context.client.get("/api/expenses")
    assert resp.status_code == 200
    expenses = resp.json()
    assert not any(e["id"] == context.created_expense_id for e in expenses), "Deleted expense still found in list"

# --- 異常系（Negative Tests）のステップ定義 ---

@when('以下の不正な内容で経費を登録する:')
def step_impl_create_invalid_expense(context):
    row = context.table[0]
    payload = {
        "title": row["title"],
        "amount": row["amount"], # 意図的にパースせず不正な値(文字列)を送信
        "category": row["category"]
    }
    context.response = context.client.post("/api/expenses", json=payload)

@then('クライアントエラー（{status_code:d}）が発生すること')
def step_impl_check_client_error(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"

@when('存在しない経費ID "{fake_id}" の金額を "{new_amount}" に更新する')
def step_impl_update_fake_expense(context, fake_id, new_amount):
    payload = {
        "title": "存在しない",
        "amount": float(new_amount),
        "category": "テスト"
    }
    context.response = context.client.put(f"/api/expenses/{fake_id}", json=payload)

@then('エラー（{status_code:d}）が発生し、"{err_msg}" というメッセージが返ること')
def step_impl_check_error_msg(context, status_code, err_msg):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"
    data = context.response.json()
    assert data["detail"] == err_msg, f"Expected '{err_msg}', got '{data.get('detail')}'"

@when('存在しない経費ID "{fake_id}" を削除する')
def step_impl_delete_fake_expense(context, fake_id):
    context.response = context.client.delete(f"/api/expenses/{fake_id}")
