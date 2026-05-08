<script setup>
import { ref, onMounted } from 'vue'

const API_BASE_URL = 'http://127.0.0.1:5001'

const profile = ref({
  name: '',
  age: 0,
  location: '',
  bio: '',
  interests: '',
  profile_pic_url: ''
})

const message = ref('')
const errorMessage = ref('')
const loading = ref(false)

const getProfilePhoto = () => {
  if (!profile.value.profile_pic_url) return null
  return `${API_BASE_URL}/uploads/${profile.value.profile_pic_url}`
}

const loadProfile = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}/me`, {
      credentials: 'include'
    })

    const data = await response.json()

    if (response.ok && data.profile) {
      profile.value = {
        name: data.profile.name || '',
        age: data.profile.age || 0,
        location: data.profile.location || '',
        bio: data.profile.bio || '',
        interests: Array.isArray(data.profile.interests)
          ? data.profile.interests.join(', ')
          : data.profile.interests || '',
        profile_pic_url: data.profile.profile_pic_url || ''
      }
    } else if (response.status === 401) {
      errorMessage.value = 'Please login to view your profile.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to backend.'
  } finally {
    loading.value = false
  }
}

const uploadPhoto = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  message.value = ''
  errorMessage.value = ''

  const formData = new FormData()
  formData.append('photo', file)

  try {
    const response = await fetch(`${API_BASE_URL}/profile/photo`, {
      method: 'POST',
      credentials: 'include',
      body: formData
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message || 'Photo uploaded successfully.'
      await loadProfile()
    } else {
      errorMessage.value = data.error || 'Failed to upload photo.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not upload photo.'
  }
}

const saveProfile = async () => {
  message.value = ''
  errorMessage.value = ''

  const interestList = profile.value.interests
    .split(',')
    .map(i => i.trim())
    .filter(i => i !== '')

  try {
    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        name: profile.value.name,
        age: Number(profile.value.age),
        location: profile.value.location,
        bio: profile.value.bio,
        interests: interestList
      })
    })

    const data = await response.json()

    if (response.ok) {
      message.value = 'Profile updated successfully.'
      await loadProfile()
    } else {
      errorMessage.value = data.error || 'Failed to update profile.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'An error occurred while saving.'
  }
}

onMounted(loadProfile)
</script>

<template>
  <div class="profile-page">
    <div class="profile-card">
      <h1>My Profile</h1>

      <p v-if="loading">Loading profile...</p>

      <div class="photo-section">
        <img
          v-if="getProfilePhoto()"
          :src="getProfilePhoto()"
          alt="Profile photo"
          class="profile-photo"
        />

        <div v-else class="avatar">
          {{ profile.name?.charAt(0) || '?' }}
        </div>

        <label class="upload-label">
          Upload Profile Picture
          <input
            type="file"
            accept="image/*"
            @change="uploadPhoto"
          />
        </label>
      </div>

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
        <input
          v-model="profile.interests"
          type="text"
          placeholder="music, movies, football"
        />
      </div>

      <p v-if="message" class="success-message">{{ message }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <button @click="saveProfile" class="save-button">
        Save Profile
      </button>

      <hr />

      <h2>Profile Preview</h2>

      <div class="preview-card">
        <img
          v-if="getProfilePhoto()"
          :src="getProfilePhoto()"
          alt="Profile photo"
          class="preview-photo"
        />

        <div v-else class="avatar">
          {{ profile.name?.charAt(0) || '?' }}
        </div>

        <h3>{{ profile.name }}, {{ profile.age }}</h3>
        <p class="location">{{ profile.location }}</p>
        <p class="bio">{{ profile.bio }}</p>

        <div class="interests">
          <span
            v-for="i in profile.interests.split(',').filter(i => i.trim() !== '')"
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
  background: #fff5f7;
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

.photo-section {
  text-align: center;
  margin-bottom: 20px;
}

.avatar,
.profile-photo,
.preview-photo {
  width: 80px;
  height: 80px;
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

.profile-photo,
.preview-photo {
  object-fit: cover;
  display: block;
}

.upload-label {
  display: inline-block;
  padding: 9px 12px;
  background: #eef4ff;
  background: #e85d75;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.upload-label input {
  display: none;
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
  background: #e85d75;
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