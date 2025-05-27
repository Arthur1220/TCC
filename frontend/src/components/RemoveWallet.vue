<template>
  <div class="admin-action-card">
    <div class="card">
      <h3 class="card-title-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M15 16h4v2h-4v-2zm-8-4h12v2H7v-2zm0-4h12v2H7V8zm14-4H3v2h18V4zM3 20h12v-2H3v2z"/></svg> Remover Carteira (Registrador)
      </h3>
      <form @submit.prevent="handleRemove" class="form">
        <div class="form-group">
          <label for="del-registrar-address" class="form-label">Endereço da Carteira Ethereum*</label>
          <input
            id="del-registrar-address"
            v-model="registrarAddress"
            type="text"
            class="input"
            placeholder="Cole o endereço da carteira a ser removida (ex: 0x...)"
            required
            aria-required="true"
          />
          <p class="form-text">Este endereço não poderá mais registrar eventos na blockchain.</p>
        </div>
        <button type="submit" class="button button-danger button-block" :disabled="isSubmitting">
          <span v-if="isSubmitting">Removendo...</span>
          <span v-else>Remover Carteira</span>
        </button>
      </form>
    </div>

    <NotificationModal
      :show="notification.show"
      :title="notification.title"
      :message="notification.message"
      :type="notification.type"
      @close="closeNotification"
    />
  </div>
</template>

<script>
import { removeRegistrar } from '@/services/contractService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'RemoveWallet',
  components: {
    NotificationModal
  },
  data() {
    return {
      registrarAddress: '', // Renomeado
      isSubmitting: false,
      notification: {
        show: false,
        title: '',
        message: '',
        type: 'success'
      }
    };
  },
  methods: {
    showAppNotification(title, message, type = 'success') {
      this.notification.title = title;
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
    },
    closeNotification() {
      this.notification.show = false;
    },
    async handleRemove() {
      if (!this.registrarAddress.trim()) {
        this.showAppNotification('Erro de Validação', 'Por favor, informe o endereço da carteira.', 'error');
        return;
      }
      if (!/^0x[a-fA-F0-9]{40}$/.test(this.registrarAddress.trim())) {
          this.showAppNotification('Erro de Validação', 'Formato de endereço de carteira Ethereum inválido.', 'error');
          return;
      }

      this.isSubmitting = true;
      this.closeNotification();

      // Adicionar uma confirmação extra para ações destrutivas
      if (!confirm(`Tem certeza que deseja remover a carteira ${this.registrarAddress.trim()} da lista de registradores? Esta ação não pode ser desfeita.`)) {
          this.isSubmitting = false;
          return;
      }

      try {
        const addressToRemove = this.registrarAddress.trim();
        const res = await removeRegistrar(addressToRemove);
        this.registrarAddress = '';
        this.showAppNotification(
          'Sucesso!',
          `Carteira ${addressToRemove.substring(0,6)}...${addressToRemove.substring(addressToRemove.length-4)} removida da lista de registradores. Hash da transação: ${res.tx_hash || 'N/A'}`,
          'success'
        );
      } catch (e) {
        console.error('Erro ao remover carteira registradora:', e);
        const errorMessage = e?.error || e?.message || e || 'Ocorreu um erro desconhecido.';
        this.showAppNotification('Erro ao Remover Carteira', `Não foi possível remover a carteira: ${errorMessage}`, 'error');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
/* Estilos são muito similares ao AddWallet.vue, podem ser compartilhados ou herdados. */
.admin-action-card .card {
  border: var(--border-width) solid var(--color-border);
}

.card-title-icon {
  display: flex;
  align-items: center;
  gap: var(--sp-sm);
  font-family: var(--font-heading);
  font-size: var(--fs-h5);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-lg);
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) solid var(--color-border-light);
}
.card-title-icon svg {
  color: var(--color-danger); /* Ícone na cor de perigo */
}

.form {
  display: flex;
  flex-direction: column;
}

.form-text {
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    margin-top: var(--sp-xs);
}

.admin-action-card .button-danger { /* Garante que o botão de remover use o estilo de perigo */
    margin-top: var(--sp-md);
}
</style>