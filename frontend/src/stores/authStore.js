import { reactive } from 'vue';
import { getUserProfile } from '@/services/userService';
import { logout as apiLogout } from '@/services/authService';

// A nossa store reativa. O nome foi corrigido para 'auth' para consistência.
export const auth = reactive({
  user: null,
  isAuthenticated: false,
  // Flag para saber se a verificação inicial já foi feita.
  hasBeenChecked: false, 
});

// Variável para garantir que a chamada à API só é feita uma vez de cada vez.
let authCheckPromise = null;

/**
 * Verifica a autenticação do utilizador.
 * Utiliza uma "trava" (promise) para evitar múltiplas chamadas à API em simultâneo.
 */
export function checkAuthentication() {
  // Se já sabemos o estado (autenticado ou não), retorna imediatamente.
  if (auth.hasBeenChecked) {
    return Promise.resolve(auth.isAuthenticated);
  }

  // Se uma verificação já estiver em andamento, retorna a promessa dessa verificação.
  if (authCheckPromise) {
    return authCheckPromise;
  }

  // Inicia uma nova verificação.
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
      authCheckPromise = null; // Limpa a trava após a conclusão.
    });

  return authCheckPromise;
}

/**
 * Efetua o logout, limpa o estado local e chama a API.
 */
export async function logout() {
  try {
    await apiLogout();
  } catch (error) {
    console.error("Erro no logout do servidor, limpando localmente de qualquer forma:", error);
  } finally {
    // Limpa o estado local independentemente do resultado da API.
    auth.user = null;
    auth.isAuthenticated = false;
    auth.hasBeenChecked = true; // Agora sabemos o estado (não logado).
  }
}

/**
 * Atualiza o estado local após um login bem-sucedido.
 */
export function setAuthenticated(userProfile) {
    auth.user = userProfile;
    auth.isAuthenticated = true;
    auth.hasBeenChecked = true;
}