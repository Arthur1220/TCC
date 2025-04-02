import { createRouter, createWebHistory } from 'vue-router';
import MVP from '../views/MVP.vue';

const routes = [
  { path: '/MVP', name: 'MVP', component: MVP },
  // Adicione outras rotas conforme necessário
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;