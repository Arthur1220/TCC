<template>
  <div class="blockchain-page">
    <AppHeader />

    <main class="main-content section">
      <div class="container blockchain-grid">
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
            <li><span class="explain-list-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></span> Imutabilidade total dos registros.</li>
            <li><span class="explain-list-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></span> Transparência completa do histórico.</li>
            <li><span class="explain-list-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></span> Rastreabilidade ponta-a-ponta.</li>
            <li><span class="explain-list-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></span> Auditabilidade em tempo real.</li>
            <li><span class="explain-list-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></span> Verificação de integridade.</li>
            <li><span class="explain-list-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></span> Relatórios customizados.</li>
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

          <div class="form-group search-form-group">
            <label for="blockchainSearch" class="form-label sr-only">ID Animal, Identificação ou Hash Tx</label>
            <input
              type="text"
              id="blockchainSearch"
              class="input search-input-field"
              v-model="searchQuery"
              placeholder="ID Animal, Identificação ou Hash Tx"
              aria-label="Buscar por ID do Animal, Identificação do Animal ou Hash da Transação na Blockchain"
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
              <p>Consultando...</p>
            </div>
            <div v-else-if="processedResults.length > 0" class="results-list">
              <h4 class="results-title">
                Resultados para: <strong>{{ searchedQueryDisplay }}</strong> 
                <span v-if="searchTypeMessage" class="search-type-message"> ({{ searchTypeMessage }})</span>
              </h4>
              <div
                v-for="result in processedResults"
                :key="result.uniqueKey" 
                class="result-card card"
                tabindex="0"
              >
                <p v-if="result.animalIdentificationDisplay"><strong>Animal (Busca):</strong> {{ result.animalIdentificationDisplay }}</p>
                <p><strong>Animal (Evento):</strong> {{ result.dbEventDetails?.animal_identification || result.blockchainData?.animalId || 'N/D' }}</p>
                <p><strong>Tipo de Evento (BD):</strong> {{ result.dbEventDetails?.event_type_name || 'N/D' }}</p>
                <p><strong>Data do Evento (BD):</strong> {{ formatDbTimestamp(result.dbEventDetails?.date) }}</p>
                <p><strong>Hash da Transação (BC):</strong> <span class="data-hash">{{ result.blockchainData?.transactionHash || result.dbBlockchainEntry?.transaction_hash || 'N/A' }}</span></p>
                <p><strong>Timestamp (BC):</strong> {{ formatBlockchainTimestamp(result.blockchainData?.timestamp || result.dbBlockchainEntry?.registration_date ) }}</p>
                
                <button class="button button-outline-primary button-sm mt-1" @click="openDetailsModal(result)">
                  Ver Mais Detalhes
                </button>
              </div>
            </div>
            <div v-else-if="hasSearched && !isSearching" class="results-placeholder empty-state">
              <p>Nenhum registro encontrado na blockchain para "<strong>{{ searchedQueryDisplay }}</strong>".</p>
              <p class="muted-text">Verifique o termo buscado ou tente novamente.</p>
            </div>
            <div v-else class="results-placeholder_initial empty-state">
                <p>Insira um ID de animal, identificação do animal ou hash de transação acima e clique em "Buscar".</p>
            </div>
          </div>
        </aside>
      </div>
    </main>
    <AppFooter />

    <div v-if="showDetailsModal && selectedEventForModal" class="modal-overlay" @click.self="closeDetailsModal">
      <EventDetailViewer
        :event-data="selectedEventForModal"
        :animals-list="animalsListForLookup"
        :properties-list="properties"
        :event-types-list="eventTypes" 
        title="Detalhes Completos do Evento Auditado"
        :show-close-button-in-header="true" 
        @close="closeDetailsModal"
      />
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
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import NotificationModal from '@/components/NotificationModal.vue';
import EventDetailViewer from '@/components/EventDetailViewer.vue'; 
import { listContractEventsByAnimalId, findBlockchainEntryByTxHash } from '@/services/contractService'; 
import { getEventDetails } from '@/services/eventService';
import { getAnimals, searchAnimalsByIdentification } from '@/services/animalService'; // Importar searchAnimalsByIdentification
import { getProperties, getEventTypes } from '@/services/lookupService';

export default {
  name: 'BlockchainSearchPage',
  components: { AppHeader, AppFooter, NotificationModal, EventDetailViewer },
  data() {
    return {
      searchQuery: '',
      searchedQueryDisplay: '',
      searchTypeMessage: '', // Para indicar o tipo de busca (ID, Hash, Identificação)
      processedResults: [], 
      hasSearched: false,
      isSearching: false,
      faqs: [ /* ... seu FAQ ... */ 
        { question: 'O que é auditabilidade em blockchain?', answer: 'É a capacidade de verificar cada transação gravada na cadeia de forma transparente e imutável...', open: false },
        { question: 'Por que esta ferramenta de auditoria é importante?', answer: 'Permite que você, seus parceiros ou auditores externos validem eventos críticos de forma independente...', open: false },
        { question: 'Quais informações são exibidas aqui?', answer: 'Esta interface exibe um resumo dos eventos registrados na blockchain... Para relatórios completos ou acesso a dados históricos detalhados, consulte as funcionalidades do seu dashboard ou contate o suporte.', open: false }
      ],
      notification: { show: false, message: '', type: 'success' },
      showDetailsModal: false,
      selectedEventForModal: null,
      properties: [],
      eventTypes: [],
      animalsListForLookup: [], // Para mapear ID de animal para identificação no modal
      searchedByType: null, // 'animalId', 'txHash', 'identification'
    };
  },
  async created() {
    this.isSearching = true; // Indica carregamento inicial
    try {
        const [properties, eventTypes, animals] = await Promise.all([
            getProperties(),
            getEventTypes(),
            getAnimals() // Carrega todos os animais para lookup de identificação
        ]);
        this.properties = properties;
        this.eventTypes = eventTypes;
        this.animalsListForLookup = animals;
    } catch (error) {
        console.error("Erro ao carregar dados de lookup:", error);
        this.showAppNotification("Erro ao carregar dados de referência para a página.", "error");
    } finally {
        this.isSearching = false;
    }
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
    closeNotification() { this.notification.show = false; },

    isTransactionHash(query) {
        return typeof query === 'string' && query.startsWith('0x') && query.length === 66;
    },
    isNumeric(query) {
        return !isNaN(parseFloat(query)) && isFinite(query);
    },

    async performSearch() {
      this.hasSearched = true;
      this.isSearching = true;
      this.processedResults = [];
      this.searchedQueryDisplay = this.searchQuery.trim();
      this.searchTypeMessage = '';
      this.searchedByType = null;

      if (!this.searchedQueryDisplay) {
        this.showAppNotification('Por favor, insira um termo para buscar.', 'warning');
        this.isSearching = false;
        this.hasSearched = false;
        return;
      }

      try {
        if (this.isTransactionHash(this.searchedQueryDisplay)) {
          this.searchTypeMessage = 'Hash da Transação';
          this.searchedByType = 'txHash';
          const blockchainEntries = await findBlockchainEntryByTxHash(this.searchedQueryDisplay);
          if (blockchainEntries && blockchainEntries.length > 0) {
            for (const entry of blockchainEntries) {
              let fullDbEventDetails = entry.event_details; 
              if (entry.event && entry.event_details?.event_type) {
                try {
                  fullDbEventDetails = await getEventDetails(entry.event, entry.event_details.event_type);
                } catch (dbError) {
                  console.warn(`Não foi possível buscar detalhes completos do DB para evento ${entry.event}:`, dbError);
                }
              }
              this.processedResults.push({
                uniqueKey: entry.transaction_hash + (entry.event || Date.now()), // Chave mais única
                dbBlockchainEntry: entry, 
                dbEventDetails: this.mapDbEventDetails(fullDbEventDetails),
                blockchainData: null,
                contextualAnimalInfo: entry.animal_details ? { identification: entry.animal_details.identification, id: entry.animal_id } : null,
              });
            }
          }
        } else if (this.isNumeric(this.searchedQueryDisplay)) {
          this.searchTypeMessage = 'ID do Animal';
          this.searchedByType = 'animalId';
          const animalId = Number(this.searchedQueryDisplay);
          const animalInfo = this.animalsListForLookup.find(a => a.id === animalId);
          const animalContext = animalInfo ? { identification: animalInfo.identification, id: animalInfo.id } : { identification: `ID ${animalId}`, id: animalId };
          const contractEvents = await listContractEventsByAnimalId(animalId);
          await this.processContractEvents(contractEvents, String(animalId));

        } else { // Assume busca por Identificação do Animal
          this.searchTypeMessage = 'Identificação do Animal';
          this.searchedByType = 'identification';
          const matchedAnimals = await searchAnimalsByIdentification(this.searchedQueryDisplay);
          if (matchedAnimals && matchedAnimals.length > 0) {
            if (matchedAnimals.length > 5) { // Limitar para evitar sobrecarga
                 this.showAppNotification(`Muitos animais encontrados (${matchedAnimals.length}). Mostrando eventos para os primeiros 5. Refine sua busca.`, "info");
            }
            for (const animal of matchedAnimals.slice(0, 5)) { // Processa até 5 animais
              const animalContext = { identification: animal.identification, id: animal.id };
              const contractEvents = await listContractEventsByAnimalId(animal.id);
              await this.processContractEvents(contractEvents, animalContext);

            }
          }
        }
      } catch (err) {
        console.error('Erro em performSearch:', err);
        this.processedResults = []; // Limpa em caso de erro
        this.showAppNotification(err.message || 'Erro ao buscar dados.', 'error');
      } finally {
        this.isSearching = false;
          if (this.processedResults.length === 0 && this.hasSearched) {
            // A mensagem de "nenhum resultado" já é tratada pelo v-else-if
          }
      }
    },

    
    async processContractEvents(contractEvents, animalContextInfo) {
        if (contractEvents && contractEvents.length > 0) {
            for (const bcEvent of contractEvents) {
                let dbEventDetailsData = null;
                try {
                    if(bcEvent.eventId && bcEvent.eventType !== undefined){ // Certifica que eventId e eventType existem
                         dbEventDetailsData = await getEventDetails(Number(bcEvent.eventId), Number(bcEvent.eventType));
                    } else {
                        console.warn("Evento da blockchain sem eventId ou eventType válidos:", bcEvent);
                    }
                } catch (dbError) {
                    console.warn(`Não foi possível buscar detalhes completos do DB para evento blockchain (ID Contrato: ${bcEvent.eventId}):`, dbError);
                }
                
                this.processedResults.push({
                    uniqueKey: `${animalContextInfo.id}-${bcEvent.dataHash || bcEvent.eventId}-${bcEvent.timestamp}`,
                    contextualAnimalInfo: animalContextInfo, 
                    blockchainData: bcEvent,
                    dbEventDetails: this.mapDbEventDetails(dbEventDetailsData), // Mapeia com lookups
                    dbBlockchainEntry: null // Neste fluxo, os dados da blockchain vêm direto do contrato
                });
            }
        }
        this.processedResults.sort((a,b) => 
            (b.blockchainData?.timestamp || new Date(b.dbBlockchainEntry?.registration_date).getTime()/1000 || 0) - 
            (a.blockchainData?.timestamp || new Date(a.dbBlockchainEntry?.registration_date).getTime()/1000 || 0)
        );
    },
    mapDbEventDetails(dbEventData) {
        if (!dbEventData) return null;
        return {
            ...dbEventData,
            animal_identification: this.getAnimalIdentificationFromList(dbEventData.animal),
            event_type_name: this.getEventTypeName(dbEventData.event_type),
            recorded_by_username: dbEventData.recorded_by_username || (dbEventData.recorded_by ? `Usuário ID ${dbEventData.recorded_by}` : 'N/A'),
            // Garante que 'details' seja um objeto, mesmo que vazio, se for null/undefined
            details: dbEventData.details || {} 
        };
    },

    getAnimalIdentificationFromList(animalId) {
        const animal = this.animalsListForLookup.find(a => a.id === animalId);
        return animal ? animal.identification : `ID ${animalId}`;
    },
    getEventTypeName(eventTypeId) {
        const type = this.eventTypes.find(t => t.id === eventTypeId);
        return type ? type.name : 'Desconhecido';
    },
     getPropertyName(propertyId) {
        const prop = this.properties.find(p => p.id === propertyId);
        return prop ? prop.name : `ID ${propertyId}`;
    },

    formatBlockchainTimestamp(timestamp) { 
        if (!timestamp && timestamp !==0) return 'N/A';
        try {
            const numericTimestamp = typeof timestamp === 'bigint' ? Number(timestamp) : Number(timestamp);
            if (isNaN(numericTimestamp)) return 'Data inválida (NaN)';
            const date = new Date(numericTimestamp * 1000); 
            return date.toLocaleString('pt-BR', {
                day: '2-digit', month: '2-digit', year: 'numeric',
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            });
        } catch (e) { return 'Data inválida'; }
    },
    formatDbTimestamp(dateTimeString) {
        if (!dateTimeString) return 'N/A';
        try {
            const date = new Date(dateTimeString);
            if (isNaN(date.getTime())) return 'Data Inválida';
            return date.toLocaleString('pt-BR', {
                day: '2-digit', month: '2-digit', year: 'numeric',
                hour: '2-digit', minute: '2-digit' 
            });
        } catch (e) { return "Data Inválida"; }
    },
     formatDate(dateString) { /* ... (como antes, mas certifique-se que a lógica de timezone está correta para 'validity') ... */ 
        if (!dateString) return 'N/A';
        try {
            // Para datas como 'YYYY-MM-DD', adicionar T00:00:00Z para interpretar como UTC e evitar problemas de fuso.
            const date = new Date(dateString.length === 10 && dateString.includes('-') ? dateString + 'T00:00:00Z' : dateString);
            if (isNaN(date.getTime())) return 'Data Inválida';
            return date.toLocaleDateString('pt-BR', {
              day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'UTC' // Exibe a data como está, sem conversão de fuso
            });
        } catch (e) { return "Data Inválida"; }
    },

    toggleFaq(index) { 
        this.faqs = this.faqs.map((faq, i) => ({
            ...faq,
            open: i === index ? !faq.open : false 
        }));
    },

    openDetailsModal(result) { // Este método agora apenas define os dados para o modal
      this.selectedEventForModal = { // Monta o objeto eventData esperado por EventDetailViewer
        dbEventDetails: result.dbEventDetails,
        blockchainData: result.blockchainData,
        dbBlockchainEntry: result.dbBlockchainEntry,
        contextualAnimalInfo: result.animalIdentificationDisplay 
                                ? { identification: result.animalIdentificationDisplay, id: result.animalIdForContext } 
                                : (result.dbEventDetails ? {identification: this.getAnimalIdentificationFromList(result.dbEventDetails.animal), id: result.dbEventDetails.animal } : null )
      };
      this.showDetailsModal = true;
    },
    closeDetailsModal() {
        this.showDetailsModal = false;
        this.selectedEventForModal = null;
    }
  }
};
</script>

<style scoped>
/* Seu CSS Scoped Existente ... */
.blockchain-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-bg-body);
}

.main-content {
  margin-top: 2rem; 
  margin-bottom: 2rem;
  flex: 1;
}

.blockchain-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr; 
  gap: var(--sp-xl); 
  align-items: flex-start; 
}

.blockchain-explain {
  padding: var(--sp-lg); 
  background-color: var(--color-bg-component);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
}

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
.subsection-title-global {
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  color: var(--color-text-primary);
  margin-top: var(--sp-xl);
  margin-bottom: var(--sp-md);
  text-align: left;
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
  align-items: flex-start;
  margin-bottom: var(--sp-md);
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
}
.explain-list-icon {
  color: var(--color-success);
  margin-right: var(--sp-sm);
  flex-shrink: 0;
  line-height: 1.5;
}
.explain-list-icon svg {
    vertical-align: top; 
}

.faq-section-container {
    margin-top: var(--sp-xl);
}
.faq-list {
  display: grid;
  gap: var(--sp-sm);
}
.faq-item {
  border: var(--border-width) solid var(--color-border-light);
  border-radius: var(--border-radius);
  overflow: hidden;
  background-color: var(--color-bg-component);
}
.faq-question {
  width: 100%;
  background-color: var(--color-bg-muted);
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
}
.faq-icon {
  font-size: var(--fs-large);
  font-weight: var(--fw-bold);
  transition: transform var(--transition-fast);
}
.faq-item[aria-expanded="true"] .faq-icon {
  transform: rotate(135deg);
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

.blockchain-search-panel {
  padding: var(--sp-lg);
  position: sticky;
  top: var(--sp-lg); 
  max-height: calc(100vh - var(--sp-lg) * 2 - 60px); 
  overflow-y: auto; 
}
.panel-title-sidebar {
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-lg);
  text-align: left;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: var(--sp-sm);
}

.search-form-group {
  display: flex;
  gap: var(--sp-sm); 
  margin-bottom: var(--sp-lg);
  align-items: stretch; 
}
.search-input-field {
  flex-grow: 1; 
}
.search-button {
  flex-shrink: 0; 
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
.search-type-message {
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    font-weight: var(--fw-normal);
}
.results-list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-md);
}
.result-card {
  padding: var(--sp-md);
  transition: var(--transition-base);
}
.result-card:hover,
.result-card:focus-within {
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow);
}
.result-card p {
  margin-bottom: var(--sp-xs);
  font-size: var(--fs-small);
  color: var(--color-text-secondary);
  word-break: break-word; 
}
.result-card p strong {
  color: var(--color-text-primary);
  font-weight: var(--fw-medium);
}
.data-hash, .registrant-address {
    font-family: var(--font-monospace);
    font-size: 0.9em; 
    color: var(--color-primary-dark);
    word-break: break-all;
}

.results-placeholder.empty-state {
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
}
.results-placeholder_initial.empty-state {
    padding: var(--sp-xl) var(--sp-md);
    text-align: center;
}
.muted-text {
    color: var(--color-text-muted);
    font-size: var(--fs-small);
    margin-top: var(--sp-xs);
}

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

.event-details-modal-body {
    max-height: 70vh; 
    overflow-y: auto; 
    padding-right: var(--sp-sm); 
}
.event-details-modal-body h4 {
    font-size: var(--fs-h5);
    color: var(--color-primary);
    margin-top: var(--sp-md);
    margin-bottom: var(--sp-sm);
    padding-bottom: var(--sp-xs);
    border-bottom: 1px solid var(--color-border-light);
}
.event-details-modal-body h4:first-child {
    margin-top: 0;
}
.details-section p {
    margin-bottom: var(--sp-xs);
    font-size: var(--fs-base);
    line-height: 1.5;
}
.details-section p strong {
    color: var(--color-text-primary);
    min-width: 150px; 
    display: inline-block;
}
.details-subtitle {
    font-size: var(--fs-base);
    font-weight: var(--fw-semibold);
    color: var(--color-text-secondary);
    margin-top: var(--sp-sm);
    margin-bottom: var(--sp-xs);
}
.specific-details {
    background-color: var(--color-bg-body); 
    padding: var(--sp-sm);
    border-radius: var(--border-radius-sm);
    margin-top: var(--sp-sm);
}
.specific-details p {
    font-size: var(--fs-small);
}
hr.my-1 { 
    margin-top: var(--sp-md);
    margin-bottom: var(--sp-md);
    border: 0;
    border-top: var(--border-width) solid var(--color-border);
}
.mt-1 { margin-top: var(--sp-sm); } 


@media (max-width: 992px) {
  .blockchain-grid {
    grid-template-columns: 1fr; 
    gap: var(--sp-xl); 
  }
  .blockchain-search-panel {
    position: static; 
    top: auto;
    max-height: none; 
    margin-top: var(--sp-xl); 
  }
  .section-title-global, .panel-title-sidebar {
    font-size: var(--fs-h3); 
  }
}
@media (max-width: 576px) {
    .search-form-group {
        flex-direction: column; 
    }
    .search-input-field, .search-button {
        width: 100%;
    }
}
</style>