<template>
  <div class="admin-event-viewer-content content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Visualização de Todos os Eventos do Sistema</h2>
    </div>
    <p class="panel-description">
      Acompanhe e audite todos os eventos registrados na plataforma. Clique em "Detalhes" para ver informações completas de cada evento, incluindo os dados da blockchain quando disponíveis.
    </p>

    <div v-if="isLoading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>Carregando todos os eventos...</p>
    </div>
    <div v-else-if="fetchError" class="empty-state card alert alert-danger">
        <h4 class="alert-heading">Erro ao Carregar Eventos</h4>
        <p>{{ fetchError }}</p>
        <button @click="fetchAllSystemData" class="button button-primary button-sm">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
            Tentar Novamente
        </button>
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
              <th>Registrado por</th>
              <th class="th-observations">Observações</th>
              <th class="text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="evt in sortedEvents" 
                :key="evt.id" 
                class="table-row-hover"
                @click="loadAndShowEventDetails(evt)"
                tabindex="0"
                role="button"
                :aria-label="`Visualizar detalhes do evento ${evt.id} para ${getAnimalIdentification(evt.animal)}`">
              <td data-label="ID Evento">{{ evt.id }}</td>
              <td data-label="Animal">{{ getAnimalIdentification(evt.animal) }}</td>
              <td data-label="Tipo de Evento">{{ getEventTypeName(evt.event_type) }}</td>
              <td data-label="Data">{{ formatDateTime(evt.date) }}</td>
              <td data-label="Localização">{{ evt.location || 'N/A' }}</td>
              <td data-label="Registrado por">{{ evt.recorded_by_username || usersMap[evt.recorded_by]?.username || `ID ${evt.recorded_by}` }}</td>
              <td data-label="Observações" class="truncate-text" :title="evt.observations || ''">{{ evt.observations || 'N/A' }}</td>
              <td data-label="Ações" class="actions-cell">
                <button class="button button-info button-sm" @click.stop="loadAndShowEventDetails(evt)" title="Ver Detalhes">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 4C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 12.5c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                  Detalhes
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state card">
        <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
        <h4 class="empty-state-title">Nenhum evento encontrado no sistema.</h4>
        <p class="muted-text">Quando eventos forem registrados, eles aparecerão aqui.</p>
      </div>
    </div>

    <div v-if="showDetailedEventViewerModal" class="modal-overlay" @click.self="closeDetailedEventViewerModal">
      <div v-if="isLoadingEventDetailsForViewer" class="modal-content card large-modal loading-state" style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 200px;">
          <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
          <p>Carregando detalhes completos do evento...</p>
      </div>
      <EventDetailViewer
        v-else-if="eventDataForViewer && !eventDataForViewer.error_message"
        class="modal-content card large-modal" 
        :event-data="eventDataForViewer"
        :animals-list="animals"        
        :properties-list="properties" 
        :event-types-list="eventTypes"  
        title="Detalhes Completos do Evento" 
        :show-close-button-in-header="true"
        @close="closeDetailedEventViewerModal"
      />
      <div v-else-if="eventDataForViewer && eventDataForViewer.error_message" class="modal-content card large-modal">
          <div class="modal-header">
              <h3 class="modal-title-text">Erro ao Carregar Detalhes</h3>
              <button @click="closeDetailedEventViewerModal" class="button-close" aria-label="Fechar modal">&times;</button>
          </div>
          <div class="modal-body" style="padding: 20px; text-align: center;">
              <p class="text-danger">{{ eventDataForViewer.error_message }}</p>
          </div>
           <div class="form-actions full-width" style="padding: 1rem; border-top: 1px solid #eee; text-align: right;">
              <button class="button button-secondary" @click="closeDetailedEventViewerModal">Fechar</button>
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
import { getEvents, getEventDetails } from '@/services/eventService';
import { getEventTypes, getProperties } from '@/services/lookupService';
import { getAnimals } from '@/services/animalService'; 
import { getAllUsers } from '@/services/userService';
import { filterBlockchain } from '@/services/blockchainService'; // Importar filterBlockchain
import NotificationModal from '@/components/NotificationModal.vue';
import EventDetailViewer from '@/components/EventDetailViewer.vue'; // Importar o novo componente

export default {
  name: 'VisualizacaoContent',
  components: {
    NotificationModal,
    EventDetailViewer // Registrar o componente
  },
  setup() {
    const events = ref([]);
    const eventTypes = ref([]);
    const animals = ref([]); 
    const properties = ref([]);
    const users = ref([]); 

    const isLoading = ref(true); 
    const fetchError = ref(null); 
    const notification = ref({ show: false, message: '', type: 'success' });

    // Estados para o modal do EventDetailViewer
    const showDetailedEventViewerModal = ref(false);
    const eventDataForViewer = ref(null);
    const isLoadingEventDetailsForViewer = ref(false);

    const animalMap = computed(() => {
        return animals.value.reduce((map, animal) => {
            map[animal.id] = animal.identification || `ID ${animal.id}`;
            return map;
        }, {});
    });
    const usersMap = computed(() => { 
        return users.value.reduce((map, user) => {
            map[user.id] = user; 
            return map;
        }, {});
    });

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
        const [eventsData, eventTypesData, animalsData, propertiesData, usersData] = await Promise.all([
          getEvents(), 
          getEventTypes(),
          getAnimals(), 
          getProperties(),
          getAllUsers() 
        ]);
        
        eventTypes.value = eventTypesData || [];
        animals.value = animalsData || [];
        properties.value = propertiesData || [];
        users.value = usersData || []; 

        if (eventsData && Array.isArray(eventsData)) {
            events.value = eventsData.map(evt => ({
                ...evt,
                recorded_by_username: usersMap.value[evt.recorded_by]?.username || `ID ${evt.recorded_by}`
            }));
        } else {
            events.value = [];
        }
      } catch (e) {
        console.error("Erro ao carregar dados para VisualizacaoContent:", e.response?.data || e.message);
        fetchError.value = `Falha ao carregar dados do sistema: ${e.message || 'Verifique o console.'}`;
        showAppNotification(fetchError.value, 'error');
      } finally {
        isLoading.value = false;
      }
    };

    const getEventTypeName = (eventTypeId) => {
      if (eventTypeId === null || eventTypeId === undefined) return 'N/D';
      const type = eventTypes.value.find(t => t.id === Number(eventTypeId));
      return type ? type.name : `ID ${eventTypeId}`;
    };

    const getAnimalIdentification = (animalId) => {
        if (animalId === null || animalId === undefined) return 'N/D';
        return animalMap.value[Number(animalId)] || `ID ${animalId}`;
    };
    
    const getPropertyName = (propertyId) => {
        if (propertyId === null || propertyId === undefined) return 'N/A';
        const prop = properties.value.find(p => p.id === Number(propertyId));
        return prop ? prop.name : `ID ${propertyId}`;
    };
    
    const formatDateTime = (dateTimeString) => {
      if (!dateTimeString) return 'N/A';
      try {
        const date = new Date(dateTimeString);
         if (isNaN(date.getTime())) return 'Data Inválida';
        return date.toLocaleString('pt-BR', {
          day: '2-digit', month: '2-digit', year: 'numeric',
          hour: '2-digit', minute: '2-digit'
        });
      } catch (e) { return dateTimeString; }
    };
    const formatDate = (dateString, isDateOnly = true) => { // Ajustado para o formato do EventDetailViewer
        if (!dateString) return 'N/A';
        try {
            const date = new Date(dateString.length === 10 && dateString.includes('-') ? dateString + 'T00:00:00Z' : dateString);
            if (isNaN(date.getTime())) return 'Data Inválida';
            
            const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
            if (isDateOnly) options.timeZone = 'UTC'; // Se for apenas data, considera UTC para evitar problemas de fuso

            if (!isDateOnly) { // Se não for apenas data, assume que é datetime e formata localmente
                 delete options.timeZone; // Usa o fuso local
                 options.hour = '2-digit';
                 options.minute = '2-digit';
                 return date.toLocaleString('pt-BR', options);
            }
            return date.toLocaleDateString('pt-BR', options);
        } catch (e) { return "Data Inválida"; }
    };

    // MÉTODO MODIFICADO PARA USAR O NOVO MODAL E BUSCAR DADOS DA BLOCKCHAIN
    const loadAndShowEventDetails = async (eventSummary) => {
      if (!eventSummary || eventSummary.id == null || eventSummary.event_type == null) {
        showAppNotification("Dados do evento inválidos para visualização.", "error");
        return;
      }

      isLoadingEventDetailsForViewer.value = true;
      eventDataForViewer.value = null; 
      showDetailedEventViewerModal.value = true; 

      try {
        const fullEventDetailsFromDB = await getEventDetails(eventSummary.id, eventSummary.event_type);

        if (!fullEventDetailsFromDB) {
          showAppNotification('Erro: Detalhes do evento não encontrados no banco de dados.', 'error');
          closeDetailedEventViewerModal();
          return;
        }

        let blockchainEntry = null;
        try {
          const blockchainEntries = await filterBlockchain({ event: eventSummary.id });
          if (blockchainEntries && blockchainEntries.length > 0) {
            blockchainEntry = blockchainEntries[0];
          }
        } catch (bcError) {
          console.error(`[VisualizacaoContent] Erro ao buscar registro blockchain para evento ${eventSummary.id}:`, bcError);
        }
        
        eventDataForViewer.value = {
          dbEventDetails: {
            ...fullEventDetailsFromDB,
            animal_identification: getAnimalIdentification(fullEventDetailsFromDB.animal),
            event_type_name: getEventTypeName(fullEventDetailsFromDB.event_type),
            recorded_by_username: usersMap.value[fullEventDetailsFromDB.recorded_by]?.username || `ID ${fullEventDetailsFromDB.recorded_by}`,
            details: fullEventDetailsFromDB.details || {}
          },
          dbBlockchainEntry: blockchainEntry,
          blockchainData: null, // Não aplicável neste contexto
          contextualAnimalInfo: {
              identification: getAnimalIdentification(fullEventDetailsFromDB.animal),
              id: fullEventDetailsFromDB.animal
          }
        };
        
      } catch (error) {
        console.error("Erro ao carregar detalhes completos do evento:", error);
        showAppNotification("Falha ao carregar detalhes completos do evento.", "error");
        eventDataForViewer.value = { 
            dbEventDetails: null, 
            dbBlockchainEntry: null, 
            error_message: 'Falha ao carregar dados do evento.'
        };
      } finally {
        isLoadingEventDetailsForViewer.value = false;
      }
    };

    const closeDetailedEventViewerModal = () => {
      showDetailedEventViewerModal.value = false;
      eventDataForViewer.value = null;
      isLoadingEventDetailsForViewer.value = false;
    };
    
    // Funções formatDetailKey e formatDetailValue não são mais necessárias aqui,
    // pois são responsabilidade do EventDetailViewer.

    onMounted(fetchAllSystemData);

    const sortedEvents = computed(() => {
        return [...events.value].sort((a, b) => new Date(b.date) - new Date(a.date));
    });

    return {
      events,
      sortedEvents,
      isLoading,
      fetchError,
      // Para o EventDetailViewer
      showDetailedEventViewerModal,
      eventDataForViewer,
      isLoadingEventDetailsForViewer,
      loadAndShowEventDetails,
      closeDetailedEventViewerModal,
      // Funções de lookup/formatação que o template principal ou o mapeamento para EventDetailViewer podem precisar
      getEventTypeName,
      getAnimalIdentification,
      formatDateTime,
      formatDate, // Mantido para uso geral se necessário
      getPropertyName,
      usersMap, 
      // Notificações e carregamento inicial
      notification,
      showAppNotification,
      closeNotification,
      fetchAllSystemData,
      // Passando as listas para o EventDetailViewer
      animals,
      properties,
      eventTypes
    };
  }
};
</script>

<style scoped>
/* SEU CSS SCOPED EXISTENTE ... */
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

.loading-state, .empty-state {
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
}
.empty-state.card { 
    background-color: var(--color-bg-muted);
}
.alert.alert-danger {
    background-color: #f8d7da; 
    color: #721c24; 
    border-color: #f5c6cb; 
    padding: var(--sp-md);
}
.alert-heading {
    color: inherit; 
    margin-bottom: var(--sp-sm);
}
.loading-state .spinner {
    margin-bottom: var(--sp-sm);
}

.table-responsive-wrapper {
  overflow-x: auto;
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-bg-component);
  box-shadow: var(--shadow-sm);
}
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

.event-details-modal-body {
    text-align: left;
    font-size: var(--fs-base);
    max-height: 70vh;
    overflow-y: auto;
    padding-right: var(--sp-sm); 
}
.event-details-grid {
    display: grid;
    grid-template-columns: 1fr; 
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
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}
.detail-group p strong, .specific-detail-item p strong {
    color: var(--color-text-primary);
    font-weight: var(--fw-medium);
    min-width: 180px; 
    margin-right: var(--sp-sm);
    flex-shrink: 0;
    text-align: left;
}
.detail-group p span:not(strong), .specific-detail-item p span:not(strong) {
    text-align: right;
    word-break: break-word;
    flex-grow: 1;
}
.specific-details-group {
    background-color: var(--color-primary-light); 
    border-color: var(--color-primary);
}
.specific-details-group h4 {
    color: var(--color-primary-dark);
    border-bottom-color: var(--color-primary-dark);
}
.modal-actions.form-actions { 
    padding-top: var(--sp-md);
    margin-top: var(--sp-lg);
    border-top: 1px solid var(--color-border-light);
    display: flex;
    justify-content: flex-end;
}

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
.small-empty-state {
    font-size: var(--fs-base);
    padding: var(--sp-md);
}
.modal-loading p {
    font-size: var(--fs-large);
    color: var(--color-text-muted);
}
</style>