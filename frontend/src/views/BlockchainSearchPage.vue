<template>
  <div class="blockchain-page">
    <AppHeader />

    <main class="main-content section"> <div class="container blockchain-grid">
        <section class="blockchain-explain">
          <h2 class="section-title-global">Auditoria Detalhada em Blockchain</h2>
          <p class="section-description">
            A auditoria em blockchain é fundamental para garantir que cada
            registro seja <strong>permanente</strong>, <strong>inalterável</strong>
            e completamente <strong>transparente</strong>. Com nossa solução, você obtém confiança e clareza em cada etapa.
          </p>
          <p class="section-description">
            Benefícios diretos da nossa plataforma de auditoria:
          </p>
          <ul class="explain-list">
            <li>
              <span class="explain-list-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </span>
              Imutabilidade total dos registros.
            </li>
            <li>
              <span class="explain-list-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </span>
              Transparência completa do histórico de transações.
            </li>
            <li>
              <span class="explain-list-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </span>
              Rastreabilidade ponta-a-ponta de todos os eventos.
            </li>
            <li>
              <span class="explain-list-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </span>
              Auditabilidade em tempo real, sem intermediários.
            </li>
            <li>
              <span class="explain-list-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </span>
              Verificação de integridade dos dados registrados.
            </li>
            <li>
              <span class="explain-list-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </span>
              Geração de relatórios customizados diretamente da blockchain.
            </li>
          </ul>
          <p class="section-description additional-info">
            Consulte diretamente nossa camada de prova, garantindo confiança absoluta em cada passo da sua cadeia produtiva, sem dependência de terceiros.
          </p>

          <div class="faq-section-container">
            <h3 class="subsection-title-global">Dúvidas Comuns</h3>
            <div class="faq-list">
              <div class="faq-item" v-for="(faq, idx) in faqs" :key="idx">
                <button
                  class="faq-question"
                  @click="toggleFaq(idx)"
                  :aria-expanded="faq.open.toString()"
                  :aria-controls="`faq-answer-${idx}`"
                >
                  <span>{{ faq.question }}</span>
                  <span class="faq-icon" aria-hidden="true">{{ faq.open ? '−' : '+' }}</span>
                </button>
                <div v-show="faq.open" :id="`faq-answer-${idx}`" class="faq-answer">
                  <p>{{ faq.answer }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <aside class="blockchain-search-panel card">
          <h3 class="panel-title-sidebar">Buscar Operações na Blockchain</h3>

          <div class="form-group search-form-group"> <label for="blockchainSearch" class="form-label sr-only">ID do Animal</label> <input
              type="text"
              id="blockchainSearch"
              class="input search-input-field"
              v-model="searchQuery"
              placeholder="Digite o ID do animal para auditoria"
              aria-label="Buscar por ID do Animal na Blockchain"
              @keyup.enter="performSearch"
            />
            <button
              class="button button-primary search-button"
              @click="performSearch"
              :disabled="isSearching"
            >
              <span v-if="isSearching">Buscando...</span>
              <span v-else>Buscar</span>
            </button>
          </div>

          <div class="results-area">
            <div v-if="isSearching" class="loading-indicator">
              <p>Consultando blockchain...</p> </div>
            <div v-else-if="results.length > 0" class="results-list">
              <h4 class="results-title">Resultados para o Animal ID: {{ searchedAnimalId }}</h4>
              <div
                v-for="op in results"
                :key="op.transactionHash || op.eventId" class="result-card card"
                tabindex="0"
              >
                <p><strong>ID do Evento:</strong> {{ op.eventId }}</p>
                <p><strong>ID do Animal Registrado:</strong> {{ op.animalId }}</p>
                <p><strong>Tipo de Evento:</strong> {{ op.eventType }}</p>
                <p><strong>Hash dos Dados:</strong> <span class="data-hash">{{ op.dataHash }}</span></p>
                <p><strong>Registrado por:</strong> <span class="registrant-address">{{ op.registrant }}</span></p>
                <p><strong>Timestamp:</strong> {{ formatBlockchainTimestamp(op.timestamp) }}</p>
              </div>
            </div>
            <div v-else-if="hasSearched && !isSearching" class="results-placeholder empty-state"> <p>Nenhum evento encontrado na blockchain para o animal com ID "<strong>{{ searchedAnimalId }}</strong>".</p>
              <p class="muted-text">Verifique o ID do animal ou tente novamente mais tarde.</p>
            </div>
            <div v-else class="results-placeholder_initial empty-state">
                <p>Insira um ID de animal acima e clique em "Buscar" para ver os registros de auditoria.</p>
            </div>
          </div>
        </aside>
      </div>
    </main>
    <AppFooter />
    <NotificationModal
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
      @close="closeNotification"
    />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import NotificationModal from '@/components/NotificationModal.vue'; // Importar
import { listContractEvents } from '@/services/contractService'; // Assumindo que este serviço busca na blockchain

export default {
  name: 'BlockchainSearchPage',
  components: { AppHeader, AppFooter, NotificationModal },
  data() {
    return {
      searchQuery: '',
      searchedAnimalId: '', // Para guardar o ID que foi efetivamente buscado
      results: [],
      hasSearched: false,
      isSearching: false, // Novo estado para feedback de carregamento
      faqs: [
        {
          question: 'O que é auditabilidade em blockchain?',
          answer: 'É a capacidade de verificar cada transação gravada na cadeia de forma transparente e imutável, assegurando que não houve alterações indevidas nos dados e que as regras de negócio foram cumpridas.',
          open: false
        },
        {
          question: 'Por que esta ferramenta de auditoria é importante?',
          answer: 'Permite que você, seus parceiros ou auditores externos validem eventos críticos de forma independente, sem depender exclusivamente de relatórios internos. Ideal para auditorias, conformidade e aumento da confiança na cadeia de valor.',
          open: false
        },
        {
          question: 'Quais informações são exibidas aqui?',
          answer: 'Esta interface exibe um resumo dos eventos registrados na blockchain para um animal específico, incluindo IDs de evento e animal, tipo de evento, o hash dos dados registrados, o endereço que registrou e o timestamp da transação. Para relatórios completos ou acesso a dados históricos detalhados, consulte as funcionalidades do seu dashboard ou contate o suporte.',
          open: false
        }
      ],
      notification: { // Para notificações
        show: false,
        message: '',
        type: 'success'
      },
    };
  },
  methods: {
    showAppNotification(message, type = 'error', duration = 3000) {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      if (duration) {
        setTimeout(() => { this.notification.show = false; }, duration);
      }
    },
    closeNotification() {
        this.notification.show = false;
    },
    async performSearch() {
      this.hasSearched = true;
      this.isSearching = true;
      this.results = [];
      this.searchedAnimalId = this.searchQuery.trim(); // Guarda o ID buscado

      if (!this.searchedAnimalId) {
        this.showAppNotification('Por favor, insira um ID de animal para buscar.', 'warning');
        this.isSearching = false;
        this.hasSearched = false; // Reseta para mostrar mensagem inicial
        return;
      }

      try {
        // A função listContractEvents deve retornar um array.
        // Se ela retorna um objeto com uma propriedade 'events', ajuste: const { events } = await ...
        const rawEvents = await listContractEvents(Number(this.searchedAnimalId));

        // Certifique-se que 'rawEvents' é um array e mapeie se necessário
        if (Array.isArray(rawEvents)) {
            this.results = rawEvents.map(event => ({ // Mapeia para um formato consistente se necessário
                eventId: event.eventId?.toString() || event.id?.toString() || 'N/A', // Ajuste conforme o retorno
                animalId: event.animalId?.toString() || 'N/A',
                eventType: event.eventType || 'Desconhecido',
                dataHash: event.dataHash || 'N/A',
                registrant: event.registrant || 'N/A',
                timestamp: event.timestamp // Será formatado no template
            })).sort((a,b) => b.timestamp - a.timestamp); // Ordena pelos mais recentes (se timestamp for numérico)
        } else {
            console.error('listContractEvents não retornou um array:', rawEvents);
            this.showAppNotification('Formato de resposta inesperado do serviço de blockchain.', 'error');
            this.results = [];
        }

      } catch (err) {
        console.error('Erro ao buscar eventos na blockchain:', err);
        this.results = [];
        this.showAppNotification(err.message || 'Erro ao conectar com a blockchain ou buscar eventos.', 'error');
      } finally {
        this.isSearching = false;
      }
    },
    toggleFaq(index) {
       this.faqs = this.faqs.map((faq, i) => ({
        ...faq,
        open: i === index ? !faq.open : false // Fecha outros ao abrir um
      }));
    },
    formatBlockchainTimestamp(timestamp) {
      if (!timestamp) return 'N/A';
      // Timestamps da blockchain geralmente são em segundos (Unix timestamp)
      // Se for BigInt (como ethers.js retorna), converta para Number primeiro
      try {
        const numericTimestamp = typeof timestamp === 'bigint' ? Number(timestamp) : timestamp;
        const date = new Date(numericTimestamp * 1000); // Multiplica por 1000 se for segundos
        return date.toLocaleString('pt-BR', {
          day: '2-digit', month: '2-digit', year: 'numeric',
          hour: '2-digit', minute: '2-digit', second: '2-digit'
        });
      } catch (e) {
        console.error("Erro ao formatar timestamp:", timestamp, e);
        return 'Data inválida';
      }
    }
  }
};
</script>

<style scoped>
/* Estilos Globais Aplicados via Classes e Variáveis */
.blockchain-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-bg-body);
}

.main-content { /* Substitui .dashboard-content para esta página */
  margin-top: 2rem; /* Espaçamento global do topo */
  margin-bottom: 2rem; /* Espaçamento global do fundo */
  flex: 1;
  /* .section já adiciona padding vertical global (var(--sp-xxl)) */
}

.blockchain-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr; /* Coluna da esquerda um pouco maior */
  gap: var(--sp-xl); /* Espaço maior entre colunas */
  align-items: flex-start; /* Alinha os itens no topo */
}

/* Coluna da Explicação */
.blockchain-explain {
  padding: var(--sp-lg); /* Padding interno para a seção de explicação */
  background-color: var(--color-bg-component);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
}

/* Títulos de Seção (usando a classe global) */
/* .section-title-global já definido na LandingPage, deve estar no style.css global */
/* Se não estiver, defina-o aqui ou no global: */
.section-title-global {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--sp-lg);
}
.section-title-global::after {
    content: '';
    display: block;
    width: 60px;
    height: 3px;
    background-color: var(--color-primary);
    margin: var(--sp-sm) auto var(--sp-lg);
}
.subsection-title-global { /* Para subtítulos como o do FAQ */
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  color: var(--color-text-primary);
  margin-top: var(--sp-xl);
  margin-bottom: var(--sp-md);
  text-align: left; /* Alinhamento específico para subtítulo */
}


.section-description {
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
  line-height: var(--lh-base);
  margin-bottom: var(--sp-md);
}
.section-description strong {
    color: var(--color-primary);
    font-weight: var(--fw-semibold);
}
.additional-info {
    margin-top: var(--sp-lg);
    font-style: italic;
    color: var(--color-text-muted);
}

.explain-list {
  list-style: none;
  padding: 0;
  margin: var(--sp-lg) 0;
}
.explain-list li {
  display: flex;
  align-items: flex-start; /* Alinha ícone com início do texto */
  margin-bottom: var(--sp-md);
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
}
.explain-list-icon {
  color: var(--color-success); /* Ícone de check com cor de sucesso */
  margin-right: var(--sp-sm);
  flex-shrink: 0; /* Evita que o ícone encolha */
  line-height: 1.5; /* Alinhar com o texto */
}
.explain-list-icon svg {
    vertical-align: top; /* Melhor alinhamento vertical */
}


/* FAQ - Estilos reutilizados da LandingPage, mas adaptados aqui */
.faq-section-container {
    margin-top: var(--sp-xl);
}
.faq-list {
  display: grid;
  gap: var(--sp-sm);
}
.faq-item {
  border: var(--border-width) solid var(--color-border-light); /* Borda mais sutil */
  border-radius: var(--border-radius);
  overflow: hidden;
  background-color: var(--color-bg-component); /* Fundo do item */
}
.faq-question {
  width: 100%;
  background-color: var(--color-bg-muted); /* Fundo do botão da pergunta */
  border: none;
  padding: var(--sp-md);
  font-family: var(--font-body);
  font-weight: var(--fw-medium);
  font-size: var(--fs-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  text-align: left;
  color: var(--color-text-primary);
  transition: background-color var(--transition-fast);
}
.faq-question:hover, .faq-question:focus {
  background-color: var(--color-bg-hover);
}
.faq-item[aria-expanded="true"] .faq-question {
   color: var(--color-primary);
   /* border-bottom: var(--border-width) solid var(--color-border); */ /* Opcional: linha quando aberto */
}
.faq-icon {
  font-size: var(--fs-large);
  font-weight: var(--fw-bold);
  transition: transform var(--transition-fast);
}
.faq-item[aria-expanded="true"] .faq-icon {
  transform: rotate(135deg); /* '+' para 'x' */
}
.faq-answer {
  padding: var(--sp-md);
  color: var(--color-text-secondary);
  background-color: var(--color-bg-component);
  border-top: var(--border-width) solid var(--color-border-light);
}
.faq-answer p {
    margin-bottom: 0;
}

/* Painel de Busca (Coluna da Direita) */
.blockchain-search-panel {
  /* .card global já aplica: background, padding, border-radius, box-shadow */
  padding: var(--sp-lg); /* Padding interno do painel */
  position: sticky;
  top: var(--sp-lg); /* Começa a fixar após um scroll */
  max-height: calc(100vh - var(--sp-lg) * 2 - 60px); /* Altura máxima considerando header e padding da página */
  overflow-y: auto; /* Scroll interno se o conteúdo for maior */
}
.panel-title-sidebar { /* Título específico para a sidebar de busca */
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-lg);
  text-align: left;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: var(--sp-sm);
}

.search-form-group { /* Usando .form-group do global se adaptado, ou estilos locais */
  display: flex;
  gap: var(--sp-sm); /* Espaço entre input e botão */
  margin-bottom: var(--sp-lg);
  align-items: stretch; /* Faz o input e botão terem a mesma altura */
}
.search-input-field { /* .input global será aplicado */
  flex-grow: 1; /* Input ocupa o espaço restante */
  /* Altura é definida pelo padding do .input global */
}
.search-button { /* .button .button-primary globais serão aplicados */
  /* Altura deve corresponder ao input se .input e .button tiverem padding vertical similar */
  flex-shrink: 0; /* Botão não encolhe */
}
.search-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.results-area {
  margin-top: var(--sp-lg);
}
.loading-indicator p,
.results-placeholder p {
    color: var(--color-text-muted);
    font-style: italic;
}
.loading-indicator {
    text-align: center;
    padding: var(--sp-xl) 0;
}

.results-title {
    font-size: var(--fs-large);
    color: var(--color-text-primary);
    margin-bottom: var(--sp-md);
    border-bottom: 1px solid var(--color-border);
    padding-bottom: var(--sp-sm);
}
.results-list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-md);
}
.result-card {
  /* .card global já aplica estilos base */
  padding: var(--sp-md);
  transition: var(--transition-base);
}
.result-card:hover,
.result-card:focus-within { /* :focus-within se houver links/botões dentro */
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow);
}
.result-card p {
  margin-bottom: var(--sp-xs);
  font-size: var(--fs-small);
  color: var(--color-text-secondary);
  word-break: break-word; /* Para quebrar hashes longos ou endereços */
}
.result-card p strong {
  color: var(--color-text-primary);
  font-weight: var(--fw-medium);
}
.data-hash, .registrant-address {
    font-family: var(--font-monospace);
    font-size: 0.9em; /* Um pouco menor para dados técnicos */
    color: var(--color-primary-dark);
    word-break: break-all;
}


.results-placeholder.empty-state { /* Estilo para quando não há resultados, herda de .empty-state */
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
}
.results-placeholder_initial.empty-state {
    padding: var(--sp-xl) var(--sp-md);
    text-align: center;
}
.muted-text { /* Classe utilitária para texto mais suave */
    color: var(--color-text-muted);
    font-size: var(--fs-small);
    margin-top: var(--sp-xs);
}

/* SR Only para acessibilidade (se não estiver no global .css) */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}


/* Responsivo */
@media (max-width: 992px) { /* Ajuste o breakpoint se necessário (era 768px) */
  .blockchain-grid {
    grid-template-columns: 1fr; /* Uma coluna */
    gap: var(--sp-xl); /* Aumenta o gap quando empilhado */
  }
  .blockchain-search-panel {
    position: static; /* Remove o sticky no mobile */
    top: auto;
    max-height: none; /* Remove altura máxima */
    margin-top: var(--sp-xl); /* Espaço acima do painel de busca quando empilhado */
  }
  .section-title-global, .panel-title-sidebar {
    font-size: var(--fs-h3); /* Títulos um pouco menores no mobile */
  }
}
@media (max-width: 576px) {
    .search-form-group {
        flex-direction: column; /* Botão de busca abaixo do input */
    }
    .search-input-field, .search-button {
        width: 100%;
    }
}
</style>