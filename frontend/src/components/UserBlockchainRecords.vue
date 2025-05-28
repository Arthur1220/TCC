<template>
  <div class="user-blockchain-records-panel content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Meus Registros na Blockchain</h2>
    </div>
    <p class="panel-description">
      Consulte o histórico imutável dos eventos dos seus animais registrados em nossa blockchain, garantindo transparência e auditabilidade.
    </p>

    <div v-if="isLoading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>Carregando seus registros da blockchain...</p>
    </div>
    <div v-else-if="errorLoading" class="empty-state card alert alert-danger">
      <h4 class="alert-heading">Erro ao Carregar Registros</h4>
      <p>Não foi possível buscar seus registros da blockchain no momento.</p>
      <p>{{ errorMessage || 'Por favor, tente novamente mais tarde.' }}</p>
      <button @click="loadUserRecords" class="button button-primary button-sm">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
        Tentar Novamente
      </button>
    </div>
    <div v-else-if="userRecords.length === 0" class="empty-state card">
      <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" viewBox="0 0 24 24" fill="currentColor" width="64" height="64"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 16H6c-.55 0-1-.45-1-1V6c0-.55.45-1 1-1h12c.55 0 1 .45 1 1v12c0 .55-.45 1-1 1zm-5-3H8v-2h5v2zm3-4H8v-2h8v2zm0-4H8V7h8v2z"/></svg>
      <h4 class="empty-state-title">Nenhum Registro Encontrado</h4>
      <p>Você ainda não possui registros de eventos na blockchain.</p>
      <p class="muted-text">Eventos importantes dos seus animais serão registrados aqui para garantir a trilha de auditoria.</p>
    </div>

    <div v-else class="records-list-container">
      <div class="records-summary">
        <p>Exibindo <strong>{{ userRecords.length }}</strong> registro(s) na blockchain.</p>
      </div>
      <ul class="records-list">
        <li v-for="record in userRecords" :key="record.id || record.transaction_hash" class="record-item card">
          <div class="record-header">
            <h4 class="record-id-title">Registro DB ID: {{ record.id }}</h4>
            <span class="record-timestamp">{{ formatDate(record.registration_date) }}</span>
          </div>
          <div class="record-body">
            <div class="record-field">
              <span class="record-label">Animal:</span>
              <span class="record-value">{{ record.animal_details?.identification || getAnimalIdentificationFromList(record.animal) || `ID ${record.animal}` }}</span>
            </div>
            <div class="record-field">
              <span class="record-label">Tipo de Evento:</span>
              <span class="record-value">{{ getEventTypeName(record.event_details?.event_type) || 'N/D' }}</span>
            </div>
            <div class="record-field">
                <span class="record-label">Data do Evento (BD):</span>
                <span class="record-value">{{ formatEventDate(record.event_details?.date) }}</span>
            </div>
            <div class="record-field">
                <span class="record-label">Localização (BD):</span>
                <span class="record-value">{{ record.event_details?.location || 'N/A' }}</span>
            </div>
            <div class="record-field">
                <span class="record-label">Status na Blockchain:</span>
                <span :class="getBlockchainStatusClass(record.status_details?.name)" class="status-badge">
                    {{ record.status_details?.name || `ID ${record.status}` || 'Desconhecido' }}
                </span>
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
          <div class="record-footer">
            <button class="button button-outline-primary button-sm" @click="openDetailsModal(record)">
              Ver Detalhes Completos
            </button>
          </div>
        </li>
      </ul>
    </div>

    <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
        <div class="modal-content card large-modal">
            <div class="modal-header">
                <h3 class="modal-title-text">Detalhes do Evento Registrado na Blockchain</h3>
                <button @click="closeDetailsModal" class="button-close" aria-label="Fechar modal">&times;</button>
            </div>
            <div class="modal-body event-details-modal-body">
                <div v-if="isLoadingModalDetails" class="loading-state modal-loading">
                    <p>Carregando detalhes completos do evento...</p>
                </div>
                <div v-else-if="selectedRecordForModal && modalEventDetails">
                    
                    <h4>Dados do Banco de Dados (Evento Original)</h4>
                    <div v-if="modalEventDetails.id" class="details-section">
                        <p><strong>ID do Evento (BD):</strong> <span>{{ modalEventDetails.id }}</span></p>
                        <p><strong>Animal (BD):</strong> <span>{{ modalEventDetails.animal_identification }} (ID: {{ modalEventDetails.animal }})</span></p>
                        <p><strong>Tipo (BD):</strong> <span>{{ modalEventDetails.event_type_name }} (ID: {{ modalEventDetails.event_type }})</span></p>
                        <p><strong>Data (BD):</strong> <span>{{ formatEventDate(modalEventDetails.date) }}</span></p>
                        <p><strong>Localização (BD):</strong> <span>{{ modalEventDetails.location || 'N/A' }}</span></p>
                        <p><strong>Observações (BD):</strong> <span>{{ modalEventDetails.observations || 'N/A' }}</span></p>
                        <p><strong>Registrado por (BD):</strong> <span>{{ modalEventDetails.recorded_by_username || 'N/A' }}</span></p>
                        
                        <div v-if="modalEventDetails.details" class="specific-details mt-1 card">
                            <h5 class="details-subtitle">Detalhes Específicos ({{modalEventDetails.event_type_name}}):</h5>
                            <div v-if="modalEventDetails.event_type_name?.toLowerCase().includes('pesagem')">
                                <p><strong>Peso:</strong> <span>{{ modalEventDetails.details.weight }} kg</span></p>
                            </div>
                            <div v-else-if="modalEventDetails.event_type_name?.toLowerCase().includes('movimento')">
                                <p><strong>Origem:</strong> <span>{{ getPropertyName(modalEventDetails.details.origin_property) }}</span></p>
                                <p><strong>Destino:</strong> <span>{{ getPropertyName(modalEventDetails.details.destination_property) }}</span></p>
                                <p><strong>Motivo:</strong> <span>{{ modalEventDetails.details.reason || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="modalEventDetails.event_type_name?.toLowerCase().includes('vacina')">
                                <p><strong>Vacina:</strong> <span>{{ modalEventDetails.details.name }}</span></p>
                                <p><strong>Dose:</strong> <span>{{ modalEventDetails.details.dose }} {{ modalEventDetails.details.dose_unit || '' }}</span></p>
                                <p><strong>Fabricante:</strong> <span>{{ modalEventDetails.details.manufacturer || 'N/A' }}</span></p>
                                <p><strong>Lote:</strong> <span>{{ modalEventDetails.details.batch || 'N/A' }}</span></p>
                                <p><strong>Validade:</strong> <span>{{ formatDate(modalEventDetails.details.validity, true) }}</span></p>
                            </div>
                            <div v-else-if="modalEventDetails.event_type_name?.toLowerCase().includes('medica')">
                                <p><strong>Medicamento:</strong> <span>{{ modalEventDetails.details.name }}</span></p>
                                <p><strong>Dose:</strong> <span>{{ modalEventDetails.details.dose }} {{ modalEventDetails.details.dose_unit || '' }}</span></p>
                                <p><strong>Motivo:</strong> <span>{{ modalEventDetails.details.reason || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="modalEventDetails.event_type_name?.toLowerCase().includes('reprodu')">
                                <p><strong>Tipo Reprodução:</strong> <span>{{ modalEventDetails.details.reproduction_type }}</span></p>
                                <p><strong>Macho:</strong> <span>{{ getAnimalIdentificationFromList(modalEventDetails.details.male_id) }}</span></p>
                                <p><strong>Fêmea:</strong> <span>{{ getAnimalIdentificationFromList(modalEventDetails.details.female_id) }}</span></p>
                                <p><strong>Resultado:</strong> <span>{{ modalEventDetails.details.result || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="modalEventDetails.event_type_name?.toLowerCase().includes('abate')">
                                <p><strong>Local Abate:</strong> <span>{{ modalEventDetails.details.location }}</span></p>
                                <p><strong>Peso Final:</strong> <span>{{ modalEventDetails.details.final_weight }} kg</span></p>
                                <p><strong>Inspeção:</strong> <span>{{ modalEventDetails.details.inspection_result || 'N/A' }}</span></p>
                            </div>
                            <div v-else-if="modalEventDetails.event_type_name?.toLowerCase().includes('ocorrência especial')">
                                <p><strong>Tipo Ocorrência:</strong> <span>{{ modalEventDetails.details.occurrence_type }}</span></p>
                                <p><strong>Descrição:</strong> <span>{{ modalEventDetails.details.description || 'N/A' }}</span></p>
                                <p><strong>Ações Tomadas:</strong> <span>{{ modalEventDetails.details.actions_taken || 'N/A' }}</span></p>
                            </div>
                            <pre v-else-if="typeof modalEventDetails.details === 'object'">{{ JSON.stringify(modalEventDetails.details, null, 2) }}</pre>
                            <p v-else>Nenhum detalhe específico adicional registrado.</p>
                        </div>
                        <p v-else-if="modalEventDetails.event_type_name !== 'Geral' && modalEventDetails.event_type_name !== undefined" class="mt-1"> 
                            Este tipo de evento ('{{ modalEventDetails.event_type_name }}') não possui detalhes específicos adicionais registrados.
                        </p>
                    </div>
                    <div v-else-if="modalEventDetails.error" class="alert alert-danger">
                        <p>{{ modalEventDetails.error }}</p>
                    </div>
                    <p v-else> 
                        Não foi possível carregar os detalhes completos do evento do banco de dados.
                    </p>

                    <hr class="my-1">

                    <h4>Dados do Registro na Blockchain</h4>
                    <div v-if="selectedRecordForModal.dbBlockchainEntry" class="details-section">
                        <p><strong>ID do Registro (BC no DB):</strong> <span>{{ selectedRecordForModal.dbBlockchainEntry.id }}</span></p>
                        <p><strong>Hash da Transação:</strong> <span class="data-hash">{{ selectedRecordForModal.dbBlockchainEntry.transaction_hash }}</span></p>
                        <p><strong>Data de Registro (BC no DB):</strong> <span>{{ formatDate(selectedRecordForModal.dbBlockchainEntry.registration_date) }}</span></p>
                        <p><strong>Status (BC no DB):</strong> <span :class="getBlockchainStatusClass(selectedRecordForModal.dbBlockchainEntry.status_details?.name)" class="status-badge">{{ selectedRecordForModal.dbBlockchainEntry.status_details?.name || 'N/D' }}</span></p>
                        <p><strong>Proprietário do Registro (BD):</strong> <span>{{ selectedRecordForModal.dbBlockchainEntry.owner_details?.username || 'N/D' }}</span></p>
                    </div>
                    <p v-else>Dados da blockchain não disponíveis para este registro (entrada no DB).</p>
                </div>
                <div v-else>
                    <p class="text-center muted-text p-1">Selecione um registro para ver os detalhes ou ocorreu um erro ao carregar as informações.</p>
                </div>
            </div>
            <div class="form-actions full-width modal-footer-custom">
                <button type="button" class="button button-secondary" @click="closeDetailsModal">Fechar</button>
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
import { ref, onMounted } from 'vue'; // Removido computed se não usado diretamente no setup
import { filterBlockchain } from '@/services/blockchainService';
import { getUserProfile } from '@/services/userService';
import { getEventDetails } from '@/services/eventService';
import { getEventTypes, getProperties } from '@/services/lookupService';
import { getAnimals } from '@/services/animalService';
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
    const errorMessage = ref('');
    const notification = ref({ show: false, message: '', type: 'success' });

    const showDetailsModal = ref(false);
    const selectedRecordForModal = ref(null);
    const modalEventDetails = ref(null);
    const isLoadingModalDetails = ref(false);

    const eventTypes = ref([]);
    const animalsListForLookup = ref([]);
    const properties = ref([]);

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

    const loadLookupData = async () => {
        try {
            // console.log("UserBlockchainRecords: Carregando dados de lookup...");
            const [fetchedEventTypes, fetchedAnimals, fetchedProperties] = await Promise.all([
                getEventTypes(),
                getAnimals(), 
                getProperties()
            ]);
            eventTypes.value = fetchedEventTypes;
            animalsListForLookup.value = fetchedAnimals;
            properties.value = fetchedProperties;
            // console.log("UserBlockchainRecords: Dados de lookup carregados.", { types: eventTypes.value.length, animals: animalsListForLookup.value.length });
        } catch (error) {
            console.error("Erro ao carregar dados de lookup (UserBlockchainRecords):", error);
            showAppNotification("Erro ao carregar dados de referência (tipos, animais, propriedades).", "warning");
        }
    };

    const loadUserRecords = async () => {
      isLoading.value = true;
      errorLoading.value = false;
      errorMessage.value = '';
      userRecords.value = [];

      if (!currentUser.value?.id) { // Garante que currentUser foi carregado e tem ID
        isLoading.value = false;
        // fetchCurrentUser já mostra notificação e seta errorLoading
        return; 
      }

      try {
        // console.log(`UserBlockchainRecords: Buscando registros para owner ID: ${currentUser.value.id}`);
        const records = await filterBlockchain({ owner: currentUser.value.id }); 
        // console.log("UserBlockchainRecords: Registros recebidos do backend:", records);
        userRecords.value = records.sort((a, b) => 
            new Date(b.registration_date || 0) - new Date(a.registration_date || 0)
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

    const formatDate = (dateInput, onlyDate = false) => {
      if (!dateInput) return 'N/A';
      let date;
      if (typeof dateInput === 'number' || (typeof dateInput === 'string' && /^\d+$/.test(dateInput))) {
        date = new Date(Number(dateInput) * 1000);
      } else {
        date = new Date(dateInput);
      }
      if (isNaN(date.getTime())) return 'Data Inválida';
      
      const options = {
        day: '2-digit', month: '2-digit', year: 'numeric',
      };
      if (!onlyDate) {
        options.hour = '2-digit';
        options.minute = '2-digit';
      }
      return date.toLocaleString('pt-BR', options);
    };
    
    const formatEventDate = (dateInput) => {
        return formatDate(dateInput, false);
    };

    const getBlockchainStatusClass = (statusName) => {
        if (!statusName) return 'status-default';
        const statusLower = String(statusName).toLowerCase();
        if (statusLower === 'confirmado') return 'status-success';
        if (statusLower === 'pendente') return 'status-warning';
        if (statusLower === 'falhou') return 'status-danger';
        return 'status-info';
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

    const getEventTypeName = (eventTypeId) => {
        if (eventTypeId === null || eventTypeId === undefined) return 'N/D (Tipo Inválido)';
        const type = eventTypes.value.find(t => t.id === Number(eventTypeId));
        return type ? type.name : `ID ${eventTypeId}`;
    };

    const getAnimalIdentificationFromList = (animalId) => {
        if (animalId === null || animalId === undefined) return 'N/D (Animal Inválido)';
        const animal = animalsListForLookup.value.find(a => a.id === Number(animalId));
        return animal ? animal.identification : `ID ${animalId}`;
    };
    
    const getPropertyName = (propertyId) => {
        if (propertyId === null || propertyId === undefined) return 'N/A';
        const prop = properties.value.find(p => p.id === Number(propertyId));
        return prop ? prop.name : `ID ${propertyId}`;
    };

    const openDetailsModal = async (record) => {
        selectedRecordForModal.value = {
            dbBlockchainEntry: record 
        };
        isLoadingModalDetails.value = true;
        showDetailsModal.value = true;
        modalEventDetails.value = null;

        const eventIdInDb = record.event_details?.id || record.event; // ID do evento no DB
        const eventTypeIdInDb = record.event_details?.event_type;

        if (eventIdInDb && eventTypeIdInDb !== undefined && eventTypeIdInDb !== null) {
            try {
                // console.log(`UserBlockchainRecords: Buscando detalhes completos para Evento DB ID: ${eventIdInDb}, Tipo ID: ${eventTypeIdInDb}`);
                const fullDetails = await getEventDetails(eventIdInDb, eventTypeIdInDb);
                // console.log("UserBlockchainRecords: Detalhes completos recebidos:", fullDetails);
                modalEventDetails.value = {
                    ...fullDetails,
                    animal_identification: getAnimalIdentificationFromList(fullDetails.animal),
                    event_type_name: getEventTypeName(fullDetails.event_type),
                    recorded_by_username: fullDetails.recorded_by_username || (fullDetails.recorded_by ? `Usuário ID ${fullDetails.recorded_by}` : 'N/D'),
                };

            } catch (error) {
                console.error("Erro ao buscar detalhes completos do evento para o modal:", error);
                showAppNotification("Falha ao carregar detalhes completos do evento.", "error");
                modalEventDetails.value = { error: "Não foi possível carregar os detalhes completos do evento do banco de dados." };
            }
        } else {
            console.warn("UserBlockchainRecords: Não foi possível buscar detalhes: ID do evento ou tipo do evento ausente.", record);
            modalEventDetails.value = { error: "Informações insuficientes no registro da blockchain para buscar detalhes completos do evento no banco de dados." };
        }
        isLoadingModalDetails.value = false;
    };

    const closeDetailsModal = () => {
        showDetailsModal.value = false;
        selectedRecordForModal.value = null;
        modalEventDetails.value = null;
    };

    onMounted(async () => {
        isLoading.value = true; // Garante que o loading principal seja ativado
        await fetchCurrentUser(); 
        await loadLookupData();   
        // loadUserRecords só será chamado se fetchCurrentUser for bem-sucedido e tiver ID
        if (currentUser.value && currentUser.value.id) {
            await loadUserRecords();  
        } else {
            isLoading.value = false; // Se não há usuário, não há o que carregar
        }
    });

    return {
      userRecords,
      isLoading,
      errorLoading,
      errorMessage,
      loadUserRecords,
      formatDate,
      formatEventDate,
      getBlockchainStatusClass,
      copyToClipboard,
      notification,
      closeNotification,
      // Modal
      showDetailsModal,
      selectedRecordForModal,
      modalEventDetails,
      isLoadingModalDetails,
      openDetailsModal,
      closeDetailsModal,
      // Helpers
      getEventTypeName,
      getAnimalIdentificationFromList,
      getPropertyName
    };
  }
};
</script>

<style scoped>
/* Seu CSS Scoped Existente ... */
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
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
  margin-top: var(--sp-lg);
}
.loading-state p, .empty-state p {
    color: var(--color-text-muted);
    margin-bottom: var(--sp-sm);
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
  grid-template-columns: 1fr; 
  gap: var(--sp-md);
}

.record-item {
  padding: var(--sp-md);
  transition: var(--transition-base);
}
.record-item:hover {
    border-color: var(--color-primary-light);
    box-shadow: var(--shadow); 
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--sp-md); 
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) dashed var(--color-border);
}
.record-id-title { 
  font-size: var(--fs-base); /* Ajustado para título do card */
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
  justify-content: space-between; 
  align-items: flex-start; 
  margin-bottom: var(--sp-xs); /* Reduzido espaço entre campos */
  padding: calc(var(--sp-xs) / 2) 0; /* Padding menor */
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
  flex-shrink: 0; 
  min-width: 150px; /* Para alinhar os valores */
  text-align: left;
}
.record-value {
  color: var(--color-text-primary);
  text-align: right; 
  word-break: break-word; 
  flex-grow: 1;
}

.transaction-hash-field .hash-value-wrapper {
    display: flex;
    align-items: center;
    justify-content: flex-end; 
    gap: var(--sp-xs);
    flex-grow: 1; 
}
.transaction-hash-text.code-text { 
  font-family: var(--font-monospace);
  background-color: var(--color-bg-muted);
  padding: var(--sp-xxs) var(--sp-xs);
  border-radius: var(--border-radius-sm);
  font-size: 0.85em; 
  word-break: break-all;
  color: var(--color-primary-dark);
  text-align: left; 
}
.button.button-icon { 
    padding: var(--sp-xs); 
    line-height: 1; 
    min-width: auto; 
}
.record-footer {
    margin-top: var(--sp-md);
    text-align: right; 
}


.status-badge {
    font-size: var(--fs-small);
    padding: var(--sp-xxs) var(--sp-sm);
    border-radius: var(--border-radius-pill);
    font-weight: var(--fw-medium);
    color: var(--color-text-inverted);
    text-transform: capitalize; 
    display: inline-block;
}
.status-success { background-color: var(--color-success); }
.status-warning { background-color: var(--color-warning); color: var(--color-text-primary); } 
.status-danger  { background-color: var(--color-danger); }
.status-info    { background-color: var(--color-info); }
.status-default { background-color: var(--color-text-muted); }

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
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap; /* Para quebrar se o valor for muito longo */
}
.details-section p strong {
    color: var(--color-text-primary);
    margin-right: var(--sp-sm);
    flex-shrink: 0;
    text-align: left;
}
.details-section p span:not(strong) { /* O valor */
    text-align: right;
    word-break: break-word;
    flex-grow: 1; /* Para o valor ocupar o espaço restante */
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
    padding: var(--sp-md); 
    border-radius: var(--border-radius); 
    margin-top: var(--sp-sm);
    border: 1px solid var(--color-border-light);
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
.modal-loading p {
    font-size: var(--fs-large);
    color: var(--color-text-muted);
}
.modal-footer-custom { /* Garante que o footer do modal tenha espaçamento e alinhamento */
    padding-top: var(--sp-md);
    margin-top: var(--sp-lg);
    border-top: 1px solid var(--color-border-light);
    display: flex;
    justify-content: flex-end;
}
</style>