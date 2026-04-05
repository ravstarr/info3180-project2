<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <nav class="navbar">
      <div class="logo">DriftDater</div>

      <div class="nav-links">
        <RouterLink to="/discover">Discover</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
        <RouterLink to="/profile">Profile</RouterLink>
        <RouterLink to="/matches">Matches</RouterLink>
      </div>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.navbar {
  background: white;
  padding: 16px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.logo {
  font-size: 1.4rem;
  font-weight: bold;
  color: #4a90e2;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
}

.nav-links a.router-link-active {
  color: #4a90e2;
}

@media (max-width: 600px) {
  .navbar {
    flex-direction: column;
    gap: 12px;
  }
}
</style>