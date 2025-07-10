import { createRouter, createWebHistory } from 'vue-router';
import { auth, checkAuthentication } from '@/stores/authStore';
import { ROLE_ID_MAP } from '@/utils/constants'; 

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
    name: 'DashboardPage',
    component: () => import('../views/DashboardPage.vue'),
    meta: { requiresAuth: true, roles: ['Usuário'] }
  },
  {
    path: '/admin',
    name: 'AdminPage',
    component: () => import('../views/AdminPage.vue'),
    meta: { requiresAuth: true, roles: ['Administrador', 'Gerente'] }
  },
  {
    path: '/search-blockchain',
    name: 'BlockchainSearchPage',
    component: () => import('../views/BlockchainSearchPage.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// GUARDA DE NAVEGAÇÃO OTIMIZADO E CORRIGIDO
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth);
  const guestOnly = to.matched.some(r => r.meta.guestOnly);

  // Se a rota requer autenticação, esta é a única vez que esperamos pela verificação.
  if (requiresAuth) {
    await checkAuthentication();
    
    if (auth.isAuthenticated) {
      // Lógica de permissões (roles)
      const requiredRoles = to.meta.roles;
      if (requiredRoles && requiredRoles.length > 0) {
        const userRoles = auth.user.roles.map(r => ROLE_ID_MAP[r.role]).filter(Boolean);
        const hasRequiredRole = userRoles.some(userRole => requiredRoles.includes(userRole));
        
        // Se o utilizador não tiver a permissão, redireciona para uma página segura (ex: landing page)
        return hasRequiredRole ? next() : next({ name: 'LandingPage' });
      }
      return next(); // Permissão OK
    } else {
      // Se não estiver autenticado, redireciona para o login
      return next({ name: 'Login', query: { redirect: to.fullPath } });
    }
  }

  // Para rotas de convidado, verificamos a autenticação para redirecionar se já estiver logado.
  if (guestOnly) {
    await checkAuthentication();
    if (auth.isAuthenticated) {
      return next({ name: 'DashboardPage' }); // Redireciona para o painel principal
    }
  }

  // Para todas as outras rotas públicas, permite o acesso imediato.
  return next();
});

export default router;