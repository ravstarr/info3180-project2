<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()

const isLoggedIn = ref(false)

const checkLogin = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5001/me', {
      credentials: 'include'
    })

    isLoggedIn.value = res.ok
  } catch {
    isLoggedIn.value = false
  }
}

const logout = async () => {
  try {
    await fetch('http://127.0.0.1:5001/logout', {
      method: 'POST',
      credentials: 'include'
    })

    isLoggedIn.value = false
    router.push('/login')
  } catch (err) {
    console.error('Logout failed:', err)
  }
}

onMounted(() => {
  checkLogin()

  router.afterEach(() => {
    checkLogin()
  })
})
</script>

<template>
  <div>
    <nav class="navbar">
      <div class="logo">DriftDater</div>

      <div class="nav-links">
        <RouterLink to="/discover">Discover</RouterLink>

        <template v-if="!isLoggedIn">
          <div class="auth-buttons">
            <RouterLink to="/login" class="login-btn">
              Login
            </RouterLink>
          </div>
        </template>

        <template v-else>
          <RouterLink to="/search">Search</RouterLink>
          <RouterLink to="/profile">Profile</RouterLink>
          <RouterLink to="/matches">Matches</RouterLink>
          <RouterLink to="/favorites">Favorites</RouterLink>
          <RouterLink to="/messages">Messages</RouterLink>
          <button class="logout-btn" @click="logout">Logout</button>
        </template>
      </div>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.navbar {
  background: #fffafa;
  padding: 16px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #1f1f1f;
  box-shadow: 0 4px 10px rgba(232, 93, 117, 0.08);
}

.logo {
  font-size: 1.45rem;
  font-weight: bold;
  color: #d94f70;
  letter-spacing: 0.3px;
}

.nav-links {
  display: flex;
  gap: 18px;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: #3d3d3d;
  font-weight: 500;
  padding: 6px 4px;
}

.nav-links a.router-link-active {
  color: #d94f70;
  border-bottom: 2px solid #d94f70;
}

.logout-btn {
  padding: 7px 13px;
  border: none;
  border-radius: 6px;
  background: #e85d75;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.logout-btn:hover {
  background: #d94f70;
}

@media (max-width: 600px) {
  .navbar {
    flex-direction: column;
    gap: 12px;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 14px;
  }
}
</style>