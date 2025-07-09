// src/stores/authStore.js
import { reactive } from 'vue';
import { getUserProfile } from '@/services/userService';

// O nosso repositório de estado reativo.
// Começa como indefinido, para sabermos que ainda não verificámos.
export const authStore = reactive({
  user: null,
  isAuthenticated: false,
  isStateKnown: false, // <-- A nossa nova flag de controlo
});

// A nossa ação para inicializar o estado
export async function initializeAuth() {
  // Se já conhecemos o estado, não fazemos nada.
  if (authStore.isStateKnown) {
    return;
  }

  try {
    // Faz a chamada à API APENAS UMA VEZ.
    const userProfile = await getUserProfile();
    authStore.user = userProfile;
    authStore.isAuthenticated = true;
    console.log("%c[AuthStore] Estado inicializado: Utilizador AUTENTICADO", 'color: #28a745');
  } catch (error) {
    // Se falhar, sabemos que não está autenticado.
    authStore.user = null;
    authStore.isAuthenticated = false;
    console.warn("[AuthStore] Estado inicializado: Utilizador NÃO AUTENTICADO");
  } finally {
    // Marcamos que o estado já é conhecido, para que esta função não volte a fazer a chamada à API.
    authStore.isStateKnown = true;
  }
}

// Ação para limpar o estado no logout
export function clearAuth() {
    authStore.user = null;
    authStore.isAuthenticated = false;
    authStore.isStateKnown = true; // Já sabemos o estado (não logado)
}