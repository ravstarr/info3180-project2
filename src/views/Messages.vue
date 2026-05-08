<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const conversations = ref([])
const messages = ref([])
const selectedMatchId = ref(null)
const selectedUserName = ref('')
const currentUserId = ref(null)
const newMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)

const API_BASE_URL = 'http://127.0.0.1:5001'
let refreshInterval = null

function formatDate(dateString) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

const loadCurrentUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/me`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      currentUserId.value = data.id
    }
  } catch (error) {
    console.error(error)
  }
}

const loadConversations = async () => {
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/conversations`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      conversations.value = data

      if (route.params.matchId) {
        const matchId = Number(route.params.matchId)
        const conversation = conversations.value.find(c => Number(c.match_id) === matchId)

        if (conversation) {
          selectedUserName.value = conversation.other_user?.name || 'Chat'
        }

        await loadMessages(matchId)
      }
    } else {
      errorMessage.value = data.error || 'Failed to load conversations.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to backend.'
  }
}

const loadMessages = async (matchId) => {
  selectedMatchId.value = matchId
  loading.value = true
  errorMessage.value = ''

  const conversation = conversations.value.find(c => Number(c.match_id) === Number(matchId))
  selectedUserName.value = conversation?.other_user?.name || 'Chat'

  try {
    const response = await fetch(`${API_BASE_URL}/messages/${matchId}`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      messages.value = data
    } else {
      messages.value = []
      errorMessage.value = data.error || 'Failed to load messages.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedMatchId.value) return

  try {
    const response = await fetch(`${API_BASE_URL}/messages/${selectedMatchId.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        content: newMessage.value.trim()
      })
    })

    const data = await response.json()

    if (response.ok) {
      newMessage.value = ''
      await loadMessages(selectedMatchId.value)
      await loadConversations()
    } else {
      errorMessage.value = data.error || 'Failed to send message.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to backend.'
  }
}

onMounted(async () => {
  await loadCurrentUser()
  await loadConversations()

  refreshInterval = setInterval(async () => {
    if (selectedMatchId.value) {
      await loadMessages(selectedMatchId.value)
      await loadConversations()
    }
  }, 10000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<template>
  <div class="messages-page">
    <h1>Messages</h1>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <div class="messages-layout">
      <div class="conversation-list">
        <h2>Conversations</h2>

        <p v-if="conversations.length === 0" class="empty">
          No conversations yet.
        </p>

        <button
          v-for="conversation in conversations"
          :key="conversation.match_id"
          class="conversation-btn"
          :class="{ active: Number(selectedMatchId) === Number(conversation.match_id) }"
          @click="loadMessages(conversation.match_id)"
        >
          <strong>{{ conversation.other_user?.name || 'Unknown User' }}</strong>
          <small v-if="conversation.last_message?.content">
            {{ conversation.last_message.content }}
          </small>
          <small v-else>No messages yet</small>
        </button>
      </div>

      <div class="chat-box">
        <h2>{{ selectedMatchId ? selectedUserName : 'Chat' }}</h2>

        <p v-if="!selectedMatchId" class="empty">Select a conversation.</p>
        <p v-if="loading">Loading messages...</p>

        <div v-if="selectedMatchId" class="message-list">
          <p v-if="messages.length === 0 && !loading" class="empty">
            No messages yet. Start the conversation.
          </p>

          <div
            v-for="message in messages"
            :key="message.id"
            class="message"
            :class="{
              sent: message.sender_id === currentUserId,
              received: message.sender_id !== currentUserId
            }"
          >
            <p>{{ message.content }}</p>
            <small>{{ formatDate(message.timestamp) }}</small>
          </div>
        </div>

        <form v-if="selectedMatchId" @submit.prevent="sendMessage" class="message-form">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Type a message..."
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.messages-page {
  min-height: 100vh;
  padding: 30px;
  background: #fff5f7;
}

h1 {
  text-align: center;
  margin-bottom: 25px;
  color: #3d3d3d;
}

.messages-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 20px;
}

.conversation-list,
.chat-box {
  background: #ffffff;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid #1f1f1f;
  box-shadow: 0 5px 14px rgba(217, 79, 112, 0.08);
}

.conversation-list h2,
.chat-box h2 {
  color: #d94f70;
  margin-bottom: 15px;
}

.conversation-btn {
  width: 100%;
  margin-bottom: 10px;
  padding: 12px;
  border: 1px solid #1f1f1f;
  border-radius: 8px;
  background: #fffafa;
  color: #3d3d3d;
  cursor: pointer;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.conversation-btn.active {
  background: #e85d75;
  color: white;
}

.conversation-btn small {
  opacity: 0.85;
}

.message-list {
  min-height: 320px;
  max-height: 420px;
  overflow-y: auto;
  margin-bottom: 15px;
  padding: 12px;
  background: #fffafa;
  border: 1px solid #1f1f1f;
  border-radius: 12px;
}

.message {
  padding: 10px 12px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 75%;
}

.message.sent {
  background: #e85d75;
  color: white;
  margin-left: auto;
  text-align: right;
  border: 1px solid #d94f70;
}

.message.received {
  background: #ffe3ea;
  color: #3d3d3d;
  margin-right: auto;
  text-align: left;
  border: 1px solid #f2b8c5;
}

.message p {
  margin: 0 0 5px;
}

.message.sent small {
  color: #ffeef2;
}

.message.received small {
  color: #777;
}

.message-form {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 11px;
  border: 1px solid #1f1f1f;
  border-radius: 8px;
  background: #fffafa;
}

input:focus {
  outline: none;
  border-color: #d94f70;
}

button {
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  background: #e85d75;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

button:hover {
  background: #d94f70;
}

.error {
  color: #c0392b;
  text-align: center;
}

.empty {
  color: #666;
}

@media (max-width: 700px) {
  .messages-layout {
    grid-template-columns: 1fr;
  }
}
</style>