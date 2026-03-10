<script setup>
import { ref, onMounted } from 'vue'

const documents = ref([])
const isEditing = ref(false)
const currentDoc = ref({ filename: '', file_type: '', meta_data: '' })

const fetchDocuments = async () => {
  try {
    const response = await fetch('/api/documents')
    documents.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch documents:', error)
  }
}

const openAddModal = () => {
  currentDoc.value = { filename: '', file_type: 'PDF', meta_data: '' }
  isEditing.value = true
}

const openEditModal = (doc) => {
  currentDoc.value = { ...doc }
  isEditing.value = true
}

const closeIdModal = () => {
  isEditing.value = false
}

const saveDocument = async () => {
  try {
    const method = currentDoc.value.id ? 'PUT' : 'POST'
    const url = currentDoc.value.id 
      ? `/api/documents/${currentDoc.value.id}`
      : '/api/documents'
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentDoc.value)
    })
    
    if (response.ok) {
      await fetchDocuments()
      closeIdModal()
    }
  } catch (error) {
    console.error('Failed to save document:', error)
  }
}

const deleteDocument = async (docId) => {
  if (!confirm('このドキュメントを削除してもよろしいですか？')) return
  try {
    const response = await fetch(`/api/documents/${docId}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      await fetchDocuments()
    }
  } catch (error) {
    console.error('Failed to delete document:', error)
  }
}

onMounted(() => {
  fetchDocuments()
})
</script>

<template>
  <div class="documents">
    <div class="header-actions">
      <h1>ドキュメント管理</h1>
      <button class="btn btn-primary" @click="openAddModal">新規登録</button>
    </div>
    
    <div class="card">
      <table class="doc-table">
        <thead>
          <tr>
            <th>ドキュメント名</th>
            <th>種類</th>
            <th>登録日</th>
            <th>タグ/メモ</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in documents" :key="doc.id">
            <td>{{ doc.filename }}</td>
            <td><span class="badge">{{ doc.file_type }}</span></td>
            <td>{{ new Date(doc.upload_date).toLocaleDateString() }}</td>
            <td>{{ doc.meta_data || '-' }}</td>
            <td>
              <div class="actions-cell">
                <button class="icon-btn" @click="openEditModal(doc)">✏️</button>
                <button class="icon-btn delete" @click="deleteDocument(doc.id)">🗑️</button>
              </div>
            </td>
          </tr>
          <tr v-if="documents.length === 0">
            <td colspan="5" class="empty-msg">ドキュメントが見つかりません</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 編集・追加モーダル -->
    <div v-if="isEditing" class="modal-overlay" @click.self="closeIdModal">
      <div class="modal card">
        <h2>{{ currentDoc.id ? 'ドキュメント編集' : '新規ドキュメント登録' }}</h2>
        <div class="form-group">
          <label>ドキュメント名</label>
          <input v-model="currentDoc.filename" type="text" placeholder="契約書、請求書など">
        </div>
        <div class="form-group">
          <label>種類</label>
          <select v-model="currentDoc.file_type">
            <option value="PDF">PDF</option>
            <option value="PNG">PNG/JPG</option>
            <option value="DOCX">DOCX</option>
            <option value="Excel">Excel</option>
            <option value="Other">その他</option>
          </select>
        </div>
        <div class="form-group">
          <label>タグ/メモ</label>
          <textarea v-model="currentDoc.meta_data" rows="3" placeholder="書類に関するメモ"></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn" @click="closeIdModal">キャンセル</button>
          <button class="btn btn-primary" @click="saveDocument">保存</button>
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

.doc-table {
  width: 100%;
  border-collapse: collapse;
}

.doc-table th {
  text-align: left;
  padding: 1rem;
  border-bottom: 2px solid var(--border);
  color: var(--text-muted);
  font-weight: 600;
}

.doc-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
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
  padding: 3rem !important;
  color: var(--text-muted);
}
</style>
