<script setup>
import { ref, onMounted } from 'vue'

const expenses = ref([])
const isEditing = ref(false)
const currentExpense = ref({ title: '', amount: 0, category: '備品・消耗品' })

const fetchExpenses = async () => {
  try {
    const response = await fetch('/api/expenses')
    expenses.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch expenses:', error)
  }
}

const openAddModal = () => {
  currentExpense.value = { title: '', amount: 0, category: '備品・消耗品' }
  isEditing.value = true
}

const openEditModal = (expense) => {
  currentExpense.value = { ...expense }
  isEditing.value = true
}

const closeModal = () => {
  isEditing.value = false
}

const saveExpense = async () => {
  if (!currentExpense.value.title || currentExpense.value.amount <= 0) {
    alert('品目と正しい金額を入力してください。')
    return
  }
  
  try {
    const method = currentExpense.value.id ? 'PUT' : 'POST'
    const url = currentExpense.value.id 
      ? `/api/expenses/${currentExpense.value.id}`
      : '/api/expenses'
    
    // 金額を数値にパース
    const payload = { ...currentExpense.value, amount: Number(currentExpense.value.amount) }
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (response.ok) {
      await fetchExpenses()
      closeModal()
    }
  } catch (error) {
    console.error('Failed to save expense:', error)
  }
}

const deleteExpense = async (expenseId) => {
  if (!confirm('この経費録を削除してもよろしいですか？')) return
  try {
    const response = await fetch(`/api/expenses/${expenseId}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      await fetchExpenses()
    }
  } catch (error) {
    console.error('Failed to delete expense:', error)
  }
}

onMounted(() => {
  fetchExpenses()
})
</script>

<template>
  <div class="expenses">
    <div class="header-actions">
      <h1>経費管理</h1>
      <button class="btn btn-primary" @click="openAddModal">経費の登録</button>
    </div>
    
    <div class="card">
      <table class="expense-table">
        <thead>
          <tr>
            <th>日付</th>
            <th>品目 / 内容</th>
            <th>カテゴリ</th>
            <th>金額</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="expense in expenses" :key="expense.id">
            <td>{{ new Date(expense.date).toLocaleDateString() }}</td>
            <td class="font-medium">{{ expense.title }}</td>
            <td><span class="badge">{{ expense.category }}</span></td>
            <td class="amount">¥{{ expense.amount.toLocaleString() }}</td>
            <td>
              <div class="actions-cell">
                <button class="icon-btn" @click="openEditModal(expense)">✏️</button>
                <button class="icon-btn delete" @click="deleteExpense(expense.id)">🗑️</button>
              </div>
            </td>
          </tr>
          <tr v-if="expenses.length === 0">
            <td colspan="5" class="empty-msg">経費データがありません</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 編集・追加モーダル -->
    <div v-if="isEditing" class="modal-overlay" @click.self="closeModal">
      <div class="modal card">
        <h2>{{ currentExpense.id ? '経費の編集' : '新規経費の登録' }}</h2>
        <div class="form-group">
          <label>品目 / 内容</label>
          <input v-model="currentExpense.title" type="text" placeholder="例：マウス購入、タクシー代など">
        </div>
        <div class="form-group">
          <label>金額 (円)</label>
          <input v-model="currentExpense.amount" type="number" min="0" placeholder="0">
        </div>
        <div class="form-group">
          <label>カテゴリ</label>
          <select v-model="currentExpense.category">
            <option value="備品・消耗品">備品・消耗品</option>
            <option value="交通費">交通費</option>
            <option value="交際費">交際費</option>
            <option value="通信費">通信費</option>
            <option value="その他">その他</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn" @click="closeModal">キャンセル</button>
          <button class="btn btn-primary" @click="saveExpense">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.expense-table {
  width: 100%;
  border-collapse: collapse;
}

.expense-table th {
  text-align: left;
  padding: 1rem;
  border-bottom: 2px solid var(--border);
  color: var(--text-muted);
  font-weight: 600;
}

.expense-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}

.font-medium {
  font-weight: 500;
}

.amount {
  font-weight: 600;
  color: var(--text-main);
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px;
  border-radius: 4px;
}

.icon-btn:hover {
  background: white;
}

.icon-btn.delete:hover {
  background: #fee2e2;
}

.badge {
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #475569;
}

/* モーダル */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-muted);
}

.form-group input, .form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.empty-msg {
  text-align: center;
  padding: 3rem !important;
  color: var(--text-muted);
}
</style>
