<!-- src/components/EventContent.vue -->
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

      <div class="form-actions">
        <button type="submit" class="button button-primary">
          {{ editing ? 'Atualizar Evento' : 'Cadastrar Evento' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { registerEvent, updateEvent } from '@/services/eventService';
import { registerMovement, registerWeighing, registerVacine, registerMedicine, registerReproduction, registerSlaughter, registerSpecialOccurrence } from '@/services/eventService';
import { getEventTypes } from '@/services/lookupService';

export default {
  name: 'EventContent',
  setup() {
    const form = ref({ animal: '', date: '', location: '', observations: '', event_type: '' });
    const editing = ref(false);
    const eventTypes = ref([]);
    const movement = ref({ origin_property: '', destination_property: '', reason: '' });
    const weighing = ref({ weight: '' });
    const vaccine = ref({ name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '' });
    const medicine = ref({ name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: '' });
    const reproduction = ref({ reproduction_type: '', male_id: '', female_id: '', date: '', result: '' });
    const slaughter = ref({ date: '', location: '', final_weight: '', inspection_result: '' });
    const occurrence = ref({ occurrence_type: '', description: '', date: '', actions_taken: '' });

    const mapping = { 1: 'movement', 2: 'weighing', 3: 'vacine', 4: 'medicine', 5: 'reproduction', 6: 'slaughter', 7: 'occurrence' };
    const selectedEventType = computed(() => mapping[form.value.event_type] || '');

    const loadEventTypes = async () => { eventTypes.value = await getEventTypes(); };
    const handleEventTypeChange = () => {};
    const handleSubmit = async () => {
      const result = editing.value
        ? await updateEvent(defaultId => defaultId, form.value)
        : await registerEvent(form.value);
      const id = result.id;
      if (selectedEventType.value === 'movement') await registerMovement({ event: id, ...movement.value });
      else if (selectedEventType.value === 'weighing') await registerWeighing({ event: id, ...weighing.value });
      else if (selectedEventType.value === 'vacine') await registerVacine({ event: id, ...vaccine.value });
      else if (selectedEventType.value === 'medicine') await registerMedicine({ event: id, ...medicine.value });
      else if (selectedEventType.value === 'reproduction') await registerReproduction({ event: id, ...reproduction.value });
      else if (selectedEventType.value === 'slaughter') await registerSlaughter({ event: id, ...slaughter.value });
      else if (selectedEventType.value === 'occurrence') await registerSpecialOccurrence({ event: id, ...occurrence.value });
      alert('Evento salvo com sucesso.');
    };

    onMounted(loadEventTypes);
    return { form, editing, eventTypes, selectedEventType, movement, weighing, vaccine, medicine, reproduction, slaughter, occurrence, handleEventTypeChange, handleSubmit };
  }
};
</script>

<style scoped>
.event-content {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  max-width: 700px;
  margin: var(--sp-xl) auto;
}

.event-content h2 {
  font-family: var(--font-heading);
  color: var(--color-primary);
  font-size: 1.75rem;
  margin-bottom: var(--sp-lg);
  text-align: center;
}

.form-group {
  margin-bottom: var(--sp-md);
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: var(--sp-sm);
  color: var(--color-dark-gray);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-family: var(--font-body);
  font-size: var(--font-size-base);
}

.dynamic-form {
  margin-top: var(--sp-md);
  padding: var(--sp-md);
  background: var(--color-light-gray);
  border-radius: var(--sp-sm);
  border: 1px solid var(--color-border);
}

button[type="submit"] {
  display: block;
  width: 100%;
  padding: var(--sp-md);
  background-color: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: var(--sp-sm);
  font-family: var(--font-body);
  font-size: var(--font-size-large);
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  margin-top: var(--sp-lg);
}

button[type="submit"]:hover,
button[type="submit"]:focus {
  background-color: var(--color-primary-dark);
  transform: scale(1.02);
  outline: none;
}
</style>
