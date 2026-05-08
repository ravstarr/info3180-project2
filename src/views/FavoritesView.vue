<script setup>
import { ref, onMounted } from 'vue'

const API_BASE_URL = 'http://127.0.0.1:5000'

const favorites = ref([])
const loading = ref(false)
const errorMessage = ref('')

const getProfilePhoto = (profile) => {
  if (!profile.profile_pic_url) return null
  return `${API_BASE_URL}/uploads/${profile.profile_pic_url}`
}

const fetchFavorites = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/favorites`, {
      method: 'GET',
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      favorites.value = data
    } else if (response.status === 401) {
      errorMessage.value = 'Please login to view favorites.'
    } else {
      errorMessage.value = data.error || 'Failed to load favorites.'
    }
  } catch (error) {
    console.error('Error fetching favorites:', error)
    errorMessage.value = 'Could not connect to backend server.'
  } finally {
    loading.value = false
  }
}

const removeFavorite = async (profile) => {
  try {
    const response = await fetch(`${API_BASE_URL}/favorites/${profile.user_id}`, {
      method: 'POST',
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok) {
      favorites.value = favorites.value.filter(
        p => p.user_id !== profile.user_id
      )
    } else {
      errorMessage.value = data.error || 'Failed to remove favorite.'
    }
  } catch (error) {
    console.error('Error removing favorite:', error)
    errorMessage.value = 'Could not connect to backend server.'
  }
}

onMounted(fetchFavorites)
</script>

<template>
  <div class="favorites">
    <h1>Your Favorites</h1>

    <p v-if="loading">Loading favorites...</p>

    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </p>

    <div v-if="favorites.length > 0" class="grid">
      <div
        v-for="profile in favorites"
        :key="profile.user_id"
        class="card"
      >
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

        <p class="location">
          {{ profile.location }}
        </p>

        <p class="bio">
          {{ profile.bio }}
        </p>

        <button
          class="remove-btn"
          @click="removeFavorite(profile)"
        >
          Remove Favorite
        </button>
      </div>
    </div>

    <div v-else-if="!loading && !errorMessage" class="empty">
      <p>No favorites yet.</p>
    </div>
  </div>
</template>

<style scoped>
.favorites {
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

.empty {
  margin-top: 40px;
  color: #777;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 22px;
}

.card {
  background: white;
  padding: 22px;
  border-radius: 16px;
  border: 1px solid #1f1f1f;
  box-shadow: 0 5px 14px rgba(217, 79, 112, 0.08);
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
}

.bio {
  margin-bottom: 18px;
  color: #555;
}

.remove-btn {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 10px;
  background: #e85d75;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.remove-btn:hover {
  background: #d94f70;
}
</style>