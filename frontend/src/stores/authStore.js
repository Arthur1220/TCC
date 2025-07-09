import { reactive } from 'vue';
import { getUserProfile } from '@/services/userService';
import { logout as apiLogout } from '@/services/authService';

// CORREÇÃO: Renomeado para 'auth' e exportado diretamente para consistência
export const auth = reactive({
  user: null,
  isAuthenticated: false,
  // Flag para saber se a verificação inicial já foi feita
  hasBeenChecked: false, 
});

let authCheckPromise = null;

// Função para verificar a autenticação, mas só quando necessário
export function checkAuthentication() {
  // Se já sabemos que o utilizador está autenticado, não fazemos nada
  if (auth.isAuthenticated) return Promise.resolve(true);
  // Se já fizemos a verificação e falhou, não fazemos nada
  if (auth.hasBeenChecked) return Promise.resolve(false);

  // Evita múltiplas chamadas à API em simultâneo
  if (!authCheckPromise) {
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
  }
  return authCheckPromise;
}

// Ação de logout que limpa o estado
export async function logout() {
  try {
    await apiLogout();
  } catch (error) {
    console.error("Erro no logout do servidor, limpando localmente:", error);
  } finally {
    auth.user = null;
    auth.isAuthenticated = false;
    auth.hasBeenChecked = true; // Já sabemos o estado (não logado)
  }
}