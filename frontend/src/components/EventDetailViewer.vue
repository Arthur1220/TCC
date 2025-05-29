<template>
  <div class="event-detail-viewer card">
    <div class="modal-header">
      <h3 class="modal-title-text">{{ title }}</h3>
      <button v-if="showCloseButtonInHeader" @click="$emit('close')" class="button-close" aria-label="Fechar visualizador">&times;</button>
    </div>

    <div class="modal-body event-details-modal-body">
      <div v-if="contextualAnimalInfoToShow" class="details-section">
        <h4>Animal da Busca (Contexto)</h4>
        <p><strong>Identificação:</strong> <span>{{ contextualAnimalInfoToShow.identification }}</span></p>
        <p v-if="contextualAnimalInfoToShow.id"><strong>ID:</strong> <span>{{ contextualAnimalInfoToShow.id }}</span></p>
        <hr class="my-1">
      </div>

      <div v-if="eventData.dbEventDetails" class="details-section">
        <h4>Dados do Banco de Dados do Evento</h4>
        <p><strong>ID do Evento (BD):</strong> <span>{{ eventData.dbEventDetails.id || 'N/D' }}</span></p>
        <p><strong>Animal (BD):</strong> <span>{{ eventData.dbEventDetails.animal_identification || getAnimalNameById(eventData.dbEventDetails.animal) || `ID ${eventData.dbEventDetails.animal}` }}</span></p>
        <p><strong>Tipo (BD):</strong> <span>{{ eventData.dbEventDetails.event_type_name || getEventTypeNameById(eventData.dbEventDetails.event_type) || `ID ${eventData.dbEventDetails.event_type}` }}</span></p>
        <p><strong>Data (BD):</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.date) }}</span></p>
        <p><strong>Localização (BD):</strong> <span>{{ eventData.dbEventDetails.location || 'N/A' }}</span></p>
        <p><strong>Observações (BD):</strong> <span>{{ eventData.dbEventDetails.observations || 'N/A' }}</span></p>
        <p><strong>Registrado por (BD):</strong> <span>{{ eventData.dbEventDetails.recorded_by_username || 'N/A' }}</span></p>

        <div v-if="eventData.dbEventDetails.details && Object.keys(eventData.dbEventDetails.details).length > 0" class="specific-details mt-1 card">
          <h5 class="details-subtitle">Detalhes Específicos ({{ eventData.dbEventDetails.event_type_name || getEventTypeNameById(eventData.dbEventDetails.event_type) }}):</h5>
          
          <div v-if="isEventType('pesagem') && eventData.dbEventDetails.details.weight !== undefined">
            <p><strong>Peso:</strong> <span>{{ eventData.dbEventDetails.details.weight }} kg</span></p>
            <p v-if="eventData.dbEventDetails.details.date"><strong>Data da Pesagem (Específica):</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.date) }}</span></p>
          </div>
          <div v-else-if="isEventType('movimento')">
            <p><strong>Origem:</strong> <span>{{ getPropertyName(eventData.dbEventDetails.details.origin_property) }}</span></p>
            <p><strong>Destino:</strong> <span>{{ getPropertyName(eventData.dbEventDetails.details.destination_property) }}</span></p>
            <p v-if="eventData.dbEventDetails.details.date"><strong>Data do Movimento (Específica):</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.date) }}</span></p>
            <p><strong>Motivo:</strong> <span>{{ eventData.dbEventDetails.details.reason || 'N/A' }}</span></p>
          </div>
          <div v-else-if="isEventType('vacina')">
            <p><strong>Vacina:</strong> <span>{{ eventData.dbEventDetails.details.name || 'N/D' }}</span></p>
            <p><strong>Dose:</strong> <span>{{ eventData.dbEventDetails.details.dose }} {{ eventData.dbEventDetails.details.dose_unit || '' }}</span></p>
            <p><strong>Fabricante:</strong> <span>{{ eventData.dbEventDetails.details.manufacturer || 'N/A' }}</span></p>
            <p><strong>Lote:</strong> <span>{{ eventData.dbEventDetails.details.batch || 'N/A' }}</span></p>
            <p><strong>Validade da Vacina:</strong> <span>{{ formatDate(eventData.dbEventDetails.details.validity) }}</span></p>
            <p v-if="eventData.dbEventDetails.details.next_dose_date"><strong>Próxima Dose:</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.next_dose_date) }}</span></p>
          </div>
          <div v-else-if="isEventType('medica')">
            <p><strong>Medicamento:</strong> <span>{{ eventData.dbEventDetails.details.name || 'N/D' }}</span></p>
            <p><strong>Dose:</strong> <span>{{ eventData.dbEventDetails.details.dose }} {{ eventData.dbEventDetails.details.dose_unit || '' }}</span></p>
            <p><strong>Fabricante:</strong> <span>{{ eventData.dbEventDetails.details.manufacturer || 'N/A' }}</span></p>
            <p><strong>Lote:</strong> <span>{{ eventData.dbEventDetails.details.batch || 'N/A' }}</span></p>
            <p><strong>Validade do Medicamento:</strong> <span>{{ formatDate(eventData.dbEventDetails.details.validity) }}</span></p>
            <p><strong>Motivo/Indicação:</strong> <span>{{ eventData.dbEventDetails.details.reason || 'N/A' }}</span></p>
            <p v-if="eventData.dbEventDetails.details.next_dose_date"><strong>Próxima Dose:</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.next_dose_date) }}</span></p>
            <p><strong>Período de Carência:</strong> <span>{{ eventData.dbEventDetails.details.withdrawal_time !== null ? `${eventData.dbEventDetails.details.withdrawal_time} dias` : 'N/A' }}</span></p>
          </div>
          <div v-else-if="isEventType('reprodu')">
            <p><strong>Tipo Reprodução:</strong> <span>{{ eventData.dbEventDetails.details.reproduction_type || 'N/D' }}</span></p>
            <p><strong>Macho:</strong> <span>{{ getAnimalNameById(eventData.dbEventDetails.details.male_id) }}</span></p>
            <p><strong>Fêmea:</strong> <span>{{ getAnimalNameById(eventData.dbEventDetails.details.female_id) }}</span></p>
            <p v-if="eventData.dbEventDetails.details.date"><strong>Data da Reprodução (Específica):</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.date) }}</span></p>
            <p><strong>Resultado:</strong> <span>{{ eventData.dbEventDetails.details.result || 'N/A' }}</span></p>
          </div>
          <div v-else-if="isEventType('abate')">
            <p v-if="eventData.dbEventDetails.details.date"><strong>Data do Abate (Específica):</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.date) }}</span></p>
            <p><strong>Local do Abate:</strong> <span>{{ eventData.dbEventDetails.details.location || 'N/D' }}</span></p>
            <p><strong>Peso Final:</strong> <span>{{ eventData.dbEventDetails.details.final_weight }} kg</span></p>
            <p><strong>Resultado da Inspeção:</strong> <span>{{ eventData.dbEventDetails.details.inspection_result || 'N/A' }}</span></p>
          </div>
          <div v-else-if="isEventType('ocorrência especial')">
            <p><strong>Tipo da Ocorrência:</strong> <span>{{ eventData.dbEventDetails.details.occurrence_type || 'N/D' }}</span></p>
            <p v-if="eventData.dbEventDetails.details.date"><strong>Data da Ocorrência (Específica):</strong> <span>{{ formatDbTimestamp(eventData.dbEventDetails.details.date) }}</span></p>
            <p><strong>Descrição:</strong> <span>{{ eventData.dbEventDetails.details.description || 'N/A' }}</span></p>
            <p><strong>Ações Tomadas:</strong> <span>{{ eventData.dbEventDetails.details.actions_taken || 'N/A' }}</span></p>
          </div>
          <div v-else>
            <p v-for="(value, key) in eventData.dbEventDetails.details" :key="key">
              <strong>{{ formatDetailKey(key) }}:</strong> <span>{{ formatDetailValue(key, value, eventData.dbEventDetails.event_type_name) }}</span>
            </p>
          </div>
        </div>
        <p v-else-if="eventData.dbEventDetails.event_type_name && eventData.dbEventDetails.event_type_name.toLowerCase() !== 'geral'" class="mt-1"> 
            Este tipo de evento ('{{ eventData.dbEventDetails.event_type_name }}') não possui detalhes específicos adicionais registrados.
        </p>
      </div>
      <p v-else>Detalhes do evento principal do banco de dados não disponíveis.</p>

      <hr class="my-1">

      <div class="details-section">
        <h4>Dados da Blockchain</h4>
        <div v-if="eventData.blockchainData">
          <p><strong>ID do Evento (BC):</strong> <span>{{ eventData.blockchainData.eventId || 'N/D' }}</span></p>
          <p><strong>ID do Animal (BC):</strong> <span>{{ eventData.blockchainData.animalId || 'N/D' }}</span></p>
          <p><strong>Tipo de Evento ID (BC):</strong> <span>{{ eventData.blockchainData.eventType || 'N/D' }}</span></p>
          <p><strong>Hash dos Dados (BC):</strong> <span class="data-hash">{{ eventData.blockchainData.dataHash || 'N/D' }}</span></p>
          <p><strong>Registrado por (Endereço BC):</strong> <span class="registrant-address">{{ eventData.blockchainData.registrant || 'N/D' }}</span></p>
          <p><strong>Hash do Usuário (BC):</strong> <span class="data-hash">{{ eventData.blockchainData.userHash || 'N/D' }}</span></p>
          <p><strong>Timestamp (BC):</strong> <span>{{ formatBlockchainTimestamp(eventData.blockchainData.timestamp) }}</span></p>
          <p v-if="eventData.blockchainData.transactionHash"><strong>Hash da Transação (BC):</strong> <span class="data-hash">{{ eventData.blockchainData.transactionHash }}</span></p>
        </div>
        <div v-else-if="eventData.dbBlockchainEntry">
          <p><strong>Hash da Transação (BD):</strong> <span class="data-hash">{{ eventData.dbBlockchainEntry.transaction_hash || 'N/D' }}</span></p>
          <p><strong>Data de Registro (BD):</strong> <span>{{ formatDbTimestamp(eventData.dbBlockchainEntry.registration_date) }}</span></p>
          <p><strong>Status (BD):</strong> <span :class="getBlockchainStatusClass(eventData.dbBlockchainEntry.status_details?.name)" class="status-badge">{{ eventData.dbBlockchainEntry.status_details?.name || 'N/D' }}</span></p>
        </div>
        <p v-else>Nenhum dado da blockchain disponível para este registro.</p>
      </div>
    </div>

    <div class="form-actions full-width">
      <button type="button" class="button button-secondary" @click="$emit('close')">Fechar</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventDetailViewer',
  props: {
    eventData: {
      type: Object,
      required: true,
      default: () => ({
        dbEventDetails: null,
        blockchainData: null,
        dbBlockchainEntry: null,
        contextualAnimalInfo: null,
      }),
    },
    title: {
      type: String,
      default: 'Detalhes do Evento',
    },
    showCloseButtonInHeader: {
        type: Boolean,
        default: true
    },
    animalsList: { // Lista completa de animais para lookup de ID -> Nome
        type: Array,
        default: () => []
    },
    propertiesList: { // Lista completa de propriedades para lookup
        type: Array,
        default: () => []
    },
    eventTypesList: { // Lista completa de tipos de evento para lookup
        type: Array,
        default: () => []
    }
  },
  emits: ['close'],
  methods: {
    formatDbTimestamp(dateTimeString) {
      if (!dateTimeString) return 'N/A';
      try {
        const date = new Date(dateTimeString);
        if (isNaN(date.getTime())) return 'Data Inválida';
        return date.toLocaleString('pt-BR', {
          day: '2-digit', month: '2-digit', year: 'numeric',
          hour: '2-digit', minute: '2-digit', second: '2-digit'
        });
      } catch (e) { return "Data Inválida"; }
    },
    formatBlockchainTimestamp(timestamp) {
      if (!timestamp && timestamp !== 0) return 'N/A';
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
    formatDate(dateString, isDateOnly = true) { // Padrão para apenas data
      if (!dateString) return 'N/A';
      try {
        const date = new Date(dateString.length === 10 && dateString.includes('-') ? dateString + 'T00:00:00Z' : dateString);
        if (isNaN(date.getTime())) return 'Data Inválida';
        
        const options = { day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'UTC' };
        if (!isDateOnly) {
            options.hour = '2-digit';
            options.minute = '2-digit';
            return date.toLocaleString('pt-BR', options);
        }
        return date.toLocaleDateString('pt-BR', options);
      } catch (e) { return "Data Inválida"; }
    },
    getEventTypeNameById(eventTypeId) {
      if (!eventTypeId || !this.eventTypesList || this.eventTypesList.length === 0) return `ID ${eventTypeId || 'N/D'}`;
      const type = this.eventTypesList.find(t => t.id === Number(eventTypeId));
      return type ? type.name : `ID ${eventTypeId}`;
    },
    getAnimalNameById(animalId) {
      if (!animalId || !this.animalsList || this.animalsList.length === 0) return `ID ${animalId || 'N/D'}`;
      const animal = this.animalsList.find(a => a.id === Number(animalId));
      return animal ? `${animal.identification} (ID: ${animalId})` : `ID ${animalId}`;
    },
    getPropertyName(propertyId) {
      if (!propertyId || !this.propertiesList || this.propertiesList.length === 0) return `ID ${propertyId || 'N/D'}`;
      const prop = this.propertiesList.find(p => p.id === Number(propertyId));
      return prop ? prop.name : `ID ${propertyId}`;
    },
    isEventType(typePartialName) {
        const eventTypeName = this.eventData.dbEventDetails?.event_type_name || this.getEventTypeNameById(this.eventData.dbEventDetails?.event_type);
        if (!eventTypeName) return false;
        return eventTypeName.toLowerCase().includes(typePartialName.toLowerCase());
    },
    formatDetailKey(key) {
        let formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const translations = {
            'Origin Property': 'Propriedade Origem', 'Destination Property': 'Propriedade Destino',
            'Reason': 'Motivo', 'Weight': 'Peso', 'Name': 'Nome',
            'Manufacturer': 'Fabricante', 'Batch': 'Lote', 'Validity': 'Validade',
            'Dose': 'Dose', 'Dose Unit': 'Unidade da Dose', 'Next Dose Date': 'Próxima Dose',
            'Withdrawal Time': 'Tempo de Carência', 'Reproduction Type': 'Tipo de Reprodução',
            'Male Id': 'ID Macho', 'Female Id': 'ID Fêmea', 'Result': 'Resultado',
            'Location': 'Local', 'Final Weight': 'Peso Final',
            'Inspection Result': 'Resultado da Inspeção', 'Occurrence Type': 'Tipo de Ocorrência',
            'Description': 'Descrição', 'Actions Taken': 'Ações Tomadas',
            'Date': 'Data Específica'
        };
        return translations[formattedKey] || formattedKey;
    },
    formatDetailValue(key, value) { // Removido eventType como parâmetro direto, pode ser acessado via this.eventData
        if (value === null || value === undefined) return 'N/A';
        if (typeof value === 'boolean') return value ? 'Sim' : 'Não';

        const lowerKey = key.toLowerCase();
        const eventTypeForDetails = this.eventData.dbEventDetails?.event_type_name || this.getEventTypeNameById(this.eventData.dbEventDetails?.event_type);


        if (lowerKey.includes('date') || lowerKey.includes('validity') || (eventTypeForDetails?.toLowerCase().includes('reprodu') && lowerKey === 'date')) {
           return this.formatDate(value, lowerKey.includes('validity'));
        }
        if ((lowerKey.includes('property') || lowerKey.endsWith('_property')) && !isNaN(Number(value))) {
            return this.getPropertyName(Number(value));
        }
        if ((lowerKey === 'male_id' || lowerKey === 'female_id') && !isNaN(Number(value))) {
            return this.getAnimalNameById(Number(value));
        }
        if (lowerKey === 'weight' || lowerKey === 'final_weight') return `${value} kg`;
        if (lowerKey === 'withdrawal_time' && value !== null) return `${value} dias`;

        return value;
    },
    getBlockchainStatusClass(statusName) {
        if (!statusName) return 'status-default';
        const statusLower = String(statusName).toLowerCase();
        if (statusLower === 'confirmado') return 'status-badge status-success';
        if (statusLower === 'pendente') return 'status-badge status-warning';
        if (statusLower === 'falhou') return 'status-badge status-danger';
        return 'status-badge status-info';
    }
  },
  computed: {
    contextualAnimalInfoToShow() { // Renomeado para evitar conflito com prop
        return this.eventData.contextualAnimalInfo;
    }
  }
};
</script>

<style scoped>
.event-detail-viewer {
  padding: var(--sp-lg);
  background-color: var(--color-bg-component);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  display: flex; /* Essencial para o layout header/body/footer */
  flex-direction: column;
  max-height: 85vh;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--sp-md);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--sp-lg);
  flex-shrink: 0; /* Impede que o header encolha */
}

.modal-title-text {
  font-family: var(--font-heading);
  font-size: var(--fs-h3);
  color: var(--color-text-primary);
  margin:0; /* Reset de margem para h3 */
}

.button-close {
  background: none;
  border: none;
  font-size: var(--fs-h2); /* Tamanho do 'x' */
  font-weight: var(--fw-light);
  color: var(--color-text-secondary);
  cursor: pointer;
  line-height: 1;
  padding: 0 var(--sp-xs);
}
.button-close:hover {
  color: var(--color-text-primary);
}

.event-details-modal-body {
  /* max-height: 70vh; */ /* Removido para uso como componente, não necessariamente modal */
  overflow-y: auto;
  flex-grow: 1;
  padding-right: var(--sp-sm); /* Para a barra de rolagem não sobrepor o conteúdo */
  text-align: left;
  font-size: var(--fs-base);
}

.details-section {
  margin-bottom: var(--sp-lg); /* Espaço entre as seções principais */
}

.details-section h4 {
  font-size: var(--fs-h5); /* Ajustado para consistência com outros subtítulos */
  color: var(--color-primary);
  margin-top: 0; /* Título da seção não tem margem superior */
  margin-bottom: var(--sp-md);
  padding-bottom: var(--sp-sm);
  border-bottom: 1px solid var(--color-border-light);
}

.details-section p {
  margin-bottom: var(--sp-sm);
  font-size: var(--fs-base);
  line-height: 1.6;
  color: var(--color-text-secondary);
  word-break: break-word;
  display: flex; /* Para alinhar label e valor */
  justify-content: space-between;
  flex-wrap: wrap; /* Permite quebrar se o conteúdo for muito longo */
}
.details-section p strong {
  color: var(--color-text-primary);
  font-weight: var(--fw-semibold); /* Mais destaque para os rótulos */
  min-width: 180px; /* Ajuste para alinhar os ":" */
  margin-right: var(--sp-sm);
  flex-shrink: 0; /* Evita que o label encolha */
  text-align: left;
}
.details-section p span:not(strong) { /* O valor */
    text-align: right;
    word-break: break-word;
    flex-grow: 1; /* Para o valor ocupar o espaço restante */
}

.specific-details {
  background-color: var(--color-bg-body);
  padding: var(--sp-md);
  border-radius: var(--border-radius-md);
  margin-top: var(--sp-sm);
  border: 1px solid var(--color-border-light);
}
.details-subtitle {
  font-size: var(--fs-large);
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
  margin-top: 0;
  margin-bottom: var(--sp-md);
}
.specific-details p {
  font-size: var(--fs-base);
  margin-bottom: var(--sp-xs);
}
.specific-details pre {
    white-space: pre-wrap;
    word-break: break-all;
    background-color: var(--color-bg-muted);
    padding: var(--sp-sm);
    border-radius: var(--border-radius-sm);
    font-family: var(--font-monospace);
    font-size: var(--fs-small);
    color: var(--color-text-secondary);
}

hr.my-1 {
  margin-top: var(--sp-lg);
  margin-bottom: var(--sp-lg);
  border: 0;
  border-top: var(--border-width) solid var(--color-border);
}

.data-hash, .registrant-address {
  font-family: var(--font-monospace);
  font-size: 0.95em;
  color: var(--color-accent);
  word-break: break-all;
  background-color: var(--color-bg-muted);
  padding: var(--sp-xxs) var(--sp-xs);
  border-radius: var(--border-radius-sm);
  display: inline-block;
}

.mt-1 { margin-top: var(--sp-sm); }

.form-actions { /* Para o botão Fechar */
  display: flex;
  justify-content: flex-end;
  padding-top: var(--sp-lg);
  margin-top: var(--sp-lg);
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
}
/* Badge de Status para Blockchain (copiado de UserBlockchainRecords) */
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

/* Estilos para spinner e empty states dentro do modal (se aplicável) */
.modal-loading {
    text-align: center;
    padding: var(--sp-xl);
}
.modal-loading .spinner {
  animation: rotate 2s linear infinite;
  width: 40px; 
  height: 40px;
  margin: 0 auto var(--sp-sm);
}
.modal-loading .spinner .path {
  stroke: var(--color-primary);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}
.modal-loading p {
    font-size: var(--fs-large);
    color: var(--color-text-muted);
}
.small-empty-state {
    font-size: var(--fs-base);
    padding: var(--sp-md);
    text-align: center;
    color: var(--color-text-muted);
}

/* Keyframes (se não estiverem globais) */
@keyframes rotate { 100% { transform: rotate(360deg); } }
@keyframes dash {
  0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
}
</style>