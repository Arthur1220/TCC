import { createRouter, createWebHistory } from 'vue-router'
import { getUserProfile } from '@/services/userService'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: () => import('../views/LandingPage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterPage.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/DashboardPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminPage',
    component: () => import('../views/AdminPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/search-blockchain',
    name: 'BlockchainSearchPage',
    component: () => import('../views/BlockchainSearchPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth)
  const guestOnly    = to.matched.some(r => r.meta.guestOnly)

  // Verifica autenticação
  let isAuth = false
  try {
    await getUserProfile()
    isAuth = true
  } catch {
    isAuth = false
  }

  // Rota protegida mas não logado → Login
  if (requiresAuth && !isAuth) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // Rota para convidados mas já logado → Dashboard
  if (guestOnly && isAuth) {
    return next({ name: 'Dashboard' })
  }

  // Caso normal: aguarda 500ms e só então chama next()
  await new Promise(resolve => setTimeout(resolve, 500))
  next()
})

export default router
