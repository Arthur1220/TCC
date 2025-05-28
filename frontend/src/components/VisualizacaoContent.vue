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
        <button @click="fetchAllSystemData" class="button button-primary button-sm">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
            Tentar Novamente
        </button>
    </div>
    <div v-else> <div v-if="events.length" class="table-responsive-wrapper">
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
            <tr v-for="evt in sortedEvents" :key="evt.id" class="table-row-hover">
              <td data-label="ID Evento">{{ evt.id }}</td>
              <td data-label="Animal">{{ getAnimalIdentification(evt.animal) }}</td>
              <td data-label="Tipo de Evento">{{ getEventTypeName(evt.event_type) }}</td>
              <td data-label="Data">{{ formatDateTime(evt.date) }}</td>
              <td data-label="Localização">{{ evt.location || 'N/A' }}</td>
              <td data-label="Registrado por">{{ evt.recorded_by_username || usersMap[evt.recorded_by]?.username || `ID ${evt.recorded_by}` }}</td>
              <td data-label="Observações" class="truncate-text" :title="evt.observations || ''">{{ evt.observations || 'N/A' }}</td>
              <td data-label="Ações" class="actions-cell">
                <button class="button button-info button-sm" @click="loadAndShowEventDetails(evt)" title="Ver Detalhes">
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
    </div> <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
        <div class="modal-content card large-modal">
            <div class="modal-header">
                <h3 class="modal-title-text">Detalhes Completos do Evento #{{ detailedEvent?.id || selectedEventForModal?.dbBlockchainEntry?.event || 'Desconhecido' }}</h3>
                <button @click="closeDetailsModal" class="button-close" aria-label="Fechar modal">&times;</button>
            </div>
            <div class="modal-body event-details-modal-body">
                <div v-if="isLoadingDetails" class="loading-state modal-loading">
                    <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
                    <p>Carregando detalhes...</p>
                </div>
                <div v-else> 
                    <div v-if="detailedEvent && detailedEvent.id" class="event-details-grid"> <div class="detail-group">
                            <h4>Informações Gerais do Evento</h4>
                            <p><strong>ID do Evento:</strong> <span>{{ detailedEvent.id }}</span></p>
                            <p><strong>Animal:</strong> <span>{{ getAnimalIdentification(detailedEvent.animal) }} (ID: {{ detailedEvent.animal }})</span></p>
                            <p><strong>Tipo de Evento:</strong> <span>{{ getEventTypeName(detailedEvent.event_type) }}</span></p>
                            <p><strong>Data e Hora:</strong> <span>{{ formatDateTime(detailedEvent.date) }}</span></p>
                            <p><strong>Localização:</strong> <span>{{ detailedEvent.location || 'N/A' }}</span></p>
                            <p><strong>Observações:</strong> <span>{{ detailedEvent.observations || 'N/A' }}</span></p>
                            <p><strong>Registrado por:</strong> <span>{{ detailedEvent.recorded_by_username || (usersMap[detailedEvent.recorded_by] ? usersMap[detailedEvent.recorded_by].username : `Usuário ID: ${detailedEvent.recorded_by}`) }}</span></p>
                        </div>

                        <div v-if="detailedEvent.specific_details" class="detail-group specific-details-group">
                            <h4>Detalhes Específicos do Tipo de Evento: {{ getEventTypeName(detailedEvent.event_type) }}</h4>
                            <div v-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('pesagem')">
                                <p><strong>Peso:</strong> <span>{{ detailedEvent.specific_details.weight }} kg</span></p>
                                <p><strong>Data da Pesagem:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.date) }}</span></p>
                            </div>
                            <div v-else-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('movimento')">
                                <p><strong>Propriedade Origem:</strong> <span>{{ getPropertyName(detailedEvent.specific_details.origin_property) }}</span></p>
                                <p><strong>Propriedade Destino:</strong> <span>{{ getPropertyName(detailedEvent.specific_details.destination_property) }}</span></p>
                                <p><strong>Data do Movimento:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.date) }}</span></p>
                                <p><strong>Motivo:</strong> <span>{{ detailedEvent.specific_details.reason || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('vacina')">
                                <p><strong>Nome da Vacina:</strong> <span>{{ detailedEvent.specific_details.name }}</span></p>
                                <p><strong>Dose:</strong> <span>{{ detailedEvent.specific_details.dose }} {{ detailedEvent.specific_details.dose_unit || '' }}</span></p>
                                <p><strong>Fabricante:</strong> <span>{{ detailedEvent.specific_details.manufacturer || 'N/A' }}</span></p>
                                <p><strong>Lote (Vacina):</strong> <span>{{ detailedEvent.specific_details.batch || 'N/A' }}</span></p>
                                <p><strong>Validade da Vacina:</strong> <span>{{ formatDate(detailedEvent.specific_details.validity, true) }}</span></p>
                                <p><strong>Próxima Dose:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.next_dose_date) || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('medica')">
                                <p><strong>Nome do Medicamento:</strong> <span>{{ detailedEvent.specific_details.name }}</span></p>
                                <p><strong>Dose:</strong> <span>{{ detailedEvent.specific_details.dose }} {{ detailedEvent.specific_details.dose_unit || '' }}</span></p>
                                <p><strong>Fabricante:</strong> <span>{{ detailedEvent.specific_details.manufacturer || 'N/A' }}</span></p>
                                <p><strong>Lote (Medicamento):</strong> <span>{{ detailedEvent.specific_details.batch || 'N/A' }}</span></p>
                                <p><strong>Validade do Medicamento:</strong> <span>{{ formatDate(detailedEvent.specific_details.validity, true) }}</span></p>
                                <p><strong>Próxima Dose:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.next_dose_date) || 'N/A' }}</span></p>
                                <p><strong>Motivo/Indicação:</strong> <span>{{ detailedEvent.specific_details.reason || 'N/A' }}</span></p>
                                <p><strong>Período de Carência:</strong> <span>{{ detailedEvent.specific_details.withdrawal_time !== null ? `${detailedEvent.specific_details.withdrawal_time} dias` : 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('reprodu')">
                                <p><strong>Tipo de Reprodução:</strong> <span>{{ detailedEvent.specific_details.reproduction_type }}</span></p>
                                <p><strong>Macho:</strong> <span>{{ getAnimalIdentification(detailedEvent.specific_details.male_id) }}</span></p>
                                <p><strong>Fêmea:</strong> <span>{{ getAnimalIdentification(detailedEvent.specific_details.female_id) }}</span></p>
                                <p><strong>Data da Reprodução:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.date) }}</span></p>
                                <p><strong>Resultado:</strong> <span>{{ detailedEvent.specific_details.result || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('abate')">
                                <p><strong>Data do Abate:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.date) }}</span></p>
                                <p><strong>Local do Abate:</strong> <span>{{ detailedEvent.specific_details.location || 'N/A' }}</span></p>
                                <p><strong>Peso Final:</strong> <span>{{ detailedEvent.specific_details.final_weight }} kg</span></p>
                                <p><strong>Resultado da Inspeção:</strong> <span>{{ detailedEvent.specific_details.inspection_result || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="getEventTypeName(detailedEvent.event_type)?.toLowerCase().includes('ocorrência especial')">
                                <p><strong>Tipo da Ocorrência:</strong> <span>{{ detailedEvent.specific_details.occurrence_type }}</span></p>
                                <p><strong>Data da Ocorrência:</strong> <span>{{ formatDateTime(detailedEvent.specific_details.date) }}</span></p>
                                <p><strong>Descrição:</strong> <span>{{ detailedEvent.specific_details.description || 'N/A' }}</span></p>
                                <p><strong>Ações Tomadas:</strong> <span>{{ detailedEvent.specific_details.actions_taken || 'N/A' }}</span></p>
                            </div>
                            <p v-else>Nenhum detalhe específico adicional para este tipo de evento.</p>
                        </div>
                        <p v-else-if="detailedEvent.event_type_name !== 'Geral' && detailedEvent.event_type_name !== undefined" class="mt-1"> 
                            Este tipo de evento ('{{ detailedEvent.event_type_name }}') não possui detalhes específicos adicionais registrados.
                        </p>
                    </div> <div v-else-if="detailedEvent && detailedEvent.error_message" class="alert alert-danger"> <p>{{ detailedEvent.error_message }}</p>
                    </div>
                    <div v-else class="empty-state small-empty-state"> <p>Não foi possível carregar os detalhes do evento.</p>
                    </div>
                </div> </div> <div class="modal-actions form-actions">
              <button class="button button-secondary" @click="closeDetailsModal">Fechar</button>
            </div>
        </div>
    </div> <NotificationModal
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
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'VisualizacaoContent',
  components: {
    NotificationModal,
  },
  setup() {
    const events = ref([]);
    const eventTypes = ref([]);
    const animals = ref([]); 
    const properties = ref([]);
    const users = ref([]); 

    const animalMap = computed(() => {
        return animals.value.reduce((map, animal) => {
            map[animal.id] = animal.identification;
            return map;
        }, {});
    });
    const usersMap = computed(() => { 
        return users.value.reduce((map, user) => {
            map[user.id] = user; 
            return map;
        }, {});
    });

    const detailedEvent = ref(null);
    const showDetailsModal = ref(false);
    const isLoading = ref(true); 
    const isLoadingDetails = ref(false);
    const fetchError = ref(null); 

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
        console.log("[DEBUG] VisualizacaoContent: Iniciando fetchAllSystemData...");
        const [eventsData, eventTypesData, animalsData, propertiesData, usersData] = await Promise.all([
          getEvents(), 
          getEventTypes(),
          getAnimals(), 
          getProperties(),
          getAllUsers() 
        ]);
        
        console.log("[DEBUG] VisualizacaoContent: Dados brutos recebidos:", { eventsData: eventsData?.length, eventTypesData: eventTypesData?.length, animalsData: animalsData?.length, propertiesData: propertiesData?.length, usersData: usersData?.length });

        eventTypes.value = eventTypesData || [];
        animals.value = animalsData || [];
        properties.value = propertiesData || [];
        users.value = usersData || []; 

        console.log("[DEBUG] VisualizacaoContent: users.value (primeiros 5):", JSON.stringify(users.value.slice(0,5)));
        console.log("[DEBUG] VisualizacaoContent: usersMap.value (exemplo):", users.value.length > 0 ? JSON.stringify(usersMap.value[users.value[0].id]) : "Mapa vazio");

        if (eventsData && Array.isArray(eventsData)) {
            events.value = eventsData.map(evt => {
                let recorderUsername = `ID ${evt.recorded_by}`; 
                if (evt.recorded_by !== null && evt.recorded_by !== undefined) {
                    const recorder = usersMap.value[evt.recorded_by];
                    if (recorder && recorder.username) {
                        recorderUsername = recorder.username;
                    } else if (recorder) { // Usuário existe no mapa mas não tem username (improvável se UserSerializer estiver ok)
                        recorderUsername = `Usuário ID ${evt.recorded_by} (s/ username)`;
                    } else {
                        // console.warn(`[DEBUG] Usuário com ID ${evt.recorded_by} não encontrado no usersMap para o evento ID ${evt.id}`);
                    }
                } else {
                    recorderUsername = 'N/D (Não especificado)';
                }
                return {
                    ...evt,
                    recorded_by_username: recorderUsername
                };
            });
            console.log("[DEBUG] VisualizacaoContent: events.value mapeados (primeiro):", events.value.length > 0 ? JSON.stringify(events.value[0]) : "Nenhum evento");
        } else {
            events.value = [];
            console.warn("[DEBUG] VisualizacaoContent: eventsData não é um array ou está indefinido.");
        }

      } catch (e) {
        // A linha 222 do erro original é provavelmente o .map() acima ou a atribuição a events.value
        console.error("Erro ao carregar dados para VisualizacaoContent (linha ~222 no seu original):", e);
        fetchError.value = `Falha ao carregar dados: ${e.message || 'Verifique o console para mais detalhes.'}`;
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
    
    const formatDateTime = (dateTimeString) => { /* ... (como antes) ... */ };
    const formatDate = (dateString, isDateOnly = false) => { /* ... (como antes) ... */ };

    const loadAndShowEventDetails = async (eventSummary) => { /* ... (como antes, mas verifique o mapeamento de recorded_by_username) ... */ 
        isLoadingDetails.value = true;
        detailedEvent.value = null; 
        showDetailsModal.value = true;
        try {
            const fullDetails = await getEventDetails(eventSummary.id, eventSummary.event_type);
            detailedEvent.value = {
                ...fullDetails, 
                animal_identification: getAnimalIdentification(fullDetails.animal),
                event_type_name: getEventTypeName(fullDetails.event_type),
                // Usa o usersMap para buscar o nome do usuário que registrou
                recorded_by_username: usersMap.value[fullDetails.recorded_by]?.username || `Usuário ID: ${fullDetails.recorded_by}`,
                specific_details: fullDetails.details || null 
            };
        } catch (error) {
            console.error(`Erro ao buscar detalhes do evento ID ${eventSummary.id}:`, error.response?.data || error);
            showAppNotification(`Erro ao carregar detalhes do evento #${eventSummary.id}.`, 'error');
            detailedEvent.value = { 
                id: eventSummary.id, 
                error_message: "Falha ao carregar detalhes completos." 
            };
        } finally {
            isLoadingDetails.value = false;
        }
    };

    const closeDetailsModal = () => { /* ... (como antes) ... */ };
    const formatDetailKey = (key) => { /* ... (como antes) ... */ };
    const formatDetailValue = (key, value, eventType = null) => { /* ... (como antes) ... */ };

    onMounted(fetchAllSystemData);

    const sortedEvents = computed(() => {
        return [...events.value].sort((a, b) => new Date(b.date) - new Date(a.date));
    });

    return {
      events,
      sortedEvents,
      isLoading,
      fetchError,
      detailedEvent,
      showDetailsModal,
      isLoadingDetails,
      getEventTypeName,
      getAnimalIdentification,
      formatDateTime,
      formatDate,
      loadAndShowEventDetails,
      closeDetailsModal,
      formatDetailKey,
      formatDetailValue,
      fetchAllSystemData,
      notification,
      showAppNotification,
      closeNotification,
      usersMap, 
      getPropertyName
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