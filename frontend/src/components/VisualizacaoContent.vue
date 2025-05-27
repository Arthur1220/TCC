<template>
  <div class="admin-event-viewer-content content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Visualização de Todos os Eventos do Sistema</h2>
    </div>
    <p class="panel-description">
      Acompanhe e audite todos os eventos registrados na plataforma. Clique em "Detalhes" para ver informações completas de cada evento.
    </p>

    <div v-if="isLoading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>Carregando todos os eventos...</p>
    </div>
    <div v-else-if="fetchError" class="empty-state card alert alert-danger">
        <h4 class="alert-heading">Erro ao Carregar Eventos</h4>
        <p>{{ fetchError }}</p>
        <button @click="fetchAllSystemData" class="button button-primary button-sm">Tentar Novamente</button>
    </div>
    <div v-else>
      <div v-if="events.length" class="table-responsive-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID Evento</th>
              <th>Animal</th>
              <th>Tipo de Evento</th>
              <th>Data</th>
              <th>Localização</th>
              <th class="th-observations">Observações</th>
              <th class="text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="evt in sortedEvents" :key="evt.id" class="table-row-hover">
              <td data-label="ID Evento">{{ evt.id }}</td>
              <td data-label="Animal">{{ getAnimalIdentification(evt.animal) }}</td>
              <td data-label="Tipo de Evento">{{ getEventTypeName(evt.event_type) }}</td>
              <td data-label="Data">{{ formatDateTime(evt.date) }}</td>
              <td data-label="Localização">{{ evt.location || 'N/A' }}</td>
              <td data-label="Observações" class="truncate-text">{{ evt.observations || 'N/A' }}</td>
              <td data-label="Ações" class="actions-cell">
                <button class="button button-outline-primary button-sm" @click="loadAndShowEventDetails(evt)" title="Ver Detalhes">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 4C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 12.5c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                  Detalhes
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state card">
        <p>Nenhum evento encontrado no sistema.</p>
      </div>
    </div>

    <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-content card large-modal">
        <div class="modal-header">
          <h3 class="modal-title-text">Detalhes Completos do Evento #{{ detailedEvent?.id }}</h3>
          <button @click="closeDetailsModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <div class="modal-body event-details-modal-body">
          <div v-if="isLoadingDetails" class="loading-state">
            <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
            <p>Carregando detalhes...</p>
          </div>
          <div v-else-if="detailedEvent" class="event-details-grid">
            <div class="detail-group">
              <h4>Informações Gerais do Evento</h4>
              <p><strong>ID do Evento:</strong> {{ detailedEvent.id }}</p>
              <p><strong>Animal:</strong> {{ getAnimalIdentification(detailedEvent.animal) }} (ID: {{ detailedEvent.animal }})</p>
              <p><strong>Tipo de Evento:</strong> {{ getEventTypeName(detailedEvent.event_type) }}</p>
              <p><strong>Data e Hora:</strong> {{ formatDateTime(detailedEvent.date) }}</p>
              <p><strong>Localização:</strong> {{ detailedEvent.location || 'N/A' }}</p>
              <p><strong>Observações:</strong> {{ detailedEvent.observations || 'N/A' }}</p>
              <p><strong>Registrado por:</strong> {{ detailedEvent.recorded_by_username || 'Usuário ID: ' + detailedEvent.recorded_by }}</p>
            </div>

            <div v-if="detailedEvent.specific_details" class="detail-group specific-details-group">
              <h4>Detalhes Específicos do Tipo de Evento</h4>
              <div v-for="(value, key) in detailedEvent.specific_details" :key="key" class="specific-detail-item">
                <p><strong>{{ formatDetailKey(key) }}:</strong> {{ formatDetailValue(key, value) }}</p>
              </div>
            </div>
            <div v-else class="detail-group specific-details-group">
                <p><em>Nenhum detalhe específico para este tipo de evento.</em></p>
            </div>
          </div>
          <div v-else class="empty-state small-empty-state">
            <p>Não foi possível carregar os detalhes do evento.</p>
          </div>
        </div>
        <div class="modal-actions form-actions">
          <button class="button button-secondary" @click="closeDetailsModal">Fechar</button>
        </div>
      </div>
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
import { getEvents, getEventDetails } from '@/services/eventService'; // getEventDetails para o modal
import { getEventTypes } from '@/services/lookupService';
import { getAnimals } from '@/services/animalService'; // Para mapear ID de animal para nome
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'VisualizacaoContent',
  components: {
    NotificationModal,
  },
  setup() {
    const events = ref([]);
    const eventTypes = ref([]);
    const animals = ref([]); // Para armazenar a lista de animais
    const animalMap = computed(() => { // Mapa para acesso rápido à identificação do animal
        return animals.value.reduce((map, animal) => {
            map[animal.id] = animal.identification;
            return map;
        }, {});
    });

    const detailedEvent = ref(null); // Para o modal, vai conter o evento principal + specific_details
    const showDetailsModal = ref(false);
    const isLoading = ref(true); // Para a lista principal de eventos
    const isLoadingDetails = ref(false); // Para o carregamento dos detalhes no modal
    const fetchError = ref(null); // Para erros ao carregar a lista principal

    const notification = ref({ show: false, message: '', type: 'success' });

    const showAppNotification = (message, type = 'error', duration = 4000) => {
      notification.value.message = message;
      notification.value.type = type;
      notification.value.show = true;
      if(duration) setTimeout(() => { notification.value.show = false; }, duration);
    };
    const closeNotification = () => { notification.value.show = false; };

    const fetchAllSystemData = async () => {
      isLoading.value = true;
      fetchError.value = null;
      try {
        // Idealmente, getEvents() para admin não filtraria por usuário
        const [eventsData, eventTypesData, animalsData] = await Promise.all([
          getEvents({all_events_admin: true}), // Supondo um parâmetro para buscar todos os eventos
          getEventTypes(),
          getAnimals({all_animals_admin: true}) // Supondo um parâmetro para buscar todos os animais
        ]);
        events.value = eventsData;
        eventTypes.value = eventTypesData;
        animals.value = animalsData;

      } catch (e) {
        console.error("Erro ao carregar dados para VisualizacaoContent:", e.response?.data || e);
        fetchError.value = 'Falha ao carregar dados do sistema. Verifique o console para mais detalhes.';
        showAppNotification(fetchError.value, 'error');
      } finally {
        isLoading.value = false;
      }
    };

    const getEventTypeName = (eventTypeId) => {
      const type = eventTypes.value.find(t => t.id === eventTypeId);
      return type ? type.name : 'Desconhecido';
    };

    const getAnimalIdentification = (animalId) => {
        return animalMap.value[animalId] || `ID ${animalId}`;
    };
    
    const formatDateTime = (dateTimeString) => {
      if (!dateTimeString) return 'N/A';
      try {
        const date = new Date(dateTimeString);
        return date.toLocaleString('pt-BR', {
          day: '2-digit', month: '2-digit', year: 'numeric',
          hour: '2-digit', minute: '2-digit'
        });
      } catch (e) { return dateTimeString; }
    };

    const loadAndShowEventDetails = async (eventSummary) => {
      isLoadingDetails.value = true;
      detailedEvent.value = null; // Limpa o evento anterior
      showDetailsModal.value = true;
      try {
        // Usa eventService.getEventDetails para buscar detalhes completos, incluindo os específicos do tipo
        const fullDetails = await getEventDetails(eventSummary.id, eventSummary.event_type);
        detailedEvent.value = {
            ...eventSummary, // Dados básicos já presentes na lista
            ...fullDetails, // Sobrescreve com dados mais completos do evento principal
            specific_details: fullDetails.details || null // Adiciona os detalhes específicos
        };
        // Tenta buscar o nome do usuário que registrou
        if (detailedEvent.value.recorded_by && !detailedEvent.value.recorded_by_username) {
            // Esta parte pode ser complexa se precisar de uma chamada separada para buscar dados de usuário por ID.
            // Por ora, podemos apenas exibir o ID. Se User Service puder buscar por ID:
            // const user = await getUserById(detailedEvent.value.recorded_by);
            // detailedEvent.value.recorded_by_username = user.username;
        }

      } catch (error) {
        console.error(`Erro ao buscar detalhes do evento ID ${eventSummary.id}:`, error.response?.data || error);
        showAppNotification(`Erro ao carregar detalhes do evento #${eventSummary.id}.`, 'error');
        detailedEvent.value = { ...eventSummary, error_message: "Falha ao carregar detalhes completos." }; // Mostra dados básicos com erro
      } finally {
        isLoadingDetails.value = false;
      }
    };

    const closeDetailsModal = () => {
      showDetailsModal.value = false;
      detailedEvent.value = null;
    };

    // Formata as chaves dos detalhes específicos para exibição
    const formatDetailKey = (key) => {
        return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()); // Ex: "origin_property" -> "Origin Property"
    };
    
    // Formata valores específicos (ex: datas, booleanos)
    const formatDetailValue = (key, value) => {
        if (value === null || value === undefined) return 'N/A';
        if (typeof value === 'boolean') return value ? 'Sim' : 'Não';
        if (key.includes('date') || key.includes('validity')) { // Se a chave contiver 'date' ou 'validity'
            const d = new Date(value);
            if (!isNaN(d.getTime())) { // Verifica se é uma data válida
                 // Se for só data (sem hora relevante como em 'validity')
                if (value.length === 10 && value.includes('-')) return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'UTC' });
                return d.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' });
            }
        }
        if (key.toLowerCase().includes('property') && properties.value.length > 0 && !isNaN(Number(value))) {
            const prop = properties.value.find(p => p.id === Number(value));
            return prop ? `${prop.name} (ID: ${value})` : `ID: ${value}`;
        }
        // Adicionar mais formatações conforme necessário (ex: buscar nome do animal se 'male_id' ou 'female_id')
        return value;
    };

    onMounted(fetchAllSystemData);

    const sortedEvents = computed(() => {
        return [...events.value].sort((a, b) => new Date(b.date) - new Date(a.date));
    });

    const properties = ref([]); // Para lookup de nomes de propriedades
    const loadProperties = async () => { // Carrega propriedades para o modal de detalhes
        try {
            // Substitua pela sua função real de buscar propriedades, se existir
            // import { getProperties } from '@/services/lookupService';
            // properties.value = await getProperties();
        } catch (e) { console.error("Erro ao carregar propriedades para lookup:", e); }
    };
    onMounted(loadProperties); // Carrega propriedades ao montar


    return {
      events,
      sortedEvents, // Usar eventos ordenados no template
      isLoading,
      fetchError,
      detailedEvent,
      showDetailsModal,
      isLoadingDetails,
      getEventTypeName,
      getAnimalIdentification,
      formatDateTime,
      loadAndShowEventDetails,
      closeDetailsModal,
      formatDetailKey,
      formatDetailValue,
      fetchAllSystemData, // Para o botão "Tentar Novamente"
      notification,
      showAppNotification,
      closeNotification
    };
  }
};
</script>

<style scoped>
/* Estilos Globais Aplicados via Classes e Variáveis CSS */

.panel-header {
    display: flex;
    justify-content: space-between; /* Se houver ações no header */
    align-items: center;
    margin-bottom: var(--sp-md);
    padding-bottom: var(--sp-md);
    border-bottom: var(--border-width) solid var(--color-border-light);
}
.panel-title-text { /* Usar esta classe para os títulos principais dos painéis */
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

.loading-state, .empty-state { /* .empty-state global já tem estilos */
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
}
.empty-state.card { /* Estilo de card para empty state */
    background-color: var(--color-bg-muted);
}
.loading-state .spinner { /* Estilo para o spinner (definido em UserBlockchainRecords) */
    margin-bottom: var(--sp-sm);
}

.table-responsive-wrapper {
  overflow-x: auto;
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-bg-component);
  box-shadow: var(--shadow-sm);
}
/* .data-table, th, td, .table-row-hover, .actions-cell, .truncate-text já estilizados em EventContent.vue */
/* Se precisar de ajustes muito específicos, pode adicionar aqui, mas idealmente são compartilhados. */
.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}
.data-table th,
.data-table td {
  text-align: left;
  padding: var(--sp-sm) var(--sp-md);
  border-bottom: var(--border-width) solid var(--color-border-light);
  font-size: var(--fs-base);
  vertical-align: middle;
}
.data-table th {
  background-color: var(--color-bg-muted);
  color: var(--color-text-primary);
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  font-size: var(--fs-small);
}
.data-table tbody tr.table-row-hover:hover {
  background-color: var(--color-bg-hover);
}
.data-table .th-observations { min-width: 220px; }
.data-table .truncate-text {
  max-width: 220px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
.actions-cell {
  white-space: nowrap;
  text-align: right;
}
.actions-cell .button {
    margin-left: var(--sp-xs);
    display: inline-flex;
    align-items: center;
    gap: var(--sp-xs);
}

/* Modal de Detalhes do Evento */
/* .modal-overlay, .modal-content, .card, .large-modal, .modal-header, */
/* .modal-title-text, .button-close, .modal-body, .form-actions, */
/* .button, .button-secondary já são globais */

.event-details-modal-body {
    text-align: left;
    font-size: var(--fs-base);
}
.event-details-grid {
    display: grid;
    grid-template-columns: 1fr; /* Uma coluna por padrão */
    gap: var(--sp-lg);
}
.detail-group {
    padding: var(--sp-md);
    background-color: var(--color-bg-muted);
    border-radius: var(--border-radius-sm);
    border: var(--border-width) solid var(--color-border-light);
}
.detail-group h4 {
    font-family: var(--font-heading);
    font-size: var(--fs-large);
    color: var(--color-primary);
    margin-top: 0;
    margin-bottom: var(--sp-md);
    padding-bottom: var(--sp-sm);
    border-bottom: var(--border-width) dashed var(--color-border);
}
.detail-group p, .specific-detail-item p {
    margin-bottom: var(--sp-sm);
    line-height: 1.5;
    color: var(--color-text-secondary);
    word-break: break-word;
}
.detail-group p strong, .specific-detail-item p strong {
    color: var(--color-text-primary);
    font-weight: var(--fw-medium);
    min-width: 150px; /* Para alinhar os valores */
    display: inline-block;
}
.specific-details-group {
    background-color: var(--color-primary-light); /* Destaque para detalhes específicos */
    border-color: var(--color-primary);
}
.specific-details-group h4 {
    color: var(--color-primary-dark);
    border-bottom-color: var(--color-primary-dark);
}

/* Spinner (reutilizado de UserBlockchainRecords) */
.spinner {
  animation: rotate 2s linear infinite;
  width: 40px; /* Menor para este contexto */
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
.small-empty-state {
    font-size: var(--fs-base);
    padding: var(--sp-md);
}
</style>