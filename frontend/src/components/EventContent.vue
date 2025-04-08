<template>
    <div class="event-content">
      <h2>Registrar Evento</h2>
      <form @submit.prevent="handleSubmit">
        <!-- CAMPOS COMUNS AO EVENTO -->
        <div class="form-group">
          <label for="animal">ID do Animal:</label>
          <input id="animal" v-model.number="form.animal" type="number" required />
        </div>
        <div class="form-group">
          <label for="date">Data:</label>
          <input id="date" v-model="form.date" type="date" required />
        </div>
        <div class="form-group">
          <label for="location">Localização:</label>
          <input id="location" v-model="form.location" type="text" required />
        </div>
        <div class="form-group">
          <label for="observations">Observações:</label>
          <textarea id="observations" v-model="form.observations"></textarea>
        </div>
        <div class="form-group">
          <label for="eventType">Tipo de Evento:</label>
          <select id="eventType" v-model="form.event_type" @change="handleEventTypeChange" required>
            <option disabled value="">Selecione</option>
            <option v-for="option in eventTypes" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>
    
        <!-- CAMPOS DINÂMICOS DE ACORDO COM O TIPO DE EVENTO -->
        <!-- MOVIMENTO -->
        <div v-if="selectedEventType === 'movement'" class="dynamic-form">
          <h3>Detalhes - Movimento</h3>
          <div class="form-group">
            <label for="origin">Propriedade de Origem:</label>
            <input id="origin" v-model.number="movement.origin_property" type="number" required />
          </div>
          <div class="form-group">
            <label for="destination">Propriedade de Destino:</label>
            <input id="destination" v-model.number="movement.destination_property" type="number" required />
          </div>
          <div class="form-group">
            <label for="reason">Razão:</label>
            <input id="reason" v-model="movement.reason" type="text" required />
          </div>
        </div>
    
        <!-- PESAGEM -->
        <div v-else-if="selectedEventType === 'weighing'" class="dynamic-form">
          <h3>Detalhes - Pesagem</h3>
          <div class="form-group">
            <label for="weight">Peso (kg):</label>
            <input id="weight" v-model.number="weighing.weight" type="number" step="0.01" required />
          </div>
        </div>
    
        <!-- VACINA -->
        <div v-else-if="selectedEventType === 'vacine'" class="dynamic-form">
            <h3>Detalhes - Vacina</h3>
            <div class="form-group">
                <label for="name">Nome:</label>
                <input id="name" v-model="vaccine.name" type="text" required />
            </div>
            <div class="form-group">
                <label for="manufacturer">Fabricante:</label>
                <input id="manufacturer" v-model="vaccine.manufacturer" type="text" required />
            </div>
            <div class="form-group">
                <label for="batch">Lote:</label>
                <input id="batch" v-model="vaccine.batch" type="text" required />
            </div>
            <div class="form-group">
                <label for="validity">Validade:</label>
                <input id="validity" v-model="vaccine.validity" type="date" required />
            </div>
            <div class="form-group">
                <label for="dose">Dose:</label>
                <input id="dose" v-model="vaccine.dose" type="text" required />
            </div>
            <div class="form-group">
                <label for="nextDoseDate">Próxima Dose:</label>
                <input id="nextDoseDate" v-model="vaccine.next_dose_date" type="date" />
            </div>
        </div>

        <!-- MEDICAÇÃO -->
        <div v-else-if="selectedEventType === 'medicine'" class="dynamic-form">
            <h3>Detalhes - Medicação</h3>
            <div class="form-group">
                <label for="medicineName">Nome:</label>
                <input id="medicineName" v-model="medicine.name" type="text" required />
            </div>
            <div class="form-group">
                <label for="medicineManufacturer">Fabricante:</label>
                <input id="medicineManufacturer" v-model="medicine.manufacturer" type="text" required />
            </div>
            <div class="form-group">
                <label for="medicineBatch">Lote:</label>
                <input id="medicineBatch" v-model="medicine.batch" type="text" required />
            </div>
            <div class="form-group">
                <label for="medicineValidity">Validade:</label>
                <input id="medicineValidity" v-model="medicine.validity" type="date" required />
            </div>
            <div class="form-group">
                <label for="medicineDose">Dose:</label>
                <input id="medicineDose" v-model="medicine.dose" type="text" required />
            </div>
            <div class="form-group">
                <label for="medicineNextDoseDate">Próxima Dose:</label>
                <input id="medicineNextDoseDate" v-model="medicine.next_dose_date" type="date" />
            </div>
            <div class="form-group">
                <label for="medicineReason">Razão:</label>
                <input id="medicineReason" v-model="medicine.reason" type="text" required />
            </div>
            <div class="form-group">
                <label for="medicineWithdrawal">Tempo de Retirada:</label>
                <input id="medicineWithdrawal" v-model="medicine.withdrawal_time" type="text" />
            </div>
        </div>

        <!-- Reproduction -->
        <div v-else-if="selectedEventType === 'reproduction'" class="dynamic-form">
            <h3>Detalhes - Reprodução</h3>
            <div class="form-group">
                <label for="reproductionType">Tipo de Reprodução:</label>
                <input id="reproductionType" v-model="reproduction.reproduction_type" type="text" required />
            </div>
            <div class="form-group">
                <label for="maleId">ID do Macho:</label>
                <input id="maleId" v-model.number="reproduction.male_id" type="number" required />
            </div>
            <div class="form-group">
                <label for="femaleId">ID da Fêmea:</label>
                <input id="femaleId" v-model.number="reproduction.female_id" type="number" required />
            </div>
            <div class="form-group">
                <label for="reproductionDate">Data:</label>
                <input id="reproductionDate" v-model="reproduction.date" type="date" required />
            </div>
            <div class="form-group">
                <label for="result">Resultado:</label>
                <input id="result" v-model="reproduction.result" type="text" />
            </div>
        </div>
    
        <!-- ABATE -->
        <div v-else-if="selectedEventType === 'slaughter'" class="dynamic-form">
            <h3>Detalhes - Abate</h3>
            <div class="form-group">
            <label for="slaughterDate">Data do Abate:</label>
            <input id="slaughterDate" v-model="slaughter.date" type="date" required />
            </div>
            <div class="form-group">
            <label for="slaughterLocation">Local de Abate:</label>
            <input id="slaughterLocation" v-model="slaughter.location" type="text" required />
            </div>
            <div class="form-group">
            <label for="finalWeight">Peso Final:</label>
            <input id="finalWeight" v-model.number="slaughter.final_weight" type="number" step="0.01" required />
            </div>
            <div class="form-group">
            <label for="inspectionResult">Resultado da Inspeção:</label>
            <input id="inspectionResult" v-model="slaughter.inspection_result" type="text" required />
            </div>
        </div>
    
        <!-- OCORRENCIAS ESPECIAIS -->
        <div v-else-if="selectedEventType === 'occurrence'" class="dynamic-form">
            <h3>Detalhes - Ocorrência Especial</h3>
            <div class="form-group">
                <label for="occurrenceType">Tipo de Ocorrência:</label>
                <input id="occurrenceType" v-model="occurrence.occurrence_type" type="text" required />
            </div>
            <div class="form-group">
                <label for="occurrenceDescription">Descrição:</label>
                <textarea id="occurrenceDescription" v-model="occurrence.description"></textarea>
            </div>
            <div class="form-group">
                <label for="occurrenceDate">Data:</label>
                <input id="occurrenceDate" v-model="occurrence.date" type="date" required />
            </div>
            <div class="form-group">
                <label for="actionsTaken">Ações Tomadas:</label>
                <textarea id="actionsTaken" v-model="occurrence.actions_taken"></textarea>
            </div>
        </div>

        <button type="submit">{{ editing ? "Atualizar Evento" : "Cadastrar Evento" }}</button>
      </form>
    </div>
  </template>
  
  <script>
import { ref, computed, onMounted } from 'vue';
// Importe as funções de serviço para o evento base e para os subeventos
import { registerEvent, updateEvent } from '@/services/eventService';
// Importe os serviços para cada detalhe (ajuste os nomes conforme sua implementação)
import { registerMovement } from '@/services/eventService';
import { registerWeighing } from '@/services/eventService';
import { registerVacine } from '@/services/eventService';
import { registerMedicine } from '@/services/eventService';
import { registerReproduction } from '@/services/eventService';
import { registerSlaughter } from '@/services/eventService';
import { registerSpecialOccurrence } from '@/services/eventService';
import { getEventTypes } from '@/services/lookupService';
  
  export default {
    name: 'EventContent',
    setup() {
      // Dados do registro base do evento
      const form = ref({
        animal: '',
        date: '',
        location: '',
        observations: '',
        event_type: ''
      });
  
      // Indicador para edição (se necessário, neste exemplo apenas cadastro)
      const editing = ref(false);
      const editingId = ref(null);
  
      // Dados para os subformulários para cada tipo
        const movement = ref({
        origin_property: '',
        destination_property: '',
        reason: ''
        });
        const weighing = ref({
        weight: ''
        });
        const vaccine = ref({
        name: '',
        manufacturer: '',
        batch: '',
        validity: '',
        dose: '',
        next_dose_date: ''
        });
        const medicine = ref({
        name: '',
        manufacturer: '',
        batch: '',
        validity: '',
        dose: '',
        next_dose_date: '',
        reason: '',
        withdrawal_time: ''
        });
        const reproduction = ref({
        reproduction_type: '',
        male_id: '',
        female_id: '',
        date: '',
        result: ''
        });
        const slaughter = ref({
        date: '',
        location: '',
        final_weight: '',
        inspection_result: ''
        });
        const occurrence = ref({
        occurrence_type: '',
        description: '',
        date: '',
        actions_taken: ''
        });
  
        // Lista de tipos de evento (obtida do backend)
        const eventTypes = ref([]);
        // Mapeador para converter ID do tipo em uma string identificadora
        const eventTypeMapping = {
        1: 'movement',
        2: 'weighing',
        3: 'vacine',
        4: 'medicine',
        5: 'reproduction',
        1: 'slaughter',
        7: 'occurrence'
        };
  
      // Computed para definir o tipo do subformulário com base na seleção
      const selectedEventType = computed(() => {
        return eventTypeMapping[form.value.event_type] || '';
      });
  
      // Carrega os tipos de evento do backend
      const loadEventTypes = async () => {
        try {
          eventTypes.value = await getEventTypes();
        } catch (error) {
          console.error('Erro ao carregar tipos de evento:', error);
        }
      };
  
        // Lida com a mudança no select do tipo do evento
        const handleEventTypeChange = () => {
        // Reinicializa os subformulários conforme o tipo selecionado
        if (selectedEventType.value === 'movement') {
            movement.value = { origin_property: '', destination_property: '', reason: '' };
        } else if (selectedEventType.value === 'weighing') {
            weighing.value = { weight: '' };
        } else if (selectedEventType.value === 'vacine') {
            vaccine.value = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '' };
        } else if (selectedEventType.value === 'medicine') {
            medicine.value = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: '' };
        } else if (selectedEventType.value === 'reproduction') {
            reproduction.value = { reproduction_type: '', male_id: '', female_id: '', date: '', result: '' };
        } else if (selectedEventType.value === 'slaughter') {
            slaughter.value = { date: '', location: '', final_weight: '', inspection_result: '' };
        } else if (selectedEventType.value === 'occurrence') {
            occurrence.value = { occurrence_type: '', description: '', date: '', actions_taken: '' };
        }
        };
  
      // Função de envio do formulário principal
    const handleSubmit = async () => {
      try {
        // Registra o evento base
        let result;
        if (editing.value) {
          result = await updateEvent(editingId.value, form.value);
          alert('Evento atualizado com sucesso.');
        } else {
          result = await registerEvent(form.value);
          alert('Evento cadastrado com sucesso.');
        }
  
        const eventIdCreated = result.id; // Presume-se que o resultado contenha o ID do evento criado
  
        // Registra os detalhes de acordo com o tipo de evento selecionado
        if (selectedEventType.value === 'movement') {
          const movementPayload = { event: eventIdCreated, ...movement.value };
          console.log('Registrando movimento com payload:', movementPayload);
          await registerMovement(movementPayload);
        } else if (selectedEventType.value === 'weighing') {
          const weighingPayload = { event: eventIdCreated, ...weighing.value };
          console.log('Registrando pesagem com payload:', weighingPayload);
          await registerWeighing(weighingPayload);
        } else if (selectedEventType.value === 'vacine') {
          const vacinePayload = { event: eventIdCreated, ...vaccine.value };
          console.log('Registrando vacina com payload:', vacinePayload);
          await registerVacine(vacinePayload);
        } else if (selectedEventType.value === 'medicine') {
          const medicinePayload = { event: eventIdCreated, ...medicine.value };
          console.log('Registrando medicação com payload:', medicinePayload);
          await registerMedicine(medicinePayload);
        } else if (selectedEventType.value === 'reproduction') {
          const reproductionPayload = { event: eventIdCreated, ...reproduction.value };
          console.log('Registrando reprodução com payload:', reproductionPayload);
          await registerReproduction(reproductionPayload);
        } else if (selectedEventType.value === 'slaughter') {
          const slaughterPayload = { event: eventIdCreated, ...slaughter.value };
          console.log('Registrando abate com payload:', slaughterPayload);
          await registerSlaughter(slaughterPayload);
        } else if (selectedEventType.value === 'occurrence') {
          const occurrencePayload = { event: eventIdCreated, ...occurrence.value };
          console.log('Registrando ocorrência especial com payload:', occurrencePayload);
          await registerSpecialOccurrence(occurrencePayload);
        }
  
          // Após o registro, reinicializa o formulário
          resetForm();
        } catch (error) {
          console.error('Erro ao salvar evento:', error);
          alert('Erro ao salvar evento.');
        }
      };
  
      const resetForm = () => {
      form.value = {
        animal: '',
        date: '',
        location: '',
        observations: '',
        event_type: ''
      };
      editing.value = false;
      editingId.value = null;
      movement.value = { origin_property: '', destination_property: '', reason: '' };
      weighing.value = { weight: '' };
      vaccine.value = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '' };
      medicine.value = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: '' };
      reproduction.value = { reproduction_type: '', male_id: '', female_id: '', date: '', result: '' };
      slaughter.value = { date: '', location: '', final_weight: '', inspection_result: '' };
      occurrence.value = { occurrence_type: '', description: '', date: '', actions_taken: '' };
    };
  
      onMounted(() => {
        loadEventTypes();
      });
  
      return {
      form,
      editing,
      eventTypes,
      selectedEventType,
      movement,
      weighing,
      vaccine,
      medicine,
      reproduction,
      slaughter,
      occurrence,
      handleEventTypeChange,
      handleSubmit,
      resetForm
    };
    }
  };
  </script>
  
  <style scoped>
  .event-content {
    padding: 1rem;
  }
  
  form {
    max-width: 600px;
    margin: auto;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.3rem;
  }
  
  input, select, textarea {
    width: 100%;
    padding: 0.5rem;
    box-sizing: border-box;
  }
  
  button {
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
  
  .dynamic-form {
    margin-top: 1rem;
    padding: 1rem;
    background-color: #f8f8f8;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  </style>
  