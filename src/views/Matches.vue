<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const matches = ref([])
const message = ref('')
const errorMessage = ref('')
const loading = ref(false)

const API_BASE_URL = 'http://127.0.0.1:5001'

const loadMatches = async () => {
  loading.value = true
  message.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/matches`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      matches.value = data
    } else {
      errorMessage.value = data.error || 'Failed to load matches.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

const openChat = (match) => {
  router.push(`/messages/${match.match_id}`)
}

const unmatchUser = async (matchId) => {
  if (!confirm('Are you sure you want to unmatch this user?')) return

  message.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/unmatch/${matchId}`, {
      method: 'DELETE',
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message || 'User unmatched successfully.'
      matches.value = matches.value.filter(match => match.match_id !== matchId)
    } else {
      errorMessage.value = data.error || 'Failed to unmatch user.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to backend.'
  }
}

const getProfilePhoto = (user) => {
  return user.profile_pic_url
    ? `${API_BASE_URL}/uploads/${user.profile_pic_url}`
    : null
}

onMounted(loadMatches)
</script>

<template>
  <div class="matches-page">
    <h1>Your Matches</h1>

    <p v-if="loading">Loading matches...</p>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <p v-if="!loading && matches.length === 0">
      No matches yet.
    </p>

    <div class="match-list">
      <div v-for="user in matches" :key="user.match_id" class="match-card">
        <img
          v-if="getProfilePhoto(user)"
          :src="getProfilePhoto(user)"
          :alt="user.name"
          class="profile-photo"
        />

        <div v-else class="avatar">
          {{ user.name?.charAt(0) || '?' }}
        </div>

        <h2>{{ user.name }}</h2>

        <div class="actions">
          <button @click="openChat(user)">Message</button>

          <button class="unmatch-btn" @click="unmatchUser(user.match_id)">
            Unmatch
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.matches-page {
  min-height: 100vh;
  padding: 30px;
  text-align: center;
  background: #fff5f7;
}

.match-list {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 25px;
}

.match-card {
  width: 240px;
  padding: 22px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.profile-photo,
.avatar {
  width: 75px;
  height: 75px;
  margin: 0 auto 12px;
  border-radius: 50%;
}

.profile-photo {
  object-fit: cover;
  display: block;
}

.avatar {
  background: #4a90e2;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: bold;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 14px;
}

button {
  padding: 8px 13px;
  border: none;
  border-radius: 8px;
  background-color: #e85d75;
  color: white;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

.unmatch-btn {
  background: #4a90e2;
}

.message {
  color: #1e8449;
}

.error-message {
  color: #c0392b;
}
</style>