import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: () => import('../views/LandingPage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterPage.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/DashboardPage.vue')
  },
  {
    path: '/search-blockchain',
    name: 'BlockchainSearchPage',
    component: () => import('../views/BlockchainSearchPage.vue')
  },

  { 
    path: '/MVP', 
    name: 'MVP', 
    component: () => import('../views/MVP.vue')
  },
  {
    path: '/MVPContract', 
    name: 'MVPContract', 
    component: () => import('../views/MVPContract.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;