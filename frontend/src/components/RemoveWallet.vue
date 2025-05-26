<template>
  <div>
    <div class="admin-action">
      <div class="card">
        <h3 class="section-subtitle">
          Remover Carteira
        </h3>
        <form @submit.prevent="handleRemove" class="form-section">
          <div class="form-group">
            <label for="del-registrar">Endereço da Carteira:</label>
            <input
              id="del-registrar"
              v-model="registrar"
              type="text"
              placeholder="0x..."
              required
            />
          </div>
          <button type="submit" class="button-danger">Remover</button>
        </form>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div
        class="modal-content"
        :class="message.startsWith('Erro') ? 'error' : 'success'"
      >
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import { removeRegistrar } from '@/services/contractService';
export default {
  name: 'RemoveWallet',
  data() {
    return {
      registrar: '',
      message: '',
      showModal: false
    };
  },
  methods: {
    async handleRemove() {
      if (!this.registrar.trim()) {
        this.showFeedback('Informe o endereço da carteira.', true);
        return;
      }
      try {
        const res = await removeRegistrar(this.registrar.trim());
        this.registrar = '';
        this.showFeedback(`✔️ Registrador removido: ${res.tx_hash}`, false);
      } catch (e) {
        this.showFeedback(`Erro ao remover: ${e.error || e}`, true);
      }
    },
    showFeedback(msg, isError) {
      this.message = msg;
      this.showModal = true;
      setTimeout(() => {
        this.showModal = false;
        this.message = '';
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
  max-width: 500px;
  background: var(--color-white);
  border: none;
  border-radius: var(--sp-sm);
  padding: var(--sp-lg);
  transform: none;
  transition: none; /* Opcional: remove a transição para esse card específico */
}
.card:hover, .card:focus-within {
  box-shadow: none; /* Use o box-shadow padrão ou none */
  transform: none; /* Remove o efeito de levantar */
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
.form-section {
  display: flex;
  flex-direction: column;
}
.form-group {
  margin-bottom: var(--sp-md);
}
.form-group label {
  display: block;
  margin-bottom: var(--sp-xs);
  color: var(--color-dark-gray);
}
.form-group input {
  width: 100%;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  transition: border-color 0.2s;
}
.form-group input:focus {
  border-color: var(--color-primary);
  outline: none;
}
.button-danger {
  background: #e74c3c;
  color: #fff;
  border: 2px solid #e74c3c;
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-danger:hover,
.button-danger:focus {
  background-color: var(--color-bg);
  color: #e74c3c;
  outline: none;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
  font-size: var(--font-size-base);
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
