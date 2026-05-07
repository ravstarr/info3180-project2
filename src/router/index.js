import { createRouter, createWebHistory } from 'vue-router'
import Discover from '../views/Discover.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import Matches from '../views/Matches.vue'
import Messages from '../views/Messages.vue'
import Search from '../views/Search.vue'


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
  },
  {
  path: '/messages',
  component: Messages
},
{
  path: '/messages/:matchId',
  name: 'messages',
  component: Messages
},
{
  path: '/messages/:matchId',
  component: Messages
},
{
  path: '/search',
  component: Search
}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router