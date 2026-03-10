<script setup>
import { ref, onMounted } from 'vue'

const summary = ref({
  tasks_count: 0,
  unprocessed_docs: 0,
  total_expenses: 0
})
const upcomingEvents = ref([])
const newEvent = ref({ title: '', date: '' })
const showAddEvent = ref(false)

const fetchData = async () => {
  try {
    const response = await fetch('/api/dashboard')
    const data = await response.json()
    summary.value = data.summary
    upcomingEvents.value = data.upcoming_events
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

const addEvent = async () => {
  if (!newEvent.value.title || !newEvent.value.date) return
  try {
    const response = await fetch('/api/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newEvent.value)
    })
    if (response.ok) {
      await fetchData()
      newEvent.value = { title: '', date: '' }
      showAddEvent.value = false
    }
  } catch (error) {
    console.error('Failed to add event:', error)
  }
}

const deleteEvent = async (eventId) => {
  try {
    const response = await fetch(`/api/events/${eventId}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      await fetchData()
    }
  } catch (error) {
    console.error('Failed to delete event:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="dashboard">
    <h1>ダッシュボード</h1>
    
    <div class="stats-grid">
      <div class="card stat-card">
        <div class="stat-label">未着手タスク</div>
        <div class="stat-value">{{ summary.tasks_count }}</div>
      </div>
      <div class="card stat-card">
        <div class="stat-label">ドキュメント数</div>
        <div class="stat-value">{{ summary.unprocessed_docs }}</div>
      </div>
      <div class="card stat-card">
        <div class="stat-label">今月の経費 (概算)</div>
        <div class="stat-value">¥{{ summary.total_expenses.toLocaleString() }}</div>
      </div>
    </div>

    <div class="content-grid">
      <div class="card event-card">
        <div class="card-header">
          <h3>直近の予定</h3>
          <button class="btn btn-primary btn-sm" @click="showAddEvent = !showAddEvent">
            {{ showAddEvent ? 'キャンセル' : '予定追加' }}
          </button>
        </div>

        <div v-if="showAddEvent" class="add-event-form">
          <input v-model="newEvent.title" type="text" placeholder="予定の内容">
          <input v-model="newEvent.date" type="datetime-local">
          <button class="btn btn-primary btn-sm" @click="addEvent">追加</button>
        </div>

        <ul class="event-list">
          <li v-for="event in upcomingEvents" :key="event.id" class="event-item">
            <span class="event-date">{{ new Date(event.date).toLocaleDateString() }}</span>
            <span class="event-title">{{ event.title }}</span>
            <button class="delete-btn" @click="deleteEvent(event.id)">×</button>
          </li>
          <li v-if="upcomingEvents.length === 0" class="empty-msg">予定はありません</li>
        </ul>
      </div>

    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  text-align: center;
  padding: 1.5rem;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary);
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.add-event-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--bg);
  border-radius: 8px;
}

.add-event-form input {
  padding: 0.5rem;
  border: 1px solid var(--border);
  border-radius: 4px;
}

.event-list {
  list-style: none;
  padding: 0;
}

.event-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
}

.event-date {
  font-weight: 600;
  color: var(--primary);
  margin-right: 1.5rem;
  min-width: 100px;
}

.event-title {
  flex: 1;
}

.delete-btn {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0 0.5rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.text-muted {
  color: var(--text-muted);
}

.empty-msg {
  padding: 2rem;
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  .add-event-form {
    flex-direction: column;
  }
}
</style>
