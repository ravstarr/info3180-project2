<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const handleLogin = () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Please enter both email and password.'
    return
  }

  successMessage.value = 'Login form submitted successfully.'
  console.log('Login data:', {
    email: email.value,
    password: password.value
  })
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to your DriftDater account</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
          />
        </div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

        <button type="submit" class="login-button">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  padding: 40px 20px;
  display: flex;
  justify-content: center;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

h1 {
  margin: 0 0 8px;
  font-size: 2rem;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 24px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 8px;
  font-weight: 600;
}

input {
  padding: 12px 14px;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
}

.login-button {
  padding: 12px;
  border: none;
  border-radius: 10px;
  background-color: #4a90e2;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.login-button:hover {
  opacity: 0.95;
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