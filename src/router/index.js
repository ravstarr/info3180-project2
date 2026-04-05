import { createRouter, createWebHistory } from 'vue-router'
import Discover from '../views/Discover.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import Matches from '../views/Matches.vue'

const routes = [
  {
    path: '/',
    redirect: '/discover'
  },
  {
    path: '/discover',
    component: Discover
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/register',
    component: Register
  },
  {
    path: '/profile',
    component: Profile
  },
  {
    path: '/matches',
    component: Matches
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router