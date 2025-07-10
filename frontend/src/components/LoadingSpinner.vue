<template>
  <div class="spinner-overlay" :class="{ 'error-state': isError }">
    <div class="spinner"></div>
    <p v-if="message" class="spinner-message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    message: {
      type: String,
      default: 'A carregar...'
    },
    isError: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style scoped>
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(5px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  transition: opacity 0.3s ease;
}

.spinner {
  /* Usando as suas variáveis de cor para consistência */
  border: 5px solid var(--color-primary-light);
  border-top: 5px solid var(--color-primary);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  transition: border-color 0.3s ease;
}

.spinner-message {
  margin-top: 1.5rem;
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
  font-size: var(--fs-large);
}

/* Estado de Erro */
.spinner-overlay.error-state .spinner {
  border-top-color: var(--color-danger);
}
.spinner-overlay.error-state .spinner-message {
  color: var(--color-danger);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>