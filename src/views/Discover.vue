<script setup>
import { ref, onMounted } from 'vue'

const profiles = ref([])
const message = ref('')
const errorMessage = ref('')

const fetchPotentialMatches = async () => {
  try {
    const response = await fetch('/api/potential-matches')
    if (response.ok) {
      profiles.value = await response.json()
    } else if (response.status === 401) {
      errorMessage.value = 'Please login to see potential matches.'
    } else {
      const data = await response.json()
      errorMessage.value = data.error || 'Failed to fetch matches.'
    }
  } catch (error) {
    console.error('Error fetching potential matches:', error)
    errorMessage.value = 'An error occurred while fetching profiles.'
  }
}

onMounted(() => {
  fetchPotentialMatches()
})

const like = async (profile) => {
  try {
    const response = await fetch(`/api/like/${profile.user_id}`, {
      method: 'POST'
    })
    const data = await response.json()
    if (response.ok) {
      message.value = data.message || `You liked ${profile.name}`
      // Remove from list
      profiles.value = profiles.value.filter(p => p.user_id !== profile.user_id)
    } else {
      message.value = data.error || 'Failed to like user.'
    }
  } catch (error) {
    console.error(error)
  }
}

const pass = async (profile) => {
  try {
    const response = await fetch(`/api/pass/${profile.user_id}`, {
      method: 'POST'
    })
    if (response.ok) {
      message.value = `You passed ${profile.name}`
      // Remove from list
      profiles.value = profiles.value.filter(p => p.user_id !== profile.user_id)
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div class="discover">
    <h1>Discover</h1>

    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <div v-if="profiles.length > 0" class="grid">
      <div v-for="profile in profiles" :key="profile.user_id" class="card">
        <div class="avatar">
          {{ profile.name.charAt(0) }}
        </div>

        <h2>{{ profile.name }}, {{ profile.age }}</h2>
        <p class="location">{{ profile.location }}</p>

        <div class="interests">
          <span v-for="i in profile.interests" :key="i" class="tag">
            {{ i }}
          </span>
        </div>

        <div class="buttons">
          <button class="pass" @click="pass(profile)">Pass</button>
          <button class="like" @click="like(profile)">Like</button>
        </div>
      </div>
    </div>

    <div v-else-if="!errorMessage" class="no-matches">
      <p>No more potential matches found. Check back later!</p>
    </div>
  </div>
</template>

<style scoped>
.discover {
  padding: 30px;
  background: #f4f7fb;
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
  color: #1e8449;
}

.no-matches {
  margin-top: 40px;
  color: #666;
  font-size: 1.1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

.avatar {
  width: 60px;
  height: 60px;
  margin: 0 auto 10px;
  border-radius: 50%;
  background: #4a90e2;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  font-weight: bold;
}

.location {
  color: #777;
  margin-bottom: 10px;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  margin-bottom: 15px;
}

.tag {
  background: #eef4ff;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
}

.buttons {
  display: flex;
  gap: 10px;
}

button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.pass {
  background: #f8d7da;
}

.like {
  background: #4a90e2;
  color: white;
}
</style>