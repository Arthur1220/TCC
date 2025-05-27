<template>
  <div class="blockchain-viewer-panel content-panel"> <div class="panel-header">
      <h2 class="panel-title-text">Visualizador de Registros da Blockchain</h2>
      </div>
    <p class="panel-description">
      Explore todos os registros imutáveis gravados na blockchain. Cada card representa uma transação ou evento significativo validado na rede.
    </p>

    <div v-if="loading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>Carregando registros da blockchain...</p>
    </div>
    <div v-else-if="errorMessage" class="empty-state card alert alert-danger">
        <h4 class="alert-heading">Erro ao Carregar Registros</h4>
        <p>{{ errorMessage }}</p>
        <button @click="fetchBlockchainRecords" class="button button-primary button-sm">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
            Tentar Novamente
        </button>
    </div>
    <div v-else-if="blockchainRecords.length === 0" class="empty-state card">
      <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" viewBox="0 0 24 24" fill="currentColor" width="64" height="64"><path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM17 11H7V9h10v2zm-4 4H7v-2h6v2zm3-7H7V6h9v2z"/></svg>
      <h4 class="empty-state-title">Nenhum Registro na Blockchain</h4>
      <p>Ainda não há dados registrados na blockchain ou não foi possível acessá-los.</p>
    </div>

    <div v-else class="blockchain-records-list">
      <div class="records-summary">
        <p>Exibindo <strong>{{ sortedBlockchainRecords.length }}</strong> registro(s) da blockchain (mais recentes primeiro).</p>
      </div>
      <div v-for="record in sortedBlockchainRecords" :key="record.id || record.transaction_hash" class="record-card card">
        <div class="record-card-header">
          <span class="record-id-tag">ID do Bloco/Registro: {{ record.id }}</span>
          <span class="record-timestamp">{{ formatPreciseDateTime(record.timestamp || record.created_at) }}</span>
        </div>
        <div class="record-card-body">
          <div class="detail-item">
            <span class="detail-label">Hash da Transação:</span>
            <div class="hash-value-wrapper">
              <span class="transaction-hash-text code-text">{{ record.transaction_hash }}</span>
              <button @click="copyToClipboard(record.transaction_hash, 'Hash da Transação')" class="button button-icon button-sm" title="Copiar Hash">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
              </button>
              <a v-if="record.transaction_hash && blockchainExplorerUrl" 
                 :href="`${blockchainExplorerUrl}tx/${record.transaction_hash}`" 
                 target="_blank" 
                 class="button button-link button-sm" 
                 title="Ver no explorador">
                 Ver no Explorador
              </a>
            </div>
          </div>
          <div class="detail-item">
            <span class="detail-label">Status do Registro:</span>
            <span :class="getBlockchainStatusClass(record.status)" class="status-badge">{{ record.status || 'Desconhecido' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Hash do Animal:</span>
            <span class="record-value code-text">{{ record.animal_details ? record.animal_details.animal_hash : 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Tipo de Evento:</span>
            <span class="record-value">{{ record.event_details ? record.event_details.name : 'N/A' }}</span>
          </div>
           <div class="detail-item">
            <span class="detail-label">ID do Evento no Sistema:</span>
            <span class="record-value">{{ record.event || 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">ID do Animal no Sistema:</span>
            <span class="record-value">{{ record.animal || 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Registrado por (Usuário):</span>
            <span class="record-value">{{ record.owner_details ? record.owner_details.username : (record.owner || 'N/A') }}</span>
          </div>
        </div>
      </div>
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
import { ref, onMounted, computed } from 'vue';
import { getBlockchains } from '@/services/blockchainService'; // Ajuste o caminho se necessário
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'BlockchainViewer',
  components: {
    NotificationModal,
  },
  data() {
    return {
      blockchainRecords: [],
      loading: true,
      errorMessage: '',
      notification: { show: false, title: '', message: '', type: 'success' },
      // Exemplo de URL base para um explorador de blockchain, configure conforme necessário
      blockchainExplorerUrl: 'https://polygonscan.com/', // Ex: para Polygon, ou Etherscan, etc. Deixe '' se não aplicável.
    };
  },
  computed: {
    sortedBlockchainRecords() {
      // Ordena os registros, assumindo que 'timestamp' ou 'created_at' existe e é comparável
      // Dando preferência a `created_at` se existir, senão `timestamp` (que pode ser numérico)
      return [...this.blockchainRecords].sort((a, b) => {
        const dateA = new Date(a.created_at || (typeof a.timestamp === 'number' ? a.timestamp * 1000 : a.timestamp));
        const dateB = new Date(b.created_at || (typeof b.timestamp === 'number' ? b.timestamp * 1000 : b.timestamp));
        return dateB - dateA; // Mais recentes primeiro
      });
    }
  },
  async created() {
    await this.fetchBlockchainRecords();
  },
  methods: {
    showAppNotification(title, message, type = 'success', duration = 4000) {
      this.notification.title = title;
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      if (duration) {
        setTimeout(() => { this.notification.show = false; }, duration);
      }
    },
    closeNotification() { this.notification.show = false; },
    async fetchBlockchainRecords() {
      this.loading = true;
      this.errorMessage = '';
      try {
        // getBlockchains() deve retornar todos os registros para um admin
        const records = await getBlockchains();
        this.blockchainRecords = records;
        if (records.length === 0) {
            this.showAppNotification("Informação", "Nenhum registro encontrado na blockchain.", "info", 5000);
        }
      } catch (error) {
        console.error('Erro ao buscar registros da blockchain:', error.response?.data || error);
        this.errorMessage = 'Erro ao carregar os registros da blockchain. Verifique a conexão ou as permissões do servidor.';
        this.showAppNotification('Erro de Carregamento', this.errorMessage, 'error');
      } finally {
        this.loading = false;
      }
    },
    formatPreciseDateTime(dateTimeInput) { // Renomeado para evitar conflito com formatDateTime mais simples
      if (!dateTimeInput) return 'N/A';
      let date;
      if (typeof dateTimeInput === 'number' || (typeof dateTimeInput === 'string' && /^\d+$/.test(dateTimeInput))) {
        date = new Date(Number(dateTimeInput) * 1000); // Assumindo timestamp Unix em segundos
      } else {
        date = new Date(dateTimeInput);
      }
      if (isNaN(date.getTime())) return 'Data Inválida';
      
      return date.toLocaleString('pt-BR', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false
      });
    },
    getBlockchainStatusClass(status) {
        if (!status) return 'status-badge status-default';
        const statusLower = String(status).toLowerCase();
        // Adapte estas strings aos status reais da sua blockchain
        if (statusLower === 'confirmado' || statusLower === 'sucesso' || statusLower === '1' || statusLower.includes('mined') || statusLower.includes('confirmed')) return 'status-badge status-success';
        if (statusLower === 'pendente' || statusLower === 'pending') return 'status-badge status-warning';
        if (statusLower === 'falhou' || statusLower === 'failed' || statusLower === '0' || statusLower.includes('reverted')) return 'status-badge status-danger';
        return 'status-badge status-info'; // Para status desconhecidos ou informativos
    },
    async copyToClipboard(text, fieldName = 'Valor') {
        try {
            await navigator.clipboard.writeText(text);
            this.showAppNotification(`${fieldName} copiado!`, `${text.substring(0,10)}... copiado para a área de transferência.`, 'success', 2000);
        } catch (err) {
            console.error(`Falha ao copiar ${fieldName.toLowerCase()}:`, err);
            this.showAppNotification(`Erro ao Copiar`, `Não foi possível copiar o ${fieldName.toLowerCase()}.`, 'error');
        }
    },
    // Opcional: para verificar se o hash parece ser de uma rede específica para o link do explorador
    // isEthHash(hash) {
    //     return typeof hash === 'string' && /^0x[a-fA-F0-9]{64}$/.test(hash);
    // }
  },
};
</script>

<style scoped>
/* Estilos Globais e Variáveis CSS são primários */

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--sp-md);
    padding-bottom: var(--sp-md);
    border-bottom: var(--border-width) solid var(--color-border-light);
}
.panel-title-text {
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

/* Estados de Carregamento, Vazio, Erro */
.loading-state, .empty-state {
  /* .empty-state global já pode ter estilos */
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
}
.empty-state.card {
    background-color: var(--color-bg-muted);
}
.loading-state .spinner {
    margin-bottom: var(--sp-sm);
}
.empty-state-icon {
    color: var(--color-text-muted);
    width: var(--sp-xxl); /* 48px */
    height: var(--sp-xxl);
    margin-bottom: var(--sp-md);
}
.empty-state-title {
    font-family: var(--font-heading);
    font-size: var(--fs-h5);
    color: var(--color-text-secondary);
    margin-bottom: var(--sp-xs);
}
.alert.alert-danger { /* Para o estado de erro */
    /* Estilos do .alert .alert-danger global */
    text-align: center;
}
.alert-heading { /* Para título dentro do alerta */
    font-size: var(--fs-large);
    font-weight: var(--fw-semibold);
    margin-bottom: var(--sp-sm);
}


.records-summary {
    margin-bottom: var(--sp-md);
    padding: var(--sp-sm);
    background-color: var(--color-bg-muted);
    border-radius: var(--border-radius-sm);
    font-size: var(--fs-base);
    color: var(--color-text-secondary);
    text-align: center;
    border: var(--border-width) solid var(--color-border-light);
}

.blockchain-records-list {
  display: grid;
  gap: var(--sp-lg); /* Espaçamento maior entre os cards */
  /* grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));  Pode ser 1fr para empilhar por padrão */
  grid-template-columns: 1fr; /* Uma coluna por padrão, para mais detalhes por card */
}

.record-card {
  /* .card global já estiliza fundo, borda, padding, shadow */
  padding: var(--sp-lg); /* Padding interno do card */
  transition: var(--transition-base);
}
.record-card:hover {
    border-color: var(--color-primary-light);
}

.record-card-header { /* Renomeado de .record-header */
  display: flex;
  justify-content: space-between;
  align-items: baseline; /* Alinha pela linha de base do texto */
  margin-bottom: var(--sp-md);
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) dashed var(--color-border);
}
.record-id-tag { /* Renomeado de .record-id */
  font-weight: var(--fw-semibold);
  font-size: var(--fs-large);
  color: var(--color-primary);
  font-family: var(--font-heading);
}
.record-timestamp { /* Renomeado de .record-date */
  font-size: var(--fs-small);
  color: var(--color-text-muted);
}

.record-card-body { /* Renomeado de .record-details */
  display: grid;
  gap: var(--sp-sm); /* Espaço entre os campos de detalhe */
}
.detail-item {
    display: flex;
    flex-direction: column; /* Label acima do valor */
    padding: var(--sp-xs) 0;
    border-bottom: var(--border-width) solid var(--color-border-light);
}
.detail-item:last-child {
    border-bottom: none;
}
.detail-label {
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  font-size: var(--fs-small);
  margin-bottom: var(--sp-xxs);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.record-value {
  color: var(--color-text-primary);
  word-break: break-word;
  font-size: var(--fs-base);
}
.code-text { /* Classe utilitária para textos como hashes */
  font-family: var(--font-monospace);
  background-color: var(--color-bg-muted);
  padding: var(--sp-xxs) var(--sp-xs);
  border-radius: var(--border-radius-sm);
  font-size: 0.9em;
  word-break: break-all;
  color: var(--color-primary-dark); /* Cor de destaque para hashes */
  display: inline-block; /* Para padding funcionar corretamente */
}

.hash-value-wrapper {
    display: flex;
    align-items: center;
    gap: var(--sp-sm);
    flex-wrap: wrap; /* Permite quebrar se não houver espaço */
}
.hash-value-wrapper .transaction-hash-text {
    flex-grow: 1; /* Hash ocupa espaço disponível */
}
.button.button-icon {
    padding: var(--sp-xs);
    line-height: 1;
    min-width: auto;
    flex-shrink: 0; /* Evita que o botão de copiar encolha */
}
.button.button-link.button-sm { /* Para o link "Ver no Explorador" */
    font-size: var(--fs-small);
    padding: var(--sp-xxs) var(--sp-xs);
    align-self: center; /* Alinha com o botão de copiar */
}


/* Badges de Status (reutilizando de UserBlockchainRecords) */
.status-badge {
    font-size: var(--fs-small);
    padding: calc(var(--sp-xxs) * 1.5) var(--sp-sm); /* Aumentado padding do badge */
    border-radius: var(--border-radius-pill);
    font-weight: var(--fw-semibold); /* Mais destaque */
    color: var(--color-text-inverted);
    text-transform: capitalize;
    display: inline-block;
    line-height: 1; /* Para alinhamento vertical */
}
.status-success { background-color: var(--color-success); }
.status-warning { background-color: var(--color-warning); color: var(--color-text-primary); }
.status-danger  { background-color: var(--color-danger); }
.status-info    { background-color: var(--color-info); }
.status-default { background-color: var(--color-text-muted); }


/* Spinner de Carregamento (reutilizado) */
.spinner {
  animation: rotate 2s linear infinite;
  width: 40px;
  height: 40px;
  margin: var(--sp-md) auto var(--sp-sm);
}
.spinner .path {
  stroke: var(--color-primary);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}
@keyframes rotate { 100% { transform: rotate(360deg); } }
@keyframes dash {
  0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
}

/* Responsividade */
@media (min-width: 992px) {
    .blockchain-records-list {
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); /* Duas colunas em telas maiores se couber */
    }
}
@media (max-width: 576px) {
    .record-card-header {
        flex-direction: column;
        align-items: flex-start;
        gap: var(--sp-xs);
    }
    .detail-item {
        flex-direction: column;
        align-items: flex-start;
    }
    .record-value {
        text-align: left;
    }
    .hash-value-wrapper {
        flex-direction: column;
        align-items: flex-start;
    }
    .hash-value-wrapper .button {
        margin-top: var(--sp-xs);
    }
}
</style>