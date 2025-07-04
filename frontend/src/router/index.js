import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'
import AdminHome from '../components/AdminHome.vue'
import AdminUsers from '../components/AdminUsers.vue'
import UserHome from '../components/UserHome.vue'
import Summary from '../components/SummaryPage.vue'
import UserHistory from '../components/UserHistory.vue'
import UserProfile from '../components/UserProfile.vue'

const routes = [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { title: 'Home' }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginForm,
      meta: { title: 'Login Page' }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterForm,
      meta: { title: 'Register Page' }
    },
    {
      path: '/admin_dashboard',
      name: 'admin_dashboard',
      component: AdminDashboard,
      redirect: '/admin_dashboard/home',
      children: [
        {
          path: 'home',
          name: 'admin_home',
          component: AdminHome,
          meta: { title: 'Admin Home' }
        },
        {
          path: 'users',
          name: 'users',
          component: AdminUsers,
          meta: { title: 'Registered Users' }
        },
        {
          path: 'summary',
          name: 'admin_summary',
          component: Summary,
          meta: { title: 'Summary' }
        }
      ]
    },
    {
      path: '/user_dashboard',
      name: 'user_dashboard',
      component: UserDashboard,
      redirect: '/user_dashboard/home',
      children: [
        {
          path: 'home',
          name: 'user_home',
          component: UserHome,
          meta: { title: 'User Home' }
        },
        {
          path: 'history',
          name: 'user_history',
          component: UserHistory,
          meta: { title: 'History' }
        },
        {
          path: 'summary',
          name: 'user_summary',
          component: Summary,
          meta: { title: 'Summary' }
        },
        {
          path: 'profile',
          name: 'user_profile',
          component: UserProfile,
          meta: { title: 'Profile' }
        }
      ]
    }
  ]
  
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Vehicle Parking App'
  next()
})

export default router
