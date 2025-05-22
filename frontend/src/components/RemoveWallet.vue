<template>
  <div class="admin-action">
    <h3 class="section-subtitle">Remover Carteira</h3>
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
    <p v-if="message" class="action-message">{{ message }}</p>
  </div>
</template>

<script>
import { removeRegistrar } from '@/services/contractService';
export default {
  name: 'RemoveWallet',
  data() {
    return {
      registrar: '',
      message: ''
    };
  },
  methods: {
    async handleRemove() {
      if (!this.registrar.trim()) {
        this.message = 'Informe o endereço da carteira.';
        return;
      }
      try {
        const res = await removeRegistrar(this.registrar.trim());
        this.message = `Registrador removido: ${res.tx_hash}`;
        this.registrar = '';
      } catch (e) {
        this.message = `Erro ao remover: ${e.error || e}`;
      }
    }
  }
};
</script>

<style scoped>
.admin-action {
  max-width: 400px;
  margin: 0 auto;
}
.section-subtitle {
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.form-section {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.form-group {
  margin-bottom: var(--sp-md);
}
.form-group label {
  display: block;
  margin-bottom: var(--sp-sm);
  color: var(--color-dark-gray);
}
.form-group input {
  width: 100%;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
}
.action-message {
  margin-top: var(--sp-sm);
  text-align: center;
  color: var(--color-secondary);
}
.button-danger {
  display: inline-block;
  padding: var(--sp-md) var(--sp-lg);
  background: #e74c3c;
  color: #fff;
  border: none;
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.2s;
}
.button-danger:hover {
  background: var(--color-primary);
}
</style>
