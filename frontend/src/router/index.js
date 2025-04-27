import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: () => import('../views/LandingPage.vue')
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