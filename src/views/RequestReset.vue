<template>
  <div class="auth-container">
    <h2>Reset Password</h2>
    <form @submit.prevent="requestReset">
      <div class="form-group">
        <label>Email Address:</label>
        <input type="email" v-model="email" required />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Requesting...' : 'Request Reset Link' }}
      </button>
    </form>
    <p v-if="message" class="success-msg">{{ message }}</p>
    <p v-if="error" class="error-msg">{{ error }}</p>
    <p class="links">
      <router-link to="/login">Back to Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

const requestReset = async () => {
  loading.value = true
  message.value = ''
  error.value = ''
  try {
    const res = await fetch('/api/auth/request-password-reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })
    const data = await res.json()
    if (res.ok) {
      // In a real app, this would send an email. For demo purposes, we will show the token or advise checking email
      message.value = `Success! Use this token to reset (for demo purposes): ${data.token || 'Check your email'}`
    } else {
      error.value = data.error || data.message || 'An error occurred'
    }
  } catch (err) {
    error.value = 'Failed to connect to the server'
  }
  loading.value = false
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-radius: 8px;
  background: white;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.btn {
  width: 100%;
  padding: 0.8rem;
  background: #ff4b4b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn:disabled {
  background: #ff9999;
}
.success-msg { color: green; margin-top: 1rem; }
.error-msg { color: red; margin-top: 1rem; }
.links { text-align: center; margin-top: 1rem; }
</style>
