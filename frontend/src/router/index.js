// src/router/index.js
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

// GUARDA DE NAVEGAÇÃO OTIMIZADO
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth);
  const guestOnly = to.matched.some(r => r.meta.guestOnly);

  // CASO 1: A rota é pública (não precisa de autenticação nem é só para convidados)
  if (!requiresAuth && !guestOnly) {
    return next(); // Permite acesso imediato. Rápido!
  }

  // CASO 2: A rota requer autenticação
  if (requiresAuth) {
    await checkAuthentication(); // Chama a API APENAS se necessário
    if (auth.isAuthenticated) {
      // Lógica de permissões (roles)
      const requiredRoles = to.meta.roles;
      if (requiredRoles && requiredRoles.length > 0) {
        const userRoles = auth.user.roles.map(r => ROLE_ID_MAP[r.role]).filter(Boolean);
        const hasRequiredRole = userRoles.some(userRole => requiredRoles.includes(userRole));
        return hasRequiredRole ? next() : next({ name: 'LandingPage' }); // Redireciona se não tiver permissão
      }
      return next(); // Permissão OK
    } else {
      return next({ name: 'Login', query: { redirect: to.fullPath } }); // Redireciona para o login
    }
  }
  
  // CASO 3: A rota é apenas para convidados (login/registo)
  if (guestOnly) {
      await checkAuthentication();
      if (auth.isAuthenticated) {
          // Se já está logado, não pode ver a página de login
          return next({ name: 'DashboardPage' }); 
      }
      return next();
  }
});

export default router;