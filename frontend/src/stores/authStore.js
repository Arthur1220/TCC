import { reactive } from 'vue';
import { getUserProfile } from '@/services/userService';
import { logout as apiLogout } from '@/services/authService';
import { ROLE_ID_MAP } from '@/utils/constants';

export const auth = reactive({
  user: null,
  isAuthenticated: false,
  hasBeenChecked: false, 
});

let authCheckPromise = null;

export function checkAuthentication() {
  if (auth.hasBeenChecked) {
    return Promise.resolve(auth.isAuthenticated);
  }
  if (authCheckPromise) {
    return authCheckPromise;
  }
  authCheckPromise = getUserProfile()
    .then(userProfile => {
      auth.user = userProfile;
      auth.isAuthenticated = true;
      return true;
    })
    .catch(() => {
      auth.user = null;
      auth.isAuthenticated = false;
      return false;
    })
    .finally(() => {
      auth.hasBeenChecked = true;
      authCheckPromise = null;
    });
  return authCheckPromise;
}

export async function logout() {
  try {
    await apiLogout();
  } catch (error) {
    console.error("Erro no logout do servidor, limpando localmente:", error);
  } finally {
    auth.user = null;
    auth.isAuthenticated = false;
    auth.hasBeenChecked = true;
  }
}

export function setAuthenticated(userProfile) {
    auth.user = userProfile;
    auth.isAuthenticated = true;
    auth.hasBeenChecked = true;
}

// === NOVO: Função para simular o login diretamente no frontend ===
export function mockLogin(role = 'Usuário') {
  console.log(`%c[MOCK] A simular login como: ${role}`, 'color: orange; font-weight: bold;');

  const roleId = Object.keys(ROLE_ID_MAP).find(id => ROLE_ID_MAP[id] === role);

  if (!roleId) {
    console.error(`[MOCK] A role '${role}' não é válida. Use 'Usuário', 'Administrador' ou 'Gerente'.`);
    return;
  }

  auth.user = {
    username: `utilizador_${role.toLowerCase()}`,
    email: `${role.toLowerCase()}@animaltracking.com`,
    first_name: 'Utilizador',
    last_name: 'de Teste',
    roles: [{ role: parseInt(roleId) }]
  };
  
  auth.isAuthenticated = true;
  auth.hasBeenChecked = true;
  
  // Recarrega a página para que o router e os componentes reajam ao novo estado
  // É uma forma simples de garantir que tudo é atualizado.
  window.location.reload();
}