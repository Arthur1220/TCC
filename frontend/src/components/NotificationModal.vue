<template>
  <transition name="notification-fade">
    <div v-if="show" :class="['notification-modal', type]">
      <p>{{ message }}</p>
      <button @click="$emit('close')" class="close-button">×</button>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'NotificationModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'success', // 'success' ou 'error'
      validator: (value) => ['success', 'error'].includes(value)
    }
  }
}
</script>

<style scoped>
.notification-modal {
  position: fixed;
  top: 20px; /* Posição no topo da tela */
  right: 20px;
  background-color: var(--color-white);
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  max-width: 350px;
  z-index: 2000; /* Acima de outros modais */
  border-left: 5px solid; /* Borda colorida para tipo */
  animation: slideInFromRight 0.4s ease-out;
}

.notification-modal.success {
  border-color: var(--color-success);
  color: var(--color-success);
}

.notification-modal.error {
  border-color: var(--color-danger);
  color: var(--color-danger);
}

.notification-modal p {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.close-button {
  background: none;
  border: none;
  color: inherit; /* Usa a cor do texto do modal */
  font-size: 1.2rem;
  cursor: pointer;
  padding: 5px;
  line-height: 1;
  transition: transform 0.2s;
}

.close-button:hover {
  transform: rotate(90deg);
}

/* Animações de transição */
.notification-fade-enter-active, .notification-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.notification-fade-enter, .notification-fade-leave-to /* .notification-fade-leave-active in <2.1.8 */ {
  opacity: 0;
  transform: translateX(100%);
}

@keyframes slideInFromRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>