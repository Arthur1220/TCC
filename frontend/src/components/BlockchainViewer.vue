<template>
  <div class="blockchain-viewer">
    <h2 class="section-title">Visualizar Registros da Blockchain</h2>

    <div v-if="loading" class="loading-state">
      <p>Carregando registros da blockchain...</p>
    </div>
    <div v-else-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
    <div v-else-if="blockchainRecords.length === 0" class="no-records">
      <p>Nenhum registro de blockchain encontrado.</p>
    </div>
    <div v-else class="blockchain-records-list">
      <div v-for="record in blockchainRecords" :key="record.id" class="record-card">
        <div class="record-header">
          <span class="record-id">ID do Registro: {{ record.id }}</span>
          <span class="record-date">Registrado em: {{ formatDateTime(record.timestamp) }}</span>
        </div>
        <div class="record-details">
          <p><strong>Hash da Transação:</strong> {{ record.transaction_hash }}</p>
          <p><strong>Status:</strong> {{ record.status }}</p>
          <p><strong>Animal Hash:</strong> {{ record.animal_details ? record.animal_details.animal_hash : 'N/A' }}</p>
          <p><strong>Evento:</strong> {{ record.event_details ? record.event_details.name : 'N/A' }}</p>
          <p><strong>Proprietário:</strong> {{ record.owner_details ? record.owner_details.username : 'N/A' }}</p>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getBlockchains } from '@/services/blockchainService'; // Ajuste o caminho se necessário

export default {
  name: 'BlockchainViewer',
  data() {
    return {
      blockchainRecords: [],
      loading: true,
      errorMessage: '',
    };
  },
  async created() {
    await this.fetchBlockchainRecords();
  },
  methods: {
    async fetchBlockchainRecords() {
      this.loading = true;
      this.errorMessage = '';
      try {
        const records = await getBlockchains();
        this.blockchainRecords = records;
      } catch (error) {
        this.errorMessage = 'Erro ao carregar os registros da blockchain. Verifique a conexão ou as permissões.';
        console.error('Erro ao buscar registros da blockchain:', error);
      } finally {
        this.loading = false;
      }
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'N/A';
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateTimeString).toLocaleDateString('pt-BR', options);
    },
  },
};
</script>

<style scoped>
.blockchain-viewer {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.section-title {
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}

.loading-state, .error-message, .no-records {
  text-align: center;
  padding: var(--sp-md);
  color: var(--color-dark-gray);
}

.error-message {
  color: #e74c3c;
}

.blockchain-records-list {
  display: grid;
  gap: var(--sp-md); /* Espaçamento entre os cards */
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* Colunas responsivas */
}

.record-card {
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  padding: var(--sp-md);
  background-color: var(--color-muted);
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.record-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.record-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--sp-sm);
  font-size: var(--fs-small);
  color: var(--color-dark-gray);
}

.record-id {
  font-weight: bold;
  color: var(--color-primary);
}

.record-details p {
  margin-bottom: var(--sp-xs); /* Espaçamento menor entre parágrafos */
  line-height: 1.4;
  color: var(--color-text);
}

.record-details strong {
  color: var(--color-primary);
}

/* Variáveis CSS para consistência */
:root {
  --color-primary: #3498db;
  --color-accent: #2ecc71; 
  --color-accent-dark: #27ae60;
  --color-text: #333333;
  --color-bg: #f5f5f5;
  --color-muted: #f0f0f0;
  --color-dark-gray: #7f8c8d;
  --color-border: #e0e0e0;
  --color-white: #ffffff;

  --font-heading: 'Roboto', sans-serif;
  --fs-small: 0.85rem;
  --fs-base: 1rem;

  --sp-xs: 0.25rem; /* 4px */
  --sp-sm: 0.5rem; /* 8px */
  --sp-md: 1rem;   /* 16px */
  --sp-lg: 1.5rem; /* 24px */
}
</style>