<script setup>
import { ref } from 'vue'

const profiles = ref([
  {
    id: 1,
    name: 'Alicia',
    age: 22,
    location: 'Kingston',
    interests: ['Music', 'Travel', 'Movies']
  },
  {
    id: 2,
    name: 'Jordan',
    age: 24,
    location: 'Montego Bay',
    interests: ['Football', 'Gym', 'Gaming']
  },
  {
    id: 3,
    name: 'Naomi',
    age: 21,
    location: 'Mandeville',
    interests: ['Reading', 'Nature', 'Photography']
  }
])

const message = ref('')

const like = (name) => {
  message.value = `You liked ${name}`
}

const pass = (name) => {
  message.value = `You passed ${name}`
}
</script>

<template>
  <div class="discover">
    <h1>Discover</h1>

    <p v-if="message" class="message">{{ message }}</p>

    <div class="grid">
      <div v-for="profile in profiles" :key="profile.id" class="card">
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
          <button class="pass" @click="pass(profile.name)">Pass</button>
          <button class="like" @click="like(profile.name)">Like</button>
        </div>
      </div>
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

.message {
  margin-bottom: 20px;
  font-weight: 600;
  color: #1e8449;
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