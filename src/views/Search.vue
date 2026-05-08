<script setup>
import { ref, onMounted } from 'vue'

const API_BASE_URL = 'http://127.0.0.1:5001'

const currentUserId = ref(null)

const location = ref('')
const minAge = ref('')
const maxAge = ref('')
const interests = ref('')
const results = ref([])
const errorMessage = ref('')
const loading = ref(false)
const searched = ref(false)

const loadCurrentUser = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/me`, {
      credentials: 'include'
    })

    if (res.ok) {
      const data = await res.json()
      currentUserId.value = Number(data.id ?? data.user_id ?? null)
    } else {
      currentUserId.value = null
    }
  } catch (err) {
    console.error('loadCurrentUser error:', err)
    currentUserId.value = null
  }
}

const formatInterests = (userInterests) => {
  if (!userInterests) return []
  if (Array.isArray(userInterests)) return userInterests
  if (typeof userInterests === 'string') {
    return userInterests
      .split(',')
      .map(i => i.trim())
      .filter(i => i !== '')
  }
  return []
}

const getProfilePhoto = (user) => {
  if (!user.profile_pic_url) return null
  return `${API_BASE_URL}/uploads/${user.profile_pic_url}`
}

const searchUsers = async () => {
  loading.value = true
  errorMessage.value = ''
  searched.value = true

  const params = new URLSearchParams()
  if (location.value.trim()) params.append('location', location.value.trim())
  if (minAge.value) params.append('min_age', minAge.value)
  if (maxAge.value) params.append('max_age', maxAge.value)
  if (interests.value.trim()) params.append('interests', interests.value.trim())

  try {
    const res = await fetch(`${API_BASE_URL}/search?${params.toString()}`, {
      credentials: 'include'
    })

    const data = await res.json()

    if (res.ok) {
      const normalized = data.map(u => ({
        ...u,
        _uid: Number(u.user_id ?? u.id)
      }))

      if (currentUserId.value != null) {
        results.value = normalized.filter(u => u._uid !== currentUserId.value)
      } else {
        results.value = normalized
      }
    } else {
      errorMessage.value = data.error || 'Search failed.'
    }
  } catch (err) {
    console.error('searchUsers error:', err)
    errorMessage.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

onMounted(loadCurrentUser)
</script>

<template>
  <div class="search-page">
    <h1>Search Profiles</h1>

    <div class="search-card">
      <div class="form-field">
        <label>Location</label>
        <input v-model="location" type="text" placeholder="Kingston" />
      </div>

      <div class="form-field">
        <label>Min age</label>
        <input v-model="minAge" type="number" placeholder="18" />
      </div>

      <div class="form-field">
        <label>Max age</label>
        <input v-model="maxAge" type="number" placeholder="35" />
      </div>

      <div class="form-field">
        <label>Interests</label>
        <input v-model="interests" type="text" placeholder="music, football" />
      </div>

      <button @click="searchUsers" :disabled="loading">
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="searched && !loading && results.length === 0" class="empty">
      No users found.
    </p>

    <div class="grid">
      <div v-for="user in results" :key="user.user_id" class="card">
        <img
          v-if="getProfilePhoto(user)"
          :src="getProfilePhoto(user)"
          :alt="user.name"
          class="profile-photo"
        />

        <div v-else class="avatar">
          {{ user.name?.charAt(0) || '?' }}
        </div>

        <h2>{{ user.name }}, {{ user.age }}</h2>
        <p class="location">{{ user.location }}</p>
        <p v-if="user.bio" class="bio">{{ user.bio }}</p>

        <div class="interests">
          <span
            v-for="interest in formatInterests(user.interests)"
            :key="interest"
            class="tag"
          >
            {{ interest }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  min-height: 100vh;
  padding: 30px;
  background: #fff5f7;
  text-align: center;
}

h1 {
  margin-bottom: 24px;
}

.search-card {
  max-width: 950px;
  margin: 0 auto 28px;
  background: white;
  padding: 20px;
  border-radius: 14px;
  display: grid;
  grid-template-columns: repeat(4, 1fr) auto;
  gap: 12px;
  align-items: end;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

.form-field {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

input {
  height: 42px;
  padding: 0 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.95rem;
}

button {
  height: 42px;
  padding: 0 18px;
  border: none;
  border-radius: 8px;
  background: #e85d75;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 18px;
}

.card {
  background: white;
  padding: 22px 18px;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

.avatar,
.profile-photo {
  width: 65px;
  height: 65px;
  margin: 0 auto 12px;
  border-radius: 50%;
}

.avatar {
  background: #4a90e2;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.profile-photo {
  object-fit: cover;
  display: block;
}

.location {
  color: #777;
  margin-bottom: 8px;
}

.bio {
  font-size: 0.95rem;
  margin-bottom: 12px;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  margin-top: 12px;
}

.tag {
  background: #eef4ff;
  color: #2d5f9a;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.82rem;
}

.error {
  color: #c0392b;
}

.empty {
  color: #666;
}

@media (max-width: 900px) {
  .search-card {
    grid-template-columns: 1fr 1fr;
  }

  button {
    grid-column: span 2;
  }
}

@media (max-width: 600px) {
  .search-card {
    grid-template-columns: 1fr;
  }

  button {
    grid-column: span 1;
  }
}
</style>