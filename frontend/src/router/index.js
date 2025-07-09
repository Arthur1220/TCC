// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { authStore, initializeAuth } from '@/stores/authStore';
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

// GUARDA DE NAVEGAÇÃO OTIMIZADA
router.beforeEach(async (to, from, next) => {
  // 1. Garante que o estado de autenticação foi verificado pelo menos uma vez.
  await initializeAuth();
  
  const { isAuthenticated, user } = authStore;

  const requiresAuth = to.matched.some(r => r.meta.requiresAuth);
  const guestOnly = to.matched.some(r => r.meta.guestOnly);

  // CASO 1: Tentando aceder a uma página de "convidado" (login/registo)
  if (guestOnly && isAuthenticated) {
    // Se já está logado, vai para o dashboard
    return next({ name: 'DashboardPage' });
  }

  // CASO 2: Tentando aceder a uma rota protegida
  if (requiresAuth) {
    if (!isAuthenticated) {
      // Se não está logado, vai para o login
      return next({ name: 'Login', query: { redirect: to.fullPath } });
    }
    
    // Se está logado, verifica as permissões (roles)
    const requiredRoles = to.meta.roles;
    if (requiredRoles && requiredRoles.length > 0) {
      const userRoles = user.roles.map(r => ROLE_ID_MAP[r.role]).filter(Boolean);
      const hasRequiredRole = userRoles.some(userRole => requiredRoles.includes(userRole));
      
      if (hasRequiredRole) {
        return next(); // Permissão OK
      } else {
        // Sem permissão, redireciona para um local seguro (página inicial ou dashboard)
        return next({ name: 'DashboardPage' });
      }
    }
    
    return next(); // Rota protegida sem roles específicos, permite acesso
  }

  // CASO 3: Rota pública
  return next();
});

export default router;