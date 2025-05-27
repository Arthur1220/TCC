<template>
  <div class="pause-contract-panel"> <h2 class="section-title-global with-icon"> <svg v-if="isActive" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M8 5v14l11-7z"/></svg>
      {{ isActive ? 'Pausar Contrato Inteligente' : 'Ativar Contrato Inteligente' }}
    </h2>

    <div class="contract-status-display card"> <p class="status-label">Status Atual do Contrato:</p>
      <p :class="['status-text-prominent', isActive ? 'text-success' : 'text-warning']">
        <span :class="['status-badge', isActive ? 'status-active' : 'status-paused']">
          {{ isActive ? 'ATIVO' : 'PAUSADO' }}
        </span>
      </p>
      <p class="action-guidance form-text">
        {{ isActive ? 'Ao pausar, novas interações com o contrato (como registros de eventos e transferências) serão temporariamente bloqueadas. Esta ação é reversível.' : 'Ao ativar, o contrato voltará a aceitar novas interações e registros conforme programado. Certifique-se de que o sistema está pronto para operar.' }}
      </p>
    </div>

    <div class="action-controls">
      <button
        :class="['button button-lg button-block', isActive ? 'button-danger' : 'button-success']"
        @click="confirmToggle"
        :disabled="isSubmitting"
        aria-live="polite"
      >
        <svg v-if="!isSubmitting && isActive" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
        <svg v-if="!isSubmitting && !isActive" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M8 5v14l11-7z"/></svg>
        <svg v-if="isSubmitting" class="button-spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
        <span v-if="isSubmitting">{{ isActive ? 'Pausando Contrato...' : 'Ativando Contrato...' }}</span>
        <span v-else>{{ isActive ? 'Confirmar e Pausar Contrato' : 'Confirmar e Ativar Contrato' }}</span>
      </button>
    </div>

    <NotificationModal
      :show="notification.show"
      :title="notification.title"
      :message="notification.message"
      :type="notification.type"
      @close="closeNotification"
      :auto-close-delay="notification.autoCloseDelay"
    />
  </div>
</template>

<script>
import { pauseContract, unpauseContract, checkContractStatus } from '@/services/contractService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'PauseContract',
  components: {
    NotificationModal
  },
  props: {
    isActive: { type: Boolean, required: true }
  },
  emits: ['update:active'],
  data() {
    return {
      isSubmitting: false,
      notification: {
        show: false,
        title: '',
        message: '',
        type: 'success',
        autoCloseDelay: 4000 // Padrão para notificações
      }
    };
  },
  methods: {
    showAppNotification(title, message, type = 'success', duration = 4000) {
      this.notification.title = title;
      this.notification.message = message;
      this.notification.type = type;
      this.notification.autoCloseDelay = duration;
      this.notification.show = true;
    },
    closeNotification() {
      this.notification.show = false;
    },
    confirmToggle() {
        const actionText = this.isActive ? 'PAUSAR' : 'ATIVAR';
        const confirmationMessage = `ATENÇÃO: Você está prestes a ${actionText} o contrato inteligente principal da plataforma.\n\n` +
                                    (this.isActive 
                                        ? 'Isso impedirá todas as novas transações de registro de eventos e outras interações críticas até que seja reativado.'
                                        : 'Isso permitirá que todas as operações do contrato sejam retomadas normalmente.') +
                                    `\n\nTem certeza que deseja prosseguir?`;
        
        if (window.confirm(confirmationMessage)) {
            this.toggleContractState();
        }
    },
    async toggleContractState() {
      this.isSubmitting = true;
      this.closeNotification(); // Fecha notificações anteriores

      try {
        let successMessage = '';
        let operationTitle = 'Operação no Contrato';
        if (this.isActive) {
          await pauseContract();
          this.$emit('update:active', false);
          successMessage = 'O contrato inteligente foi PAUSADO com sucesso. Novas transações de registro estão bloqueadas.';
          operationTitle = 'Contrato Pausado';
        } else {
          await unpauseContract();
          this.$emit('update:active', true);
          successMessage = 'O contrato inteligente foi ATIVADO com sucesso. As operações foram normalizadas.';
          operationTitle = 'Contrato Ativado';
        }
        this.showAppNotification(operationTitle, successMessage, 'success');
      } catch (e) {
        console.error(`Erro ao ${this.isActive ? 'pausar' : 'ativar'} contrato:`, e.response?.data || e);
        const actionTerm = this.isActive ? 'pausar' : 'ativar';
        const errorMessageContent = e?.response?.data?.error || e?.error || e?.message || 'Ocorreu um erro desconhecido.';
        this.showAppNotification(
            `Falha ao ${actionTerm} Contrato`,
            `Não foi possível ${actionTerm} o contrato: ${errorMessageContent}`,
            'error'
        );
        this.recheckContractStatus(); // Tenta sincronizar o estado visual com o real do contrato
      } finally {
        this.isSubmitting = false;
      }
    },
    async recheckContractStatus() {
        try {
            const { active } = await checkContractStatus();
            if (this.isActive !== active) { // Só emite se houver mudança real para evitar loops
                this.$emit('update:active', active);
            }
        } catch (error) {
            console.error("Falha ao re-verificar status do contrato:", error.response?.data || error);
            // Poderia mostrar uma notificação discreta se a re-verificação falhar
        }
    }
  }
};
</script>

<style scoped>
/* Estilos Globais e Variáveis CSS são primários */
.pause-contract-panel {
  /* O padding e o estilo de card virão do elemento <section class="card form-section"> na AdminPage.vue */
  /* Este componente agora apenas preenche esse card. */
  text-align: center; /* Centraliza o conteúdo dentro do painel */
}

.section-title-global.with-icon { /* Reutilizando .section-title-global */
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-sm);
  margin-bottom: var(--sp-xl); /* Mais espaço abaixo do título principal */
}
.section-title-global.with-icon svg {
  color: var(--color-primary); /* Ícone do título na cor primária */
}


.contract-status-display {
  /* Aplicando .card para esta seção de status */
  padding: var(--sp-lg);
  margin-bottom: var(--sp-xl);
  background-color: var(--color-bg-muted); /* Fundo sutil para destacar */
  border-left: 5px solid; /* Borda lateral colorida baseada no status */
}
.contract-status-display.status-active-border { border-left-color: var(--color-success); }
.contract-status-display.status-paused-border { border-left-color: var(--color-warning); }

.status-label {
    font-size: var(--fs-base);
    color: var(--color-text-secondary);
    margin-bottom: var(--sp-xs);
    font-weight: var(--fw-medium);
}
.status-text-prominent {
    font-size: var(--fs-h4); /* Tamanho grande para o status */
    font-weight: var(--fw-bold);
    margin-bottom: var(--sp-md);
    display: flex;
    align-items: center;
    justify-content: center;
}
.status-text-prominent .status-badge {
    font-size: var(--fs-h5); /* Badge um pouco menor que o texto */
    padding: var(--sp-xs) var(--sp-md);
    margin-left: 0; /* Removido margin-left, pois está centralizado */
}
.text-success { color: var(--color-success); }
.text-warning { color: var(--color-warning); }


.action-description { /* Herda de .form-text global */
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: 0; /* Removido, pois o status-display já tem margin-bottom */
}

.action-controls {
    margin-top: var(--sp-xl); /* Espaço acima do botão de ação */
}
.confirmation-prompt {
    font-size: var(--fs-base);
    color: var(--color-text-secondary);
    margin-bottom: var(--sp-md);
    font-style: italic;
}

.button { /* Estilos de botão globais */
  /* O botão já usa .button .button-lg .button-block e .button-danger/.button-success */
  display: inline-flex; /* Para alinhar ícone e texto no botão */
  align-items: center;
  justify-content: center;
  gap: var(--sp-sm);
}
.button-spinner { /* Spinner para o botão */
  animation: rotate 0.8s linear infinite; /* Animação mais rápida para botão */
  width: 20px;
  height: 20px;
  /* stroke: currentColor; Se o SVG for stroke-based */
}
.button-spinner .path {
  stroke: currentColor; /* Usa a cor do texto do botão */
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}
/* Keyframes rotate e dash já definidos no global ou em outro componente */


/* Badges de Status (já definidos no global style.css ou outro componente) */
/*
.status-badge {
  font-weight: var(--fw-semibold);
  padding: var(--sp-xxs) var(--sp-sm);
  border-radius: var(--border-radius-pill);
  color: var(--color-text-inverted);
  text-transform: uppercase;
  font-size: var(--fs-small);
}
.status-active { background-color: var(--color-success); }
.status-paused { background-color: var(--color-warning); color: var(--color-text-primary); }
*/
</style>