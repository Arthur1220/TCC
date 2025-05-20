<!-- File: src/views/BlockchainSearchPage.vue -->
<template>
  <div class="blockchain-page">
    <AppHeader />

    <main class="dashboard-content section-gap">
      <div class="container blockchain-grid">
        <!-- Coluna da Explicação (sem borda) -->
        <section class="blockchain-explain">
          <h2 class="section-title">Auditoria de Blockchain</h2>
          <p class="section-description">
            A auditoria em blockchain é fundamental para garantir que cada
            registro seja <strong>permanente</strong>, <strong>inalterável</strong>
            e completamente <strong>transparente</strong>.  
          </p>
          <p class="section-description">
            Com nossa solução você consegue:
          </p>
          <ul class="explain-list">
            <li>
              <span class="check-icon">✔️</span>
              Imutabilidade de registros — ninguém consegue apagar ou alterar dados.
            </li>
            <li>
              <span class="check-icon">✔️</span>
              Transparência total — acesso público ao histórico de transações.
            </li>
            <li>
              <span class="check-icon">✔️</span>
              Rastreabilidade ponta-a-ponta — saiba exatamente quando e onde um evento ocorreu.
            </li>
            <li>
              <span class="check-icon">✔️</span>
              Auditabilidade em tempo real — valide transações sem intermediários.
            </li>
            <li>
              <span class="check-icon">✔️</span>
              Verificação de integridade de dados — assegure que nada foi adulterado.
            </li>
            <li>
              <span class="check-icon">✔️</span>
              Relatórios customizados — filtre por datas e tipos de evento na própria blockchain.
            </li>
          </ul>
          <p class="section-description">
            Isso tudo sem depender de terceiros ou de bancos de dados internos:
            você consulta diretamente nossa camada de prova, garantindo confiança
            em cada passo da sua cadeia produtiva.
          </p>

          <!-- FAQ no estilo Landing Page -->
          <div class="faq-grid">
            <div
              class="faq-item"
              v-for="(faq, idx) in faqs"
              :key="idx"
            >
              <button
                class="faq-question"
                @click="toggleFaq(idx)"
                :aria-expanded="faq.open"
              >
                <span>{{ faq.question }}</span>
                <span class="faq-icon">{{ faq.open ? '−' : '+' }}</span>
              </button>
              <div v-if="faq.open" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Coluna do Painel de Busca (com borda à direita) -->
        <aside class="blockchain-search-panel card">
          <h3 class="panel-title">Buscar Operações</h3>

          <div class="search-filter-group full-width">
            <input
              type="text"
              class="search-input"
              v-model="searchQuery"
              placeholder="Hash de transação ou ID de bloco"
              aria-label="Busca Blockchain"
            />
            <button
              class="button-primary"
              @click="performSearch"
            >
              Buscar
            </button>
          </div>

          <div class="results-area">
            <div v-if="results.length" class="results-list">
              <div
                v-for="op in results"
                :key="op.id"
                class="result-card card"
                tabindex="0"
              >
                <p><strong>ID:</strong> {{ op.id }}</p>
                <p><strong>Status:</strong> {{ op.status }}</p>
                <p><strong>Timestamp:</strong> {{ op.timestamp }}</p>
                <pre class="result-data">{{ op.data }}</pre>
              </div>
            </div>
            <div v-else-if="hasSearched" class="results-placeholder">
              <p>Nenhum resultado encontrado para "<em>{{ searchQuery }}</em>".</p>
            </div>
          </div>
        </aside>
      </div>
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
      results: [],
      hasSearched: false,
      faqs: [
        {
          question: 'O que é auditabilidade em blockchain?',
          answer: 'É a capacidade de verificar cada transação gravada na cadeia, assegurando que não houve alterações indevidas nos dados.',
          open: false
        },
        {
          question: 'Por que usar essa ferramenta?',
          answer: 'Permite que você mesmo valide eventos críticos sem depender exclusivamente de relatórios internos. Ideal para auditorias externas e investigações de conformidade.',
          open: false
        },
        {
          question: 'Como obter dados completos?',
          answer: 'Os resultados aqui são um resumo básico. Para acesso a relatórios completos ou dados históricos, entre em contato com o usuario do sistema.',
          open: false
        }
      ]
    };
  },
  methods: {
    performSearch() {
      this.hasSearched = true;
      if (!this.searchQuery.trim()) {
        this.results = [];
        return;
      }
      // Chamada real ao serviço de blockchain
      const mockData = {
        id: this.searchQuery.trim(),
        status: 'Confirmado',
        timestamp: new Date().toISOString(),
        data: JSON.stringify({
          evento: 'Vacinação',
          animalId: '042',
          propriedade: 'Fazenda Exemplo'
        }, null, 2)
      };
      this.results = [mockData];
    },
    toggleFaq(i) {
      this.faqs[i].open = !this.faqs[i].open;
    }
  }
};
</script>

<style scoped>
.blockchain-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.dashboard-content {
  flex: 1;
  background: var(--color-light-gray);
}
.blockchain-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--sp-lg);
  padding: var(--sp-lg) 0;
}
/* Exclusivo para o painel de busca */
.card {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
/* Explicação sem borda */
.blockchain-explain {
  padding: var(--sp-lg);
}
.section-title {
  font-size: 1.75rem;
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.section-description {
  font-size: var(--fs-base);
  color: var(--color-dark-gray);
  margin-bottom: var(--sp-lg);
}
.explain-list {
  list-style: none;
  padding: 0;
  margin: var(--sp-md) 0;
}
.check-icon {
  color: var(--color-primary);
  margin-right: var(--sp-xs);
}
/* FAQ estilo Landing Page */
.faq-grid {
  margin-top: var(--sp-lg);
  display: grid;
  gap: var(--sp-md);
}
.faq-item {
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  overflow: hidden;
}
.faq-question {
  width: 100%;
  background: var(--color-muted);
  border: none;
  padding: var(--sp-md);
  font-family: var(--font-heading);
  font-size: var(--fs-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
.faq-icon {
  font-size: var(--fs-large);
}
.faq-answer {
  background: var(--color-white);
  padding: var(--sp-md);
  color: var(--color-text);
}
/* Painel de busca */
.blockchain-search-panel {
  position: sticky;
  top: var(--sp-lg);
}
.search-filter-group {
  display: flex;
  gap: var(--sp-md);
  margin-bottom: var(--sp-lg);
}
.search-input {
  flex: 1;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-size: var(--fs-base);
  transition: border-color 0.2s;
}
.search-input:focus {
  border-color: var(--color-primary);
  outline: none;
}
/* Botão primário restaurado e sempre ativo */
.button-primary {
  padding: var(--sp-sm) var(--sp-lg);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  border-radius: var(--sp-sm);
  font-size: var(--fs-base);
  height: calc(var(--sp-sm) * 2 + var(--fs-base));
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
/* Resultados */
.results-list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-md);
}
.result-card {
  padding: var(--sp-md);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}
.result-card:hover,
.result-card:focus {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  outline: none;
}
.result-data {
  margin-top: var(--sp-sm);
  background: var(--color-light-gray);
  padding: var(--sp-sm);
  border-radius: var(--sp-sm);
  overflow-x: auto;
}
.results-placeholder {
  text-align: center;
  color: var(--color-gray);
  margin-top: var(--sp-md);
}
/* Responsivo */
@media (max-width: 768px) {
  .blockchain-grid {
    grid-template-columns: 1fr;
  }
  .blockchain-search-panel {
    position: relative;
    top: auto;
  }
}
</style>
