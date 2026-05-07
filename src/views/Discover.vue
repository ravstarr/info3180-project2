<script setup>
import { ref, onMounted } from 'vue'

const API_BASE_URL = 'http://127.0.0.1:5000'

const profiles = ref([])
const message = ref('')
const errorMessage = ref('')
const loading = ref(false)

const getProfilePhoto = (profile) => {
  if (!profile.profile_pic_url) return null
  return `${API_BASE_URL}/uploads/${profile.profile_pic_url}`
}

const fetchPotentialMatches = async () => {
  loading.value = true
  message.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/potential-matches`, {
      method: 'GET',
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      profiles.value = data
    } else if (response.status === 401) {
      errorMessage.value = 'Please login to see potential matches.'
    } else if (response.status === 403) {
      errorMessage.value = data.error || 'You do not have permission to view potential matches.'
    } else {
      errorMessage.value = data.error || 'Failed to fetch matches.'
    }
  } catch (error) {
    console.error('Error fetching potential matches:', error)
    errorMessage.value = 'Could not connect to the backend server.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchPotentialMatches)

const like = async (profile) => {
  message.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/like/${profile.user_id}`, {
      method: 'POST',
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message || `You liked ${profile.name}.`
      profiles.value = profiles.value.filter(p => p.user_id !== profile.user_id)
    } else {
      errorMessage.value = data.error || 'Failed to like user.'
    }
  } catch (error) {
    console.error('Error liking user:', error)
    errorMessage.value = 'Could not connect to the backend server.'
  }
}

const pass = async (profile) => {
  message.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/pass/${profile.user_id}`, {
      method: 'POST',
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message || `You passed ${profile.name}.`
      profiles.value = profiles.value.filter(p => p.user_id !== profile.user_id)
    } else {
      errorMessage.value = data.error || 'Failed to pass user.'
    }
  } catch (error) {
    console.error('Error passing user:', error)
    errorMessage.value = 'Could not connect to the backend server.'
  }
}

const formatInterests = (interests) => {
  if (!interests) return []
  if (Array.isArray(interests)) return interests
  if (typeof interests === 'string') return interests.split(',').map(i => i.trim())
  return []
}
</script>

<template>
  <div class="discover">
    <h1>Discover</h1>

    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-if="loading">Loading profiles...</p>

    <div v-if="profiles.length > 0" class="grid">
      <div v-for="profile in profiles" :key="profile.user_id" class="card">
        <img
          v-if="getProfilePhoto(profile)"
          :src="getProfilePhoto(profile)"
          :alt="profile.name"
          class="profile-photo"
        />

        <div v-else class="avatar">
          {{ profile.name?.charAt(0) || '?' }}
        </div>

        <h2>{{ profile.name }}, {{ profile.age }}</h2>
        <p class="location">{{ profile.location }}</p>
        <p class="bio">{{ profile.bio }}</p>

        <div class="interests">
          <span
            v-for="i in formatInterests(profile.interests)"
            :key="i"
            class="tag"
          >
            {{ i }}
          </span>
        </div>

        <div class="buttons">
          <button class="pass" @click="pass(profile)">Pass</button>
          <button class="like" @click="like(profile)">Like</button>
        </div>
      </div>
    </div>

    <div v-else-if="!loading && !errorMessage" class="no-matches">
      <p>No more potential matches found. Check back later!</p>
    </div>
  </div>
</template>

<style scoped>
.discover {
  padding: 30px;
  background: #fff5f7;
  min-height: 100vh;
  text-align: center;
}

.error-message {
  color: #c0392b;
  margin-bottom: 20px;
  font-weight: 600;
}

.message {
  margin-bottom: 20px;
  font-weight: 600;
  color: #c94f68;
}

.no-matches {
  margin-top: 40px;
  color: #777;
  font-size: 1.05rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 22px;
}

.card {
  background: #ffffff;
  padding: 22px;
  border-radius: 16px;
  border: 1px solid #1f1f1f;
  box-shadow: 0 5px 14px rgba(217, 79, 112, 0.08);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
}

.avatar,
.profile-photo {
  width: 68px;
  height: 68px;
  margin: 0 auto 14px;
  border-radius: 50%;
}

.avatar {
  background: #e85d75;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.profile-photo {
  object-fit: cover;
  display: block;
  border: 3px solid #ffd6e0;
}

h2 {
  color: #3d3d3d;
  margin-bottom: 6px;
}

.location {
  color: #888;
  margin-bottom: 12px;
  font-size: 0.95rem;
}

.bio {
  margin-bottom: 14px;
  color: #555;
  line-height: 1.4;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 18px;
}

.tag {
  background: #ffe3ea;
  color: #c94f68;
  padding: 6px 12px;
  border-radius: 18px;
  font-size: 0.82rem;
  font-weight: 500;
}

.buttons {
  display: flex;
  gap: 10px;
}

button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s ease;
}

.pass {
  background: #ffe1e6;
  color: #b54b62;
}

.pass:hover {
  background: #ffd1d9;
}

.like {
  background: #e85d75;
  color: white;
}

.like:hover {
  background: #d94f70;
}
</style>