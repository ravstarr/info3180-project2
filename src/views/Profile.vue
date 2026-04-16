<script setup>
import { ref, onMounted } from 'vue'

const profile = ref({
  name: '',
  age: 0,
  location: '',
  bio: '',
  interests: ''
})

const message = ref('')
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await fetch('/api/me')
    if (response.ok) {
      const data = await response.json()
      if (data.profile) {
        profile.value = {
          ...data.profile,
          interests: (data.profile.interests || []).join(', ')
        }
      }
    } else if (response.status === 401) {
      errorMessage.value = 'Please login to view your profile.'
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
})

const saveProfile = async () => {
  message.value = ''
  errorMessage.value = ''
  
  const interestList = profile.value.interests
    .split(',')
    .map(i => i.trim())
    .filter(i => i !== '')

  try {
    const response = await fetch('/api/profile', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...profile.value,
        interests: interestList
      })
    })

    if (response.ok) {
      message.value = 'Profile updated successfully.'
    } else {
      const data = await response.json()
      errorMessage.value = data.error || 'Failed to update profile.'
    }
  } catch (error) {
    errorMessage.value = 'An error occurred while saving.'
    console.error(error)
  }
}
</script>

<template>
  <div class="profile-page">
    <div class="profile-card">
      <h1>My Profile</h1>

      <div class="form-group">
        <label>Name</label>
        <input v-model="profile.name" type="text" />
      </div>

      <div class="form-group">
        <label>Age</label>
        <input v-model="profile.age" type="number" />
      </div>

      <div class="form-group">
        <label>Location</label>
        <input v-model="profile.location" type="text" />
      </div>

      <div class="form-group">
        <label>Bio</label>
        <textarea v-model="profile.bio" rows="4"></textarea>
      </div>

      <div class="form-group">
        <label>Interests</label>
        <input v-model="profile.interests" type="text" />
      </div>

      <p v-if="message" class="success-message">{{ message }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <button @click="saveProfile" class="save-button">Save Profile</button>

      <hr />

      <h2>Profile Preview</h2>

      <div class="preview-card">
        <div class="avatar">
          {{ profile.name.charAt(0) }}
        </div>

        <h3>{{ profile.name }}, {{ profile.age }}</h3>
        <p class="location">{{ profile.location }}</p>
        <p class="bio">{{ profile.bio }}</p>

        <div class="interests">
          <span
            v-for="i in profile.interests.split(',')"
            :key="i"
            class="tag"
          >
            {{ i.trim() }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  background-color: #f4f7fb;
  min-height: 100vh;
}

.profile-card {
  width: 100%;
  max-width: 500px;
  background: white;
  padding: 30px;
  border-radius: 14px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

h2 {
  text-align: center;
  margin: 20px 0 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

label {
  margin-bottom: 6px;
  font-weight: 600;
}

input,
textarea {
  padding: 11px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #4a90e2;
}

.save-button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background-color: #4a90e2;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.error-message {
  color: #c0392b;
  font-size: 0.95rem;
  margin-bottom: 12px;
}

.success-message {
  color: #1e8449;
  font-size: 0.95rem;
  margin-bottom: 12px;
}

hr {
  margin: 24px 0;
  border: none;
  border-top: 1px solid #ddd;
}

.preview-card {
  padding: 20px;
  border-radius: 12px;
  background: #f9fbff;
  text-align: center;
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

.location {
  color: #777;
}

.bio {
  margin: 10px 0;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.tag {
  background: #eef4ff;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
}
</style>