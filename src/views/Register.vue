<script setup>
import { ref } from 'vue'

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

const handleRegister = () => {
  errorMessage.value = ''
  successMessage.value = ''

  const { name, email, password, confirmPassword, age, location, interests } = form.value

  if (!name || !email || !password || !confirmPassword || !age || !location || !interests) {
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

  successMessage.value = 'Registration form submitted successfully.'
  console.log('Register data:', {
    ...form.value,
    interests: interestList
  })
}
</script>

<template>
  <div class="register-page">
    <div class="register-card">
      <h1>Create Account</h1>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label>Name</label>
          <input v-model="form.name" type="text" placeholder="Enter your name" />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="Enter your email" />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="Enter password" />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input v-model="form.confirmPassword" type="password" placeholder="Confirm password" />
        </div>

        <div class="form-group">
          <label>Age</label>
          <input v-model="form.age" type="number" placeholder="Enter your age" />
        </div>

        <div class="form-group">
          <label>Location</label>
          <input v-model="form.location" type="text" placeholder="Enter your location" />
        </div>

        <div class="form-group">
          <label>Interests</label>
          <input
            v-model="form.interests"
            type="text"
            placeholder="e.g. music, football, movies"
          />
        </div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

        <button type="submit" class="register-button">Register</button>
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
  background: white;
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
  background-color: #4a90e2;
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