<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Please enter both email and password.'
    return
  }

  try {
    loading.value = true

    const response = await fetch('http://127.0.0.1:5001/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      successMessage.value = 'Login successful! Redirecting...'

      setTimeout(() => {
        window.location.href = '/discover'
      }, 500)
    } else {
      errorMessage.value = data.error || 'Login failed.'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Could not connect to the backend server.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to your DriftDater account</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <label>Email</label>
        <input v-model="email" type="email" placeholder="Enter your email" />

        <label>Password</label>
        <input v-model="password" type="password" placeholder="Enter your password" />

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

        <div class="auth-actions">
          <button type="submit" class="login-button" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>

          <RouterLink to="/register" class="register-link">
            Register
          </RouterLink>
        </div>
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
  background: #fff5f7;
  padding: 32px;
  border-radius: 16px;
  border: 1px solid #1f1f1f;
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
  gap: 14px;
}

label {
  font-weight: 600;
}

input {
  padding: 12px 14px;
  border: 1px solid #1f1f1f;
  border-radius: 10px;
  font-size: 1rem;
}

.auth-actions {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.login-button,
.register-link {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
}

.login-button {
  border: none;
  background-color: #e85d75;
  color: white;
}

.login-button:hover {
  background-color: #d94f70;
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-link {
  text-decoration: none;
  background: white;
  color: #d94f70;
  border: 1px solid #d94f70;
}

.register-link:hover {
  background: #ffe3ea;
}

.error-message {
  color: #c0392b;
}

.success-message {
  color: #1e8449;
}
</style>