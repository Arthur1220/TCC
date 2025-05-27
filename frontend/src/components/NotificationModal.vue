<template>
  <transition :name="animationType">
    <div v-if="show" :class="['notification-toast', `toast-${type}`]" role="alert" aria-live="assertive">
      <div class="toast-icon-content-wrapper">
        <div v-if="type === 'success'" class="toast-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>
        </div>
        <div v-else-if="type === 'error'" class="toast-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
        </div>
         <div v-else-if="type === 'warning'" class="toast-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
        </div>
        <div v-else class="toast-icon"> <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M11 7h2v2h-2V7zm0 4h2v6h-2v-6zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
        </div>
        <div class="toast-content">
            <div v-if="title" class="toast-title">{{ title }}</div>
            <div class="toast-message">{{ message }}</div>
        </div>
      </div>
      <button @click="close" class="toast-close-button" aria-label="Fechar Notificação">&times;</button>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'NotificationModal',
  props: {
    show: { type: Boolean, default: false },
    title: { type: String, default: '' },
    message: { type: String, default: '' },
    type: {
      type: String, default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    autoCloseDelay: { type: Number, default: 4000 },
    animationType: { type: String, default: 'slide-in-from-right' }
  },
  emits: ['close'],
  watch: {
    show(newVal) {
      if (this.closeTimer) clearTimeout(this.closeTimer);
      if (newVal && this.autoCloseDelay !== null && this.autoCloseDelay > 0) {
        this.closeTimer = setTimeout(() => {
          this.close();
        }, this.autoCloseDelay);
      }
    }
  },
  data() {
      return {
          closeTimer: null
      };
  },
  methods: {
    close() {
      if (this.closeTimer) clearTimeout(this.closeTimer);
      this.$emit('close');
    }
  },
  beforeUnmount() {
      if (this.closeTimer) clearTimeout(this.closeTimer);
  }
}
</script>

<style scoped>
/* Estilos para NotificationModal como um TOAST no canto superior direito */
.notification-toast {
  position: fixed;
  top: var(--sp-lg, 1.5rem);
  right: var(--sp-lg, 1.5rem);
  background-color: var(--color-bg-component);
  padding: var(--sp-md, 1rem);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-sm);
  width: auto;
  min-width: 300px;
  max-width: 450px;
  z-index: var(--zindex-tooltip, 2000); /* Z-index alto para ficar sobre outros elementos */
  border-left: 5px solid;
  color: var(--color-text-primary);
}

.toast-icon-content-wrapper {
    display: flex;
    align-items: flex-start;
    gap: var(--sp-sm);
    flex-grow: 1;
}
.toast-icon svg {
    flex-shrink: 0;
    margin-top: 2px;
}

.toast-content { flex-grow: 1; }
.toast-title {
    font-family: var(--font-heading);
    font-size: var(--fs-base);
    font-weight: var(--fw-semibold);
    margin-bottom: var(--sp-xs);
    line-height: 1.3;
}
.toast-message {
  margin: 0;
  font-size: var(--fs-base);
  line-height: 1.5;
  color: var(--color-text-secondary);
}

.toast-close-button {
  background: none; border: none;
  color: var(--color-text-muted);
  font-size: var(--fs-large);
  font-weight: var(--fw-light);
  cursor: pointer;
  padding: 0 var(--sp-xxs);
  line-height: 1;
  align-self: flex-start;
  margin-top: -2px; /* Ajuste fino */
}
.toast-close-button:hover { color: var(--color-text-primary); }

.toast-success { border-left-color: var(--color-success); }
.toast-success .toast-title, .toast-success .toast-icon svg { color: var(--color-success); }

.toast-error { border-left-color: var(--color-danger); }
.toast-error .toast-title, .toast-error .toast-icon svg { color: var(--color-danger); }

.toast-warning { border-left-color: var(--color-warning); }
.toast-warning .toast-title, .toast-warning .toast-icon svg { color: var(--color-warning); }
.toast-warning .toast-message { color: var(--color-text-primary); }

.toast-info { border-left-color: var(--color-info); }
.toast-info .toast-title, .toast-info .toast-icon svg { color: var(--color-info); }

/* Animações */
.slide-in-from-right-enter-active,
.slide-in-from-right-leave-active {
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.slide-in-from-right-enter-from,
.slide-in-from-right-leave-to {
  opacity: 0;
  transform: translateX(calc(100% + var(--sp-lg, 1.5rem)));
}
.slide-in-from-right-enter-to,
.slide-in-from-right-leave-from {
  opacity: 1;
  transform: translateX(0);
}
</style>