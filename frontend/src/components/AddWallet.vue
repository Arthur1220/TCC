<template>
  <div class="admin-action-card"> <div class="card">
      <h3 class="card-title-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-3h-2v2H12v-2H10v-2h2V9h2v2h2v2z"/></svg>
        Registrar Nova Carteira (Registrador)
      </h3>
      <form @submit.prevent="handleAdd" class="form">
        <div class="form-group">
          <label for="new-registrar-address" class="form-label">Endereço da Carteira Ethereum*</label>
          <input
            id="new-registrar-address"
            v-model="registrarAddress"
            type="text"
            class="input"
            placeholder="Cole o endereço da carteira (ex: 0x...)"
            required
            aria-required="true"
          />
          <p class="form-text">Este endereço será autorizado a registrar eventos na blockchain.</p>
        </div>
        <button type="submit" class="button button-primary button-block" :disabled="isSubmitting">
          <span v-if="isSubmitting">Adicionando...</span>
          <span v-else>Adicionar Carteira</span>
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
import { addRegistrar } from '@/services/contractService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'AddWallet',
  components: {
    NotificationModal
  },
  data() {
    return {
      registrarAddress: '', // Renomeado para clareza
      isSubmitting: false, // Estado de carregamento para o botão
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
    async handleAdd() {
      if (!this.registrarAddress.trim()) {
        this.showAppNotification('Erro de Validação', 'Por favor, informe o endereço da carteira.', 'error');
        return;
      }
      // Adicionar validação simples para formato de endereço Ethereum
      if (!/^0x[a-fA-F0-9]{40}$/.test(this.registrarAddress.trim())) {
          this.showAppNotification('Erro de Validação', 'Formato de endereço de carteira Ethereum inválido.', 'error');
          return;
      }

      this.isSubmitting = true;
      this.closeNotification(); // Fecha notificações anteriores

      try {
        const addressToAdd = this.registrarAddress.trim();
        const res = await addRegistrar(addressToAdd);
        this.registrarAddress = ''; // Limpa o campo
        this.showAppNotification(
          'Sucesso!',
          `Carteira ${addressToAdd.substring(0,6)}...${addressToAdd.substring(addressToAdd.length-4)} adicionada como registrador. Hash da transação: ${res.tx_hash || 'N/A'}`,
          'success'
        );
      } catch (e) {
        console.error('Erro ao adicionar carteira registradora:', e);
        const errorMessage = e?.error || e?.message || e || 'Ocorreu um erro desconhecido.';
        this.showAppNotification('Erro ao Adicionar Carteira', `Não foi possível adicionar a carteira: ${errorMessage}`, 'error');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
/* A classe .admin-action-card é o container principal do componente dentro do grid da AdminPage */

/* O .card global já define background, border-radius, padding base, box-shadow. */
/* Sobrescrevemos apenas o que for necessário para o contexto do admin, se for diferente. */
.admin-action-card .card {
  border: var(--border-width) solid var(--color-border); /* Adiciona uma borda padrão */
  /* Mantém a sombra padrão do .card, remove transform se AdminPage não deve ter cards interativos */
  /* Para remover o efeito de levantar no hover, específico para admin cards: */
  /* transition: none;
  transform: none !important; */
}
/* .admin-action-card .card:hover {
  transform: none !important;
  box-shadow: var(--shadow) !important; /* Mantém a sombra base ou a padrão de card */
/*}*/


.card-title-icon { /* Substitui .section-subtitle */
  display: flex;
  align-items: center;
  gap: var(--sp-sm);
  font-family: var(--font-heading);
  font-size: var(--fs-h5); /* Tamanho apropriado para título de card de ação */
  color: var(--color-text-primary); /* Cor de texto primário */
  margin-bottom: var(--sp-lg); /* Mais espaço abaixo do título */
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) solid var(--color-border-light);
}
.card-title-icon svg {
  color: var(--color-primary); /* Ícone na cor primária */
}

.form { /* Se .form global não existir ou precisar de ajustes */
  display: flex;
  flex-direction: column;
}

/* .form-group, .form-label, .input, .button, .button-primary, .button-block são globais */
.form-text { /* Para texto de ajuda abaixo do input, usar classe global */
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    margin-top: var(--sp-xs);
}

.admin-action-card .button-primary {
    margin-top: var(--sp-md); /* Espaço acima do botão */
}
</style>