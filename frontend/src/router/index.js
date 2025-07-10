import { createRouter, createWebHistory } from 'vue-router';
import { auth, checkAuthentication } from '@/stores/authStore';
import { showLoader, hideLoader, showError } from '@/stores/uiStore';
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

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth);
  const guestOnly = to.matched.some(r => r.meta.guestOnly);

  // Se a rota não precisa de verificação, continua imediatamente.
  if (!requiresAuth && !guestOnly) {
    return next();
  }

  // Mostra o spinner porque sabemos que uma verificação será necessária.
  showLoader('A verificar credenciais...');
  
  try {
    await checkAuthentication();

    if (requiresAuth) {
      if (auth.isAuthenticated) {
        // Lógica de permissões (roles)
        const requiredRoles = to.meta.roles;
        if (requiredRoles && requiredRoles.length > 0) {
          const userRoles = auth.user.roles.map(r => ROLE_ID_MAP[r.role]).filter(Boolean);
          const hasRequiredRole = userRoles.some(userRole => requiredRoles.includes(userRole));
          return hasRequiredRole ? next() : next({ name: 'LandingPage' });
        }
        return next();
      } else {
        return next({ name: 'Login', query: { redirect: to.fullPath } });
      }
    }

    if (guestOnly) {
      if (auth.isAuthenticated) {
        return next({ name: 'DashboardPage' });
      }
    }

    return next();

  } catch (error) {
    console.error("Erro durante a verificação de autenticação no router:", error);
    showError('Erro de conexão. A redirecionar...');
    // Redireciona para a home em caso de erro na verificação
    setTimeout(() => {
        router.push('/');
    }, 3000);
  }
});

// O afterEach é crucial para esconder o spinner após a navegação bem-sucedida.
router.afterEach(() => {
  hideLoader();
});

// O onError já está a ser tratado dentro do bloco try/catch do beforeEach,
// mas pode ser mantido como uma segurança extra.
router.onError(error => {
    console.error("Erro fatal na navegação:", error);
    showError('Ocorreu um erro inesperado.', 5000);
});

export default router;