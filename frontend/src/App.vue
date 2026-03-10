<script setup>
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Documents from './components/Documents.vue'
import Tasks from './components/Tasks.vue'
import Expenses from './components/Expenses.vue'

const currentView = ref('dashboard')
</script>

<template>
  <nav class="navbar">
    <div class="container nav-content">
      <div class="brand">事務管理システム</div>
      <div class="menu">
        <a href="#" :class="{ active: currentView === 'dashboard' }" @click.prevent="currentView = 'dashboard'">ダッシュボード</a>
        <a href="#" :class="{ active: currentView === 'documents' }" @click.prevent="currentView = 'documents'">ドキュメント</a>
        <a href="#" :class="{ active: currentView === 'tasks' }" @click.prevent="currentView = 'tasks'">タスク</a>
        <a href="#" :class="{ active: currentView === 'expenses' }" @click.prevent="currentView = 'expenses'">経費管理</a>
      </div>
    </div>
  </nav>

  <main class="container">
    <Dashboard v-if="currentView === 'dashboard'" />
    <Documents v-else-if="currentView === 'documents'" />
    <Tasks v-else-if="currentView === 'tasks'" />
    <Expenses v-else-if="currentView === 'expenses'" />
  </main>
</template>

<style>
.navbar {
  background: white;
  border-bottom: 1px solid var(--border);
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
}

.menu a {
  margin-left: 1.5rem;
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 500;
  transition: color 0.2s;
}

.menu a:hover, .menu a.active {
  color: var(--primary);
}
</style>
