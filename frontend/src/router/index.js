import { createRouter, createWebHistory } from 'vue-router';
import MVP from '../views/MVP.vue';
import MVPContract from '../views/MVPContract.vue';

const routes = [
  { path: '/MVP', name: 'MVP', component: MVP },
  {path: '/MVPContract', name: 'MVPContract', component: MVPContract},
  // Adicione outras rotas conforme necessário
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;