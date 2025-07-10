import { reactive } from 'vue';

export const uiState = reactive({
  isLoading: false,
  message: 'A carregar...',
  isError: false,
});

export function showLoader(message = 'A carregar...') {
  uiState.isLoading = true;
  uiState.isError = false;
  uiState.message = message;
}

export function hideLoader() {
  uiState.isLoading = false;
}

export function showError(message = 'Ocorreu um erro.', duration = 4000) {
  uiState.isLoading = true; // Mantém o overlay visível
  uiState.isError = true;
  uiState.message = message;
  
  // Esconde a mensagem de erro e o spinner após um tempo
  setTimeout(() => {
    hideLoader();
  }, duration);
}