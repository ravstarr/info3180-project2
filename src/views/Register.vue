<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const API_BASE_URL = 'http://127.0.0.1:5000'

const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  location: '',
  interests: ''
})

const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  const {
    name,
    email,
    password,
    confirmPassword,
    age,
    location,
    interests
  } = form.value

  if (
    !name ||
    !email ||
    !password ||
    !confirmPassword ||
    !age ||
    !location ||
    !interests
  ) {
    errorMessage.value = 'Please fill in all fields.'
    return
  }

  if (password !== confirmPassword) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  const interestList = interests
    .split(',')
    .map(item => item.trim())
    .filter(item => item !== '')

  if (interestList.length < 3) {
    errorMessage.value = 'Enter at least 3 interests separated by commas.'
    return
  }

  try {
    // Register User
    const regResponse = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        email,
        password
      })
    })

    const regData = await regResponse.json()

    if (!regResponse.ok) {
      errorMessage.value = regData.error || 'Registration failed.'
      return
    }

    // Login User
    const loginResponse = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        email,
        password
      })
    })

    const loginData = await loginResponse.json()

    if (!loginResponse.ok) {
      errorMessage.value =
        loginData.error ||
        'Registration successful, but login failed.'
      return
    }

    // Create Profile
    const profResponse = await fetch(`${API_BASE_URL}/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        name,
        age: parseInt(age),
        location,
        interests: interestList
      })
    })

    const profData = await profResponse.json()

    if (profResponse.ok) {
      successMessage.value =
        'Account created successfully! Redirecting...'

      setTimeout(() => {
        router.push('/')
      }, 1500)
    } else {
      errorMessage.value =
        profData.error || 'Failed to create profile.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value =
      'An error occurred during registration.'
  }
}
</script>

<template>
  <div class="register-page">
    <div class="register-card">
      <h1>Create Account</h1>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label>Name</label>
          <input
            v-model="form.name"
            type="text"
            placeholder="Enter your name"
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="Enter your email"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Enter password"
          />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input
            v-model="form.confirmPassword"
            type="password"
            placeholder="Confirm password"
          />
        </div>

        <div class="form-group">
          <label>Age</label>
          <input
            v-model="form.age"
            type="number"
            placeholder="Enter your age"
          />
        </div>

        <div class="form-group">
          <label>Location</label>
          <input
            v-model="form.location"
            type="text"
            placeholder="Enter your location"
          />
        </div>

        <div class="form-group">
          <label>Interests</label>
          <input
            v-model="form.interests"
            type="text"
            placeholder="e.g. music, football, movies"
          />
        </div>

        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <p v-if="successMessage" class="success-message">
          {{ successMessage }}
        </p>

        <button type="submit" class="register-button">
          Register
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  padding: 40px 20px;
  display: flex;
  justify-content: center;
}

.register-card {
  width: 100%;
  max-width: 420px;
  background: #fff5f7;
  padding: 30px;
  border-radius: 14px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 6px;
  font-weight: 600;
}

input {
  padding: 11px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
}

.register-button {
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
}

.success-message {
  color: #1e8449;
  font-size: 0.95rem;
}
</style>