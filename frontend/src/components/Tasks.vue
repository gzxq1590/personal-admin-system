<script setup>
import { ref, onMounted } from 'vue'

const tasks = ref([])
const isEditing = ref(false)
const currentTask = ref({ title: '', description: '', status: 'todo' })

const fetchTasks = async () => {
  try {
    const response = await fetch('/api/tasks')
    tasks.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch tasks:', error)
  }
}

const openAddModal = () => {
  currentTask.value = { title: '', description: '', status: 'todo' }
  isEditing.value = true
}

const openEditModal = (task) => {
  currentTask.value = { ...task }
  isEditing.value = true
}

const closeIdModal = () => {
  isEditing.value = false
}

const saveTask = async () => {
  try {
    const method = currentTask.value.id ? 'PUT' : 'POST'
    const url = currentTask.value.id 
      ? `/api/tasks/${currentTask.value.id}`
      : '/api/tasks'
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentTask.value)
    })
    
    if (response.ok) {
      await fetchTasks()
      closeIdModal()
    }
  } catch (error) {
    console.error('Failed to save task:', error)
  }
}

const deleteTask = async (taskId) => {
  if (!confirm('このタスクを削除してもよろしいですか？')) return
  try {
    const response = await fetch(`/api/tasks/${taskId}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      await fetchTasks()
    }
  } catch (error) {
    console.error('Failed to delete task:', error)
  }
}

const updateStatus = async (taskId, newStatus) => {
  try {
    const response = await fetch(`/api/tasks/${taskId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    if (response.ok) {
      await fetchTasks()
    }
  } catch (error) {
    console.error('Failed to update task status:', error)
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<template>
  <div class="tasks">
    <div class="header-actions">
      <h1>タスク・工程管理</h1>
      <button class="btn btn-primary" @click="openAddModal">新規タスク追加</button>
    </div>
    
    <div class="task-board">
      <div v-for="status in ['todo', 'in_progress', 'done']" :key="status" class="task-column card">
        <h3>{{ status === 'todo' ? '未着手' : (status === 'in_progress' ? '進行中' : '完了') }}</h3>
        <div class="task-list">
          <div v-for="task in tasks.filter(t => t.status === status)" :key="task.id" class="task-item card">
            <div class="task-header">
              <h4>{{ task.title }}</h4>
              <div class="header-btns">
                <button class="icon-btn" @click="openEditModal(task)" title="編集">✏️</button>
                <button class="icon-btn delete" @click="deleteTask(task.id)" title="削除">🗑️</button>
              </div>
            </div>
            <p>{{ task.description }}</p>
            <div class="actions">
              <select :value="task.status" @change="updateStatus(task.id, $event.target.value)">
                <option value="todo">未着手</option>
                <option value="in_progress">進行中</option>
                <option value="done">完了</option>
              </select>
            </div>
          </div>
          <div v-if="tasks.filter(t => t.status === status).length === 0" class="empty-msg">
            タスクなし
          </div>
        </div>
      </div>
    </div>

    <!-- 編集・追加モーダル -->
    <div v-if="isEditing" class="modal-overlay" @click.self="closeIdModal">
      <div class="modal card">
        <h2>{{ currentTask.id ? 'タスク編集' : '新規タスク追加' }}</h2>
        <div class="form-group">
          <label>タイトル</label>
          <input v-model="currentTask.title" type="text" placeholder="タスク名">
        </div>
        <div class="form-group">
          <label>詳細</label>
          <textarea v-model="currentTask.description" rows="3" placeholder="タスクの詳細内容"></textarea>
        </div>
        <div class="form-group">
          <label>ステータス</label>
          <select v-model="currentTask.status">
            <option value="todo">未着手</option>
            <option value="in_progress">進行中</option>
            <option value="done">完了</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn" @click="closeIdModal">キャンセル</button>
          <button class="btn btn-primary" @click="saveTask">保存</button>
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

.task-board {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.task-column h3 {
  border-bottom: 2px solid var(--border);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.task-item {
  padding: 1rem;
  background: var(--bg);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.header-btns {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 2px;
  border-radius: 4px;
}

.icon-btn:hover {
  background: white;
}

.icon-btn.delete:hover {
  background: #fee2e2;
}

.task-item h4 {
  margin: 0;
}

.actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.actions select {
  padding: 0.25rem;
  border-radius: 4px;
  border: 1px solid var(--border);
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
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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

.form-group input, .form-group textarea, .form-group select {
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
  padding: 1rem;
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>
