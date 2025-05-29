import { createRouter, createWebHistory } from 'vue-router';
import { getUserProfile } from '@/services/userService';
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
    // Definimos quais perfis podem acessar esta rota
    meta: { requiresAuth: true, roles: ['Usuário'] }
  },
  {
    path: '/admin',
    name: 'AdminPage',
    component: () => import('../views/AdminPage.vue'),
    // Definimos quais perfis podem acessar esta rota
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

// GUARDA DE NAVEGAÇÃO GLOBAL ATUALIZADA
router.beforeEach(async (to, from, next) => {
  console.log(`%c[Router Guard] Navegando de '${from.path}' para '${to.path}'`, 'color: blue');
  
  const requiredRoles = to.meta.roles;
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth);
  const guestOnly = to.matched.some(r => r.meta.guestOnly);

  let userIsAuthenticated = false;
  let userProfile = null;

  // A verificação de login agora é uma chamada à API
  try {
    console.log("[Router Guard] Verificando autenticação no backend...");
    userProfile = await getUserProfile();
    userIsAuthenticated = true;
    console.log("%c[Router Guard] Backend confirmou: Usuário está AUTENTICADO.", 'color: green', userProfile);
  } catch (error) {
    userIsAuthenticated = false;
    console.warn("[Router Guard] Backend confirmou: Usuário NÃO está autenticado.");
  }

  // CASO 1: Acessando uma rota "guestOnly" (login/registro)
  if (guestOnly) {
    if (userIsAuthenticated) {
      // Se já está logado, não pode ver o login. Redireciona para a home,
      // que por sua vez o redirecionará para o painel correto.
      console.log("[Router Guard] Usuário logado tentou acessar rota de convidado. Redirecionando para a Home.");
      return next({ path: '/' });
    } else {
      // Se não está logado, pode ver a página de login/registro.
      return next();
    }
  }

  // CASO 2: Acessando uma rota protegida (`requiresAuth: true`)
  if (requiresAuth) {
    if (!userIsAuthenticated) {
      // Se não está logado, redireciona para o login.
      console.warn("[Router Guard] Rota protegida. Usuário não autenticado. Redirecionando para /login.");
      return next({ name: 'Login', query: { redirect: to.fullPath } });
    }
    
    // Se está logado, verifica se tem o perfil (role) necessário
    if (requiredRoles && requiredRoles.length > 0) {
      const userRoles = userProfile.roles
        .map(r => ROLE_ID_MAP[r.role])
        .filter(Boolean); // Garante que não há 'undefined'

      const hasRequiredRole = userRoles.some(userRole => requiredRoles.includes(userRole));

      if (hasRequiredRole) {
        console.log("%c[Router Guard] Permissão de perfil CONCEDIDA.", 'color: green');
        return next(); // Permissão OK
      } else {
        console.warn("%c[Router Guard] Permissão de perfil NEGADA.", 'color: red', { userRoles, requiredRoles });
        // Sem permissão, redireciona para a página principal que ele PODE acessar
        if (userRoles.includes('Administrador') || userRoles.includes('Gerente')) {
          return next({ name: 'AdminPage' });
        }
        if (userRoles.includes('Usuário')) {
          return next({ name: 'Dashboard' });
        }
        // Se não tem perfil válido, desloga (por segurança)
        // A falha na autenticação no próximo ciclo cuidará disso.
        return next({ name: 'Login' });
      }
    }
    
    return next(); // Rota protegida mas sem restrição de perfil, permite acesso
  }

  // CASO 3: Rota pública que não é "guestOnly"
  return next();
});

export default router;
