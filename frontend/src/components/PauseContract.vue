<template>
  <div class="admin-action">
    <div class="card">
      <h3 class="section-subtitle">
        <span class="icon">⏸️</span>
        {{ isActive ? 'Pausar Contrato' : 'Ativar Contrato' }}
      </h3>
      <button
        class="button-primary"
        @click="toggle"
      >
        {{ isActive ? 'Pausar' : 'Ativar' }}
      </button>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div
        class="modal-content"
        :class="modalError ? 'error' : 'success'"
      >
        {{ modalMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { pauseContract, unpauseContract } from '@/services/contractService';

export default {
  name: 'PauseContract',
  props: {
    isActive: { type: Boolean, required: true }
  },
  data() {
    return {
      showModal: false,
      modalMessage: '',
      modalError: false
    };
  },
  methods: {
    async toggle() {
      try {
        if (this.isActive) {
          await pauseContract();
          this.$emit('update:active', false);
          this.showFeedback('✔️ Contrato pausado com sucesso.', false);
        } else {
          await unpauseContract();
          this.$emit('update:active', true);
          this.showFeedback('✔️ Contrato ativado com sucesso.', false);
        }
      } catch (e) {
        this.showFeedback(`Erro: ${e.error || e}`, true);
      }
    },
    showFeedback(msg, isError) {
      this.modalMessage = msg;
      this.modalError = isError;
      this.showModal = true;
      setTimeout(() => {
        this.showModal = false;
      }, 3000);
    }
  }
};
</script>

<style scoped>
.admin-action {
  display: flex;
  justify-content: center;
  padding: var(--sp-lg) 0;
}
.card {
  width: 100%;
  max-width: 400px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  padding: var(--sp-lg);
  text-align: center;
}
.section-subtitle {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.section-subtitle .icon {
  margin-right: var(--sp-sm);
  font-size: 1.2rem;
}
.button-primary {
  padding: var(--sp-sm) var(--sp-lg);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  font-family: var(--font-heading);
  text-align: center;
  max-width: 80%;
}
.modal-content.success {
  border: 2px solid #27ae60;
  color: #27ae60;
}
.modal-content.error {
  border: 2px solid #e74c3c;
  color: #e74c3c;
}
</style>
