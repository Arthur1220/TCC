// ------------------------------
// File: src/views/BlockchainSearchPage.vue
// ------------------------------
<template>
  <div class="blockchain-page">
    <AppHeader />
    <main class="dashboard-content section-gap">
      <section class="blockchain-search full-screen">
        <h2 class="section-title">Auditoria de Blockchain</h2>
        <p class="section-description">
          A auditoria em blockchain garante a transparência e imutabilidade dos registros.
          Aqui você pode buscar hashes de transações ou IDs de blocos para verificar
          eventos críticos registrados na nossa cadeia de segunda camada.
        </p>

        <!-- Search Input -->
        <div class="search-filter-group full-width">
          <input
            type="text"
            class="search-input"
            v-model="searchQuery"
            placeholder="Digite hash de transação ou ID de bloco"
            aria-label="Busca Blockchain"
          />
          <button class="button-primary" @click="performSearch">Buscar</button>
        </div>

        <!-- Results -->
        <div class="results-section" v-if="result">
          <div class="result-card">
            <h3>Resultado da Busca</h3>
            <pre class="result-data">{{ result }}</pre>
          </div>
        </div>
        <div class="results-placeholder" v-else>
          <p>Nenhum resultado. Insira um hash ou bloco acima.</p>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
export default {
  name: 'BlockchainSearchPage',
  components: { AppHeader, AppFooter },
  data() {
    return {
      searchQuery: '',
      result: null
    };
  },
  methods: {
    performSearch() {
      if (!this.searchQuery) return;
      this.result = {
        id: this.searchQuery,
        timestamp: '2025-04-30T12:34:56Z',
        status: 'Confirmado',
        data: {
          evento: 'Vacinação',
          animalId: '042',
          propriedade: 'Fazenda Exemplo'
        }
      };
    }
  }
};
</script>

<style scoped>
.blockchain-page {
  display: flex;
  flex-direction: column;
  min-height: 120vh; /* ocupa quase toda a tela para footer só aparecer com scroll */
}
.dashboard-content {
  flex: 1;
  padding: var(--sp-lg);
  background: var(--color-light-gray);
}
.full-screen {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  min-height: calc(100vh - 200px); /* força rolagem */
}
.section-title {
  font-size: 1.75rem;
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.section-description {
  font-size: var(--font-size-base);
  color: var(--color-dark-gray);
  margin-bottom: var(--sp-lg);
}
.full-width {
  display: flex;
  gap: var(--sp-md);
  margin-bottom: var(--sp-lg);
}
.search-input {
  flex: 1;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-base);
  transition: border-color 0.2s;
}
.search-input:focus {
  border-color: var(--color-primary);
  outline: none;
}
.button-primary {
  padding: var(--sp-sm) var(--sp-md);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-large);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-primary:hover, .button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  transform: scale(1.02);
  outline: none;
}
.results-section {
  margin-top: var(--sp-lg);
}
.result-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  padding: var(--sp-lg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.result-card h3 {
  margin-bottom: var(--sp-md);
  color: var(--color-secondary);
}
.result-data {
  font-family: monospace;
  background: var(--color-light-gray);
  padding: var(--sp-sm);
  border-radius: var(--sp-sm);
  overflow-x: auto;
}
.results-placeholder {
  font-size: var(--font-size-base);
  color: var(--color-gray);
  text-align: center;
  margin-top: var(--sp-lg);
}
@media (max-width: 768px) {
  .full-width { flex-direction: column; }
}
</style>
