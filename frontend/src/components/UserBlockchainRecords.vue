<template>
  <div class="user-blockchain-records-panel content-panel"> <div class="panel-header">
      <h2 class="panel-title-text">Meus Registros na Blockchain</h2>
    </div>
    <p class="panel-description">
      Consulte o histórico imutável dos eventos dos seus animais registrados em nossa blockchain, garantindo transparência e auditabilidade.
    </p>

    <div v-if="isLoading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>Carregando seus registros da blockchain...</p>
    </div>
    <div v-else-if="errorLoading" class="empty-state card alert alert-danger"> <h4 class="alert-heading">Erro ao Carregar Registros</h4>
      <p>Não foi possível buscar seus registros da blockchain no momento.</p>
      <p>{{ errorMessage || 'Por favor, tente novamente mais tarde.' }}</p>
      <button @click="loadUserRecords" class="button button-primary button-sm">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
        Tentar Novamente
      </button>
    </div>
    <div v-else-if="userRecords.length === 0" class="empty-state card"> <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" viewBox="0 0 24 24" fill="currentColor" width="64" height="64"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 16H6c-.55 0-1-.45-1-1V6c0-.55.45-1 1-1h12c.55 0 1 .45 1 1v12c0 .55-.45 1-1 1zm-5-3H8v-2h5v2zm3-4H8v-2h8v2zm0-4H8V7h8v2z"/></svg>
      <h4 class="empty-state-title">Nenhum Registro Encontrado</h4>
      <p>Você ainda não possui registros de eventos na blockchain.</p>
      <p class="muted-text">Eventos importantes dos seus animais serão registrados aqui para garantir a trilha de auditoria.</p>
    </div>

    <div v-else class="records-list-container">
      <div class="records-summary">
        <p>Exibindo <strong>{{ userRecords.length }}</strong> registro(s) na blockchain.</p>
      </div>
      <ul class="records-list">
        <li v-for="record in userRecords" :key="record.id || record.transaction_hash" class="record-item card"> <div class="record-header">
            <h4 class="record-id-title">Registro ID: {{ record.id }}</h4>
            <span class="record-timestamp">{{ formatDate(record.created_at || record.timestamp) }}</span>
          </div>
          <div class="record-body">
            <div class="record-field">
                <span class="record-label">Animal ID:</span>
                <span class="record-value">{{ record.animal }}</span>
            </div>
            <div class="record-field">
                <span class="record-label">Evento ID:</span>
                <span class="record-value">{{ record.event }}</span>
            </div>
             <div class="record-field">
                <span class="record-label">Status na Blockchain:</span>
                <span :class="getBlockchainStatusClass(record.status)" class="status-badge">{{ record.status || 'Desconhecido' }}</span>
            </div>
            <div class="record-field transaction-hash-field">
                <span class="record-label">Hash da Transação:</span>
                <div class="hash-value-wrapper">
                    <span class="transaction-hash-text code-text">{{ record.transaction_hash }}</span>
                    <button @click="copyToClipboard(record.transaction_hash)" class="button button-icon button-sm" title="Copiar Hash">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
                    </button>
                    </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <NotificationModal
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
      @close="closeNotification"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { filterBlockchain } from '@/services/blockchainService';
import { getUserProfile } from '@/services/userService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'UserBlockchainRecords',
  components: {
    NotificationModal,
  },
  setup() {
    const userRecords = ref([]);
    const currentUser = ref(null);
    const isLoading = ref(true);
    const errorLoading = ref(false);
    const errorMessage = ref(''); // Para mensagens de erro mais específicas
    const notification = ref({ show: false, message: '', type: 'success' });

    const showAppNotification = (message, type = 'error', duration = 4000) => {
      notification.value.message = message;
      notification.value.type = type;
      notification.value.show = true;
      if (duration) {
        setTimeout(() => { notification.value.show = false; }, duration);
      }
    };
    const closeNotification = () => { notification.value.show = false; };

    const fetchCurrentUser = async () => {
      try {
        currentUser.value = await getUserProfile();
        if (!currentUser.value || !currentUser.value.id) {
            throw new Error('ID do usuário não encontrado no perfil.');
        }
      } catch (error) {
        console.error('Erro ao buscar perfil do usuário:', error.response?.data || error.message);
        errorLoading.value = true;
        errorMessage.value = 'Não foi possível identificar o usuário para buscar os registros.';
        showAppNotification(errorMessage.value, 'error');
        throw error; 
      }
    };

    const loadUserRecords = async () => {
      isLoading.value = true;
      errorLoading.value = false;
      errorMessage.value = '';
      userRecords.value = [];

      if (!currentUser.value) { // Se currentUser ainda não foi carregado
        try {
          await fetchCurrentUser();
        } catch (error) {
          isLoading.value = false;
          return; // fetchCurrentUser já trata o erro
        }
      }
      
      if (!currentUser.value || !currentUser.value.id) {
          isLoading.value = false;
          errorLoading.value = true;
          errorMessage.value = 'ID do usuário não disponível para filtrar registros.';
          showAppNotification(errorMessage.value, 'error');
          return;
      }

      try {
        // Confirme o nome do parâmetro de filtro: 'owner', 'user_id', 'recorded_by', etc.
        const records = await filterBlockchain({ owner: currentUser.value.id }); 
        userRecords.value = records.sort((a, b) => 
            new Date(b.created_at || b.timestamp * 1000) - new Date(a.created_at || a.timestamp * 1000)
        );
      } catch (error) {
        console.error('Erro ao carregar registros de blockchain do usuário:', error.response?.data || error);
        errorLoading.value = true;
        errorMessage.value = 'Falha ao buscar registros da blockchain. Verifique sua conexão ou tente mais tarde.';
        showAppNotification(errorMessage.value, 'error');
      } finally {
        isLoading.value = false;
      }
    };

    const formatDate = (dateInput) => {
      if (!dateInput) return 'N/A';
      let date;
      // Se for um timestamp numérico (provavelmente segundos da blockchain)
      if (typeof dateInput === 'number' || (typeof dateInput === 'string' && /^\d+$/.test(dateInput))) {
        date = new Date(Number(dateInput) * 1000);
      } else { // Se for uma string de data ISO
        date = new Date(dateInput);
      }

      if (isNaN(date.getTime())) return 'Data Inválida';
      
      return date.toLocaleString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit'
      });
    };

    const getBlockchainStatusClass = (status) => {
        if (!status) return 'status-default';
        const statusLower = String(status).toLowerCase();
        if (statusLower === 'confirmado' || statusLower === 'success' || statusLower === '1') return 'status-success'; // Exemplo
        if (statusLower === 'pendente' || statusLower === 'pending') return 'status-warning';  // Exemplo
        if (statusLower === 'falhou' || statusLower === 'failed' || statusLower === '0') return 'status-danger';   // Exemplo
        return 'status-info'; // Um status padrão para outros casos
    };
    
    const copyToClipboard = async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            showAppNotification('Hash copiado para a área de transferência!', 'success', 2000);
        } catch (err) {
            console.error('Falha ao copiar hash:', err);
            showAppNotification('Falha ao copiar o hash.', 'error');
        }
    };

    onMounted(loadUserRecords);

    return {
      userRecords,
      isLoading,
      errorLoading,
      errorMessage,
      loadUserRecords,
      formatDate,
      getBlockchainStatusClass,
      copyToClipboard,
      notification,
      closeNotification,
      showAppNotification
    };
  }
};
</script>

<style scoped>
/* Estilos globais como .content-panel, .card, .button, etc., são herdados */

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--sp-md);
    padding-bottom: var(--sp-md);
    border-bottom: var(--border-width) solid var(--color-border-light);
}
.panel-title-text { /* Usar esta classe para os títulos principais dos painéis do dashboard */
  font-family: var(--font-heading);
  color: var(--color-text-primary);
  font-size: var(--fs-h3);
  margin: 0;
  text-align: left;
}
.panel-description {
  text-align: left;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
}

.loading-state, .empty-state, .error-state {
  /* Herda de .empty-state global se definido, ou estiliza aqui */
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
  margin-top: var(--sp-lg);
}
.loading-state p, .empty-state p, .error-state p {
    color: var(--color-text-muted);
    margin-bottom: var(--sp-sm);
}
.empty-state-icon {
    color: var(--color-text-muted);
    margin-bottom: var(--sp-md);
}
.empty-state-title {
    font-family: var(--font-heading);
    font-size: var(--fs-h5);
    color: var(--color-text-secondary);
    margin-bottom: var(--sp-xs);
}
.error-state .button { /* Botão Tentar Novamente */
    margin-top: var(--sp-md);
}

.records-summary {
    margin-bottom: var(--sp-md);
    padding: var(--sp-sm) var(--sp-xs);
    background-color: var(--color-primary-light);
    color: var(--color-primary-dark);
    border-radius: var(--border-radius-sm);
    font-size: var(--fs-base);
    text-align: center;
}

.records-list-container {
  margin-top: var(--sp-lg);
}
.records-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr; /* Uma coluna por padrão */
  gap: var(--sp-md);
}

.record-item {
  /* .card global já estiliza fundo, borda, padding, shadow */
  padding: var(--sp-md);
  transition: var(--transition-base);
}
.record-item:hover {
    border-color: var(--color-primary-light);
    box-shadow: var(--shadow); /* Sombra do card global */
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--sp-md); /* Aumentado espaço */
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) dashed var(--color-border);
}
.record-id-title { /* Era strong */
  font-size: var(--fs-large); /* Um pouco maior */
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
  margin:0;
}
.record-timestamp {
    font-size: var(--fs-small);
    color: var(--color-text-muted);
}

.record-body .record-field {
  display: flex;
  justify-content: space-between; /* Alinha label à esquerda e valor à direita */
  align-items: flex-start; /* Alinha no topo se o valor for longo */
  margin-bottom: var(--sp-sm); /* Espaço entre os campos */
  padding: var(--sp-xs) 0;
  border-bottom: var(--border-width) solid var(--color-border-light);
}
.record-body .record-field:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.record-label {
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  margin-right: var(--sp-sm);
  flex-shrink: 0; /* Evita que o label encolha */
}
.record-value {
  color: var(--color-text-primary);
  text-align: right; /* Alinha o valor à direita */
  word-break: break-word; /* Para quebrar valores longos */
}

.transaction-hash-field .hash-value-wrapper {
    display: flex;
    align-items: center;
    justify-content: flex-end; /* Alinha à direita */
    gap: var(--sp-xs);
}
.transaction-hash-text.code-text { /* .code-text pode ser global para texto monoespaçado */
  font-family: var(--font-monospace);
  background-color: var(--color-bg-muted);
  padding: var(--sp-xxs) var(--sp-xs);
  border-radius: var(--border-radius-sm);
  font-size: 0.85em; /* Um pouco menor */
  word-break: break-all;
  color: var(--color-primary-dark);
}
.button.button-icon { /* Estilo para botões que são apenas ícones */
    padding: var(--sp-xs); /* Padding menor */
    line-height: 1; /* Para alinhar o SVG */
    min-width: auto; /* Remove min-width do botão padrão */
}

/* Badges de Status para Blockchain */
.status-badge {
    font-size: var(--fs-small);
    padding: var(--sp-xxs) var(--sp-sm);
    border-radius: var(--border-radius-pill);
    font-weight: var(--fw-medium);
    color: var(--color-text-inverted);
    text-transform: capitalize; /* Capitaliza o status */
    display: inline-block;
}
.status-success { background-color: var(--color-success); }
.status-warning { background-color: var(--color-warning); color: var(--color-text-primary); } /* Texto escuro para fundo amarelo */
.status-danger  { background-color: var(--color-danger); }
.status-info    { background-color: var(--color-info); }
.status-default { background-color: var(--color-text-muted); }

/* Spinner de Carregamento (exemplo simples) */
.spinner {
  animation: rotate 2s linear infinite;
  width: 50px;
  height: 50px;
  margin: 0 auto var(--sp-md);
}
.spinner .path {
  stroke: var(--color-primary);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}
@keyframes rotate {
  100% { transform: rotate(360deg); }
}
@keyframes dash {
  0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
}
</style>