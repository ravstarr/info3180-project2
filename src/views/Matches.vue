<script setup>
import { ref } from 'vue'

const matches = ref([
  { id: 1, name: 'Alicia', age: 22 },
  { id: 2, name: 'Jordan', age: 24 }
])

const message = ref('')

const openChat = (name) => {
  message.value = `Opening chat with ${name}`
}
</script>

<template>
  <div class="matches-page">
    <h1>Your Matches</h1>

    <p v-if="message" class="message">{{ message }}</p>

    <div v-if="matches.length === 0">
      <p>No matches yet</p>
    </div>

    <div v-else class="match-list">
      <div v-for="user in matches" :key="user.id" class="match-card">
        <div class="avatar">
          {{ user.name.charAt(0) }}
        </div>

        <h2>{{ user.name }}, {{ user.age }}</h2>

        <button @click="openChat(user.name)">Message</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.matches-page {
  padding: 30px;
  background: #f4f7fb;
  min-height: 100vh;
  text-align: center;
}

.match-list {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.match-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 220px;
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
  font-weight: bold;
}

button {
  margin-top: 10px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  background: #4a90e2;
  color: white;
  cursor: pointer;
}

.message {
  margin-bottom: 20px;
  color: #1e8449;
}
</style>