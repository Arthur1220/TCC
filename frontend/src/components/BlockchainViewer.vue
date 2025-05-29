<template>
  <div class="user-blockchain-records-panel content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">{{ title }}</h2>
    </div>

    <div v-if="mode === 'user'">
      <p class="panel-description">
        Aqui você encontra o histórico imutável dos eventos dos seus animais. Cada registro na blockchain garante a máxima transparência e auditabilidade das informações.
      </p>
    </div>
    <div v-else-if="mode === 'admin'">
      <p class="panel-description">
        Visão completa de todos os registros de eventos na blockchain da plataforma. Utilize esta área para auditoria e monitoramento geral das atividades.
      </p>
    </div>

    <div v-if="isLoading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>{{ loadingMessage }}</p>
    </div>

    <div v-else-if="errorLoading" class="empty-state card alert alert-danger">
      <h4 class="alert-heading">Erro ao Carregar Registros</h4>
      <p>{{ errorMessage || 'Não foi possível buscar os registros da blockchain no momento.' }}</p>
      <button @click="fetchRecords" class="button button-primary button-sm">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
        Tentar Novamente
      </button>
    </div>

    <div v-else-if="records.length === 0" class="empty-state card">
      <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" viewBox="0 0 24 24" fill="currentColor" width="64" height="64"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 16H6c-.55 0-1-.45-1-1V6c0-.55.45-1 1-1h12c.55 0 1 .45 1 1v12c0 .55-.45 1-1 1zm-5-3H8v-2h5v2zm3-4H8v-2h8v2zm0-4H8V7h8v2z"/></svg>
      <h4 class="empty-state-title">{{ emptyStateTitle }}</h4>
      
      <div v-if="mode === 'user'">
        <p>Parece que você ainda não tem nenhum evento de animal registrado na blockchain.</p>
        <p class="muted-text">Assim que um evento for criado, ele aparecerá aqui.</p>
      </div>
      <div v-else-if="mode === 'admin'">
        <p>Ainda não existem registros de blockchain na plataforma.</p>
        <p class="muted-text">Todos os eventos criados por qualquer usuário serão listados aqui.</p>
      </div>
    </div>

    <div v-else class="records-list-container">
      <div class="records-summary">
        <p><strong>{{ summaryText }}</strong></p>
      </div>
      <ul class="records-list">
        <li v-for="record in records" :key="record.id || record.transaction_hash" class="record-item card">
          <div class="record-header">
            <h4 class="record-id-title">Registro ID: {{ record.id }}</h4>
            <span class="record-timestamp">{{ formatDate(record.registration_date) }}</span>
          </div>
          <div class="record-body">
            
            <div v-if="mode === 'admin'" class="record-field">
                <span class="record-label">Proprietário:</span>
                <span class="record-value">{{ record.owner_details?.username || `Usuário ID ${record.owner}` }}</span>
            </div>

            <div class="record-field">
              <span class="record-label">Animal:</span>
              <span class="record-value">{{ record.animal_details?.identification || getAnimalIdentificationFromList(record.animal) || `ID ${record.animal}` }}</span>
            </div>
            <div class="record-field">
              <span class="record-label">Tipo de Evento:</span>
              <span class="record-value">{{ getEventTypeName(record.event_details?.event_type) || 'N/D' }}</span>
            </div>
            <div class="record-field">
              <span class="record-label">Status Blockchain:</span>
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
        <div v-if="isLoadingModalDetails" class="modal-content card large-modal loading-state" style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 200px;">
            <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
            <p>Carregando detalhes completos do evento...</p>
        </div>
        
        <EventDetailViewer
            v-else-if="selectedRecordForModal && preparedEventDataForViewer"
            class="modal-content card large-modal"
            :event-data="preparedEventDataForViewer"
            :animals-list="animalsListForLookup"
            :properties-list="properties"
            :event-types-list="eventTypes"
            title="Detalhes Completos do Evento Auditado"
            :show-close-button-in-header="true"
            @close="closeDetailsModal"
        />

        <div v-else-if="selectedRecordForModal && preparedEventDataForViewer && preparedEventDataForViewer.dbEventDetails.error_message" class="modal-content card large-modal">
            <div class="modal-header">
                <h3 class="modal-title-text">Erro ao Carregar Detalhes</h3>
                <button @click="closeDetailsModal" class="button-close" aria-label="Fechar modal">&times;</button>
            </div>
            <div class="modal-body" style="padding: 20px; text-align: center;">
                <p class="text-danger">{{ preparedEventDataForViewer.dbEventDetails.error_message }}</p>
            </div>
            <div class="modal-actions form-actions" style="padding: 1rem; border-top: 1px solid #eee; text-align: right;">
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

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { filterBlockchain } from '@/services/blockchainService';
import { getUserProfile } from '@/services/userService';
import { getEventDetails } from '@/services/eventService';
import { getEventTypes, getProperties } from '@/services/lookupService';
import { getAnimals } from '@/services/animalService';
import NotificationModal from '@/components/NotificationModal.vue';
import EventDetailViewer from '@/components/EventDetailViewer.vue';

// 1. Definição da Prop 'mode'
const props = defineProps({
  mode: {
    type: String,
    required: true,
    default: 'user',
    validator: (value) => ['user', 'admin'].includes(value),
  },
});

const records = ref([]);
const currentUser = ref(null);
const isLoading = ref(true);
const errorLoading = ref(false);
const errorMessage = ref('');
const notification = ref({ show: false, message: '', type: 'success' });

// Estado do Modal
const showDetailsModal = ref(false);
const selectedRecordForModal = ref(null);
const isLoadingModalDetails = ref(false);

// Dados de lookup
const eventTypes = ref([]);
const animalsListForLookup = ref([]);
const properties = ref([]);

// 2. Propriedades Computadas para Textos Dinâmicos
const title = computed(() => {
  return props.mode === 'admin'
    ? 'Auditoria Geral da Blockchain'
    : 'Meus Registros na Blockchain';
});

const description = computed(() => {
  return props.mode === 'admin'
    ? 'Consulte o histórico imutável de todos os eventos registrados na blockchain.'
    : 'Consulte o histórico imutável dos eventos dos seus animais registrados em nossa blockchain, garantindo transparência e auditabilidade.';
});

const loadingMessage = computed(() => {
    return props.mode === 'admin'
        ? 'Carregando todos os registros da plataforma...'
        : 'Carregando seus registros da blockchain...';
});

const emptyStateTitle = computed(() => {
    return props.mode === 'admin'
        ? 'Nenhum Registro na Plataforma'
        : 'Nenhum Registro Encontrado';
});

const summaryText = computed(() => {
    const count = records.value.length;
    if (count === 0) return '';
    
    if (props.mode === 'admin') {
        return `Exibindo ${count} registro${count > 1 ? 's' : ''} total(is) de todos os usuários.`;
    } else {
        return `Você tem ${count} registro${count > 1 ? 's' : ''} na blockchain.`;
    }
});

const preparedEventDataForViewer = computed(() => {
    if (!selectedRecordForModal.value || !selectedRecordForModal.value.dbEventDetails) {
        return null;
    }
    const dbDetails = selectedRecordForModal.value.dbEventDetails;
    return {
        dbEventDetails: { ...dbDetails, },
        dbBlockchainEntry: selectedRecordForModal.value.dbBlockchainEntry,
        contextualAnimalInfo: selectedRecordForModal.value.contextualAnimalInfo || 
                            (dbDetails ? { identification: getAnimalIdentificationFromList(dbDetails.animal), id: dbDetails.animal } : null)
    };
});

// Funções de notificação e utilitárias (sem alteração)
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
  if (currentUser.value) return;
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
    if (eventTypes.value.length > 0 && animalsListForLookup.value.length > 0) return;
    try {
        const [fetchedEventTypes, fetchedAnimals, fetchedProperties] = await Promise.all([
            getEventTypes(),
            getAnimals(),
            getProperties()
        ]);
        eventTypes.value = fetchedEventTypes;
        animalsListForLookup.value = fetchedAnimals;
        properties.value = fetchedProperties;
    } catch (error) {
        console.error("Erro ao carregar dados de lookup (UserBlockchainRecords):", error);
        showAppNotification("Erro ao carregar dados de referência.", "warning");
    }
};

// 3. Lógica de Busca Condicional (sem alteração)
const fetchRecords = async () => {
  isLoading.value = true;
  errorLoading.value = false;
  errorMessage.value = '';
  records.value = [];

  let params = {};

  try {
    if (props.mode === 'user') {
      await fetchCurrentUser();
      if (!currentUser.value?.id) {
        isLoading.value = false;
        return;
      }
      params.owner = currentUser.value.id;
    }

    const result = await filterBlockchain(params);
    records.value = result.sort((a, b) =>
      new Date(b.registration_date || 0) - new Date(a.registration_date || 0)
    );

  } catch (error) {
    console.error(`Erro ao carregar registros de blockchain no modo '${props.mode}':`, error.response?.data || error);
    errorLoading.value = true;
    errorMessage.value = `Falha ao buscar registros no modo '${props.mode}'. Verifique sua conexão ou tente mais tarde.`;
    showAppNotification(errorMessage.value, 'error');
  } finally {
    isLoading.value = false;
  }
};

// 4. Ciclo de Vida e Watcher (sem alteração)
onMounted(async () => {
  await loadLookupData();
  await fetchRecords();
});

watch(() => props.mode, (newMode, oldMode) => {
    if (newMode !== oldMode) {
        fetchRecords();
    }
});

// Funções utilitárias (sem alteração)
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

const formatEventDate = (dateInput) => formatDate(dateInput, false);

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

// Funções do Modal (sem alteração na lógica)
const openDetailsModal = async (recordFromList) => {
    isLoadingModalDetails.value = true;
    selectedRecordForModal.value = {
        dbBlockchainEntry: recordFromList,
        dbEventDetails: null,
        blockchainData: null,
        contextualAnimalInfo: recordFromList.animal_details 
            ? { identification: recordFromList.animal_details.identification, id: recordFromList.animal }
            : { identification: getAnimalIdentificationFromList(recordFromList.animal), id: recordFromList.animal }
    };
    showDetailsModal.value = true;

    const eventIdInDb = recordFromList.event_details?.id || recordFromList.event;
    const eventTypeIdInDb = recordFromList.event_details?.event_type;

    if (eventIdInDb && eventTypeIdInDb !== undefined && eventTypeIdInDb !== null) {
        try {
            const fullDetails = await getEventDetails(eventIdInDb, eventTypeIdInDb);
            selectedRecordForModal.value.dbEventDetails = {
                ...fullDetails,
                animal_identification: getAnimalIdentificationFromList(fullDetails.animal),
                event_type_name: getEventTypeName(fullDetails.event_type),
                recorded_by_username: fullDetails.recorded_by_username || (fullDetails.recorded_by ? `Usuário ID ${fullDetails.recorded_by}` : 'N/D'),
                details: fullDetails.details || {}
            };
        } catch (error) {
            console.error("Erro ao buscar detalhes completos do evento para o modal:", error);
            showAppNotification("Falha ao carregar detalhes completos do evento.", "error");
            selectedRecordForModal.value.dbEventDetails = { error_message: "Não foi possível carregar os detalhes do evento do banco de dados." };
        }
    } else {
        console.warn("UserBlockchainRecords: Informações do evento DB ausentes no registro da blockchain.", recordFromList);
        selectedRecordForModal.value.dbEventDetails = { error_message: "Informações do evento original não encontradas no registro da blockchain." };
    }
    isLoadingModalDetails.value = false;
};

const closeDetailsModal = () => {
    showDetailsModal.value = false;
    selectedRecordForModal.value = null;
    isLoadingModalDetails.value = false;
};
</script>

<style scoped>
/* Seu CSS Scoped Existente ... (não precisa mudar nada aqui) */
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

/* Estilos do Modal (copiados do código antigo para consistência) */
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