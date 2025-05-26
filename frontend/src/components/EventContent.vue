<template>
  <section class="content-panel">
    <h3 class="panel-title">Gerenciar Eventos</h3>
    <p class="panel-description">
      Nesta tela você pode registrar novos eventos para seus animais, editar registros existentes ou registrar um evento para múltiplos animais de uma vez.
    </p>

    <div class="header-actions">
      <button class="button button-primary" @click="openModal">
        + Registrar Evento Individual
      </button>
      <button class="button button-accent" @click="openBatchEventRegistrationModal">
        + Registrar Evento em Lote
      </button>
    </div>

    <div class="table-container">
        <div v-if="events.length">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Animal</th>
                        <th>Tipo de Evento</th>
                        <th>Data</th>
                        <th>Localização</th>
                        <th>Observações</th>
                        <th class="text-right">Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="eventItem in events" :key="eventItem.id">
                        <td>{{ getAnimalIdentification(eventItem.animal) }}</td>
                        <td>{{ getEventTypeName(eventItem.event_type) }}</td>
                        <td>{{ formatDateTime(eventItem.date) }}</td>
                        <td>{{ eventItem.location || 'N/A' }}</td>
                        <td class="truncate">{{ eventItem.observations || 'N/A' }}</td>
                        <td class="actions-cell">
                            <button class="button-action button-edit" @click="editEvent(eventItem)">Editar</button>
                            <button class="button-action button-delete" @click="confirmDelete(eventItem.id)">Deletar</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else class="empty-state">
            <p>Nenhum evento registrado para seus animais.</p>
        </div>
    </div>


    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content large-modal">
        <h3 class="modal-title">{{ editing ? 'Editar Evento Individual' : 'Registrar Evento Individual' }}</h3>
        <form @submit.prevent="handleSubmit" class="form-grid">
          
          <div class="form-group">
            <label for="animal">Animal:</label>
            <select id="animal" v-model.number="form.animal" class="select" required>
              <option disabled :value="null">Selecione um animal</option>
              <option
                v-for="a in animals"
                :key="a.id"
                :value="a.id"
              >
                {{ a.identification }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="event-type">Tipo de Evento:</label>
            <select id="event-type" v-model.number="form.event_type" @change="handleEventTypeChange" class="select" required>
              <option disabled :value="null">Selecione um tipo de evento</option>
              <option
                v-for="o in eventTypes"
                :key="o.id"
                :value="o.id"
              >
                {{ o.name }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="date">Data e Hora:</label>
            <input id="date" v-model="form.date" type="datetime-local" class="input" required />
          </div>

          <div class="form-group">
            <label for="location">Localização:</label>
            <input id="location" v-model="form.location" type="text" class="input" />
          </div>

          <div class="form-group full-width">
            <label for="observations">Observações:</label>
            <textarea id="observations" v-model="form.observations" class="textarea"></textarea>
          </div>

          <div v-if="selectedEventTypeName === 'movimento'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes do Movimento</h4>
            <div class="form-group">
              <label for="origin-property">Propriedade Origem:</label>
              <select id="origin-property" v-model.number="movement.origin_property" class="select" required>
                <option disabled :value="null">Selecione a propriedade de origem</option>
                <option v-for="prop in properties" :key="prop.id" :value="prop.id">{{ prop.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="destination-property">Propriedade Destino:</label>
              <select id="destination-property" v-model.number="movement.destination_property" class="select" required>
                <option disabled :value="null">Selecione a propriedade de destino</option>
                <option v-for="prop in properties" :key="prop.id" :value="prop.id">{{ prop.name }}</option>
              </select>
            </div>
            <div class="form-group full-width">
              <label for="movement-reason">Razão:</label>
              <textarea id="movement-reason" v-model="movement.reason" class="textarea"></textarea>
            </div>
          </div>

          <div v-else-if="selectedEventTypeName === 'pesagem'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Pesagem</h4>
            <div class="form-group">
              <label for="weight">Peso (kg):</label>
              <input id="weight" v-model.number="weighing.weight" type="number" step="0.01" class="input" required />
            </div>
          </div>

          <div v-else-if="selectedEventTypeName === 'vacinação'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Vacina</h4>
            <div class="form-group">
              <label for="vacine-name">Nome:</label>
              <input id="vacine-name" v-model="vaccine.name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="vacine-manufacturer">Fabricante:</label>
              <input id="vacine-manufacturer" v-model="vaccine.manufacturer" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="vacine-batch">Lote:</label>
              <input id="vacine-batch" v-model="vaccine.batch" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="vacine-validity">Validade:</label>
              <input id="vacine-validity" v-model="vaccine.validity" type="date" class="input" required />
            </div>
            <div class="form-group">
              <label for="vacine-dose">Dose:</label>
              <input id="vacine-dose" v-model.number="vaccine.dose" type="number" step="0.01" class="input" required />
            </div>
            <div class="form-group">
              <label for="vacine-next">Próxima Dose:</label>
              <input id="vacine-next" v-model="vaccine.next_dose_date" type="datetime-local" class="input" />
            </div>
          </div>

          <div v-else-if="selectedEventTypeName === 'medicação'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Medicação</h4>
            <div class="form-group">
              <label for="med-name">Nome:</label>
              <input id="med-name" v-model="medicine.name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="med-manufacturer">Fabricante:</label>
              <input id="med-manufacturer" v-model="medicine.manufacturer" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="med-batch">Lote:</label>
              <input id="med-batch" v-model="medicine.batch" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="med-validity">Validade:</label>
              <input id="med-validity" v-model="medicine.validity" type="date" class="input" required />
            </div>
            <div class="form-group">
              <label for="med-dose">Dose:</label>
              <input id="med-dose" v-model.number="medicine.dose" type="number" step="0.01" class="input" required />
            </div>
            <div class="form-group">
              <label for="med-next">Próxima Dose:</label>
              <input id="med-next" v-model="medicine.next_dose_date" type="datetime-local" class="input" />
            </div>
            <div class="form-group">
              <label for="med-reason">Razão:</label>
              <textarea id="med-reason" v-model="medicine.reason" class="textarea"></textarea>
            </div>
            <div class="form-group">
              <label for="med-withdrawal">Tempo de Retirada (dias):</label>
              <input id="med-withdrawal" v-model.number="medicine.withdrawal_time" type="number" class="input" />
            </div>
          </div>

          <div v-else-if="selectedEventTypeName === 'reprodução'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Reprodução</h4>
            <div class="form-group">
              <label for="rep-type">Tipo:</label>
              <select id="rep-type" v-model="reproduction.reproduction_type" class="select" required>
                <option disabled value="">Selecione o tipo</option>
                <option value="natural">Natural</option>
                <option value="artificial">Artificial</option>
              </select>
            </div>
            <div class="form-group">
              <label for="rep-male">Macho (ID):</label>
              <input id="rep-male" v-model.number="reproduction.male_id" type="number" class="input" required />
            </div>
            <div class="form-group">
              <label for="rep-female">Fêmea (ID):</label>
              <input id="rep-female" v-model.number="reproduction.female_id" type="number" class="input" required />
            </div>
            <div class="form-group">
              <label for="rep-result">Resultado:</label>
              <select id="rep-result" v-model="reproduction.result" class="select">
                <option :value="null">(Opcional)</option>
                <option value="positive">Positivo</option>
                <option value="negative">Negativo</option>
              </select>
            </div>
          </div>

          <div v-else-if="selectedEventTypeName === 'abate'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes do Abate</h4>
            <div class="form-group">
              <label for="sl-location">Local:</label>
              <input id="sl-location" v-model="slaughter.location" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="sl-weight">Peso Final (kg):</label>
              <input id="sl-weight" v-model.number="slaughter.final_weight" type="number" step="0.01" class="input" required />
            </div>
            <div class="form-group">
              <label for="sl-inspection">Resultado da Inspeção:</label>
              <select id="sl-inspection" v-model="slaughter.inspection_result" class="select">
                <option :value="null">(Opcional)</option>
                <option value="passed">Aprovado</option>
                <option value="failed">Reprovado</option>
              </select>
            </div>
          </div>

          <div v-else-if="selectedEventTypeName === 'ocorrência especial'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Ocorrência Especial</h4>
            <div class="form-group">
              <label for="occ-type">Tipo:</label>
              <input id="occ-type" v-model="occurrence.occurrence_type" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="occ-desc">Descrição:</label>
              <textarea id="occ-desc" v-model="occurrence.description" class="textarea"></textarea>
            </div>
            <div class="form-group">
              <label for="occ-actions">Ações Tomadas:</label>
              <textarea id="occ-actions" v-model="occurrence.actions_taken" class="textarea"></textarea>
            </div>
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="button button-primary">
              {{ editing ? 'Atualizar Evento' : 'Registrar Evento' }}
            </button>
            <button type="button" class="button button-secondary" @click="closeModal">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showBatchEventModal" class="modal-overlay" @click.self="closeBatchEventRegistrationModal">
      <div class="modal-content large-modal">
        <h3 class="modal-title">Registrar Evento em Lote</h3>
        <p class="modal-description">Selecione os animais e o tipo de evento para aplicar a todo o lote.</p>

        <form @submit.prevent="handleBatchEventSubmit" class="form-grid">
          <div class="form-group full-width">
            <label>Animais do Lote:</label>
            <div class="animal-checkbox-list">
              <div v-for="animal in animals" :key="animal.id" class="animal-checkbox-item">
                <input type="checkbox" :value="animal.id" v-model="batchEventForm.animal_ids" :id="`batch-animal-${animal.id}`" />
                <label :for="`batch-animal-${animal.id}`">{{ animal.identification }}</label>
              </div>
            </div>
            <p v-if="batchEventForm.animal_ids.length > 0" class="selected-count">
              {{ batchEventForm.animal_ids.length }} animal(is) selecionado(s).
            </p>
            <p v-else class="empty-selection">Nenhum animal selecionado.</p>
          </div>

          <div class="form-group">
            <label for="batch-event-type">Tipo de Evento:</label>
            <select id="batch-event-type" v-model.number="batchEventForm.event_type" @change="handleBatchEventTypeChange" class="select" required>
              <option disabled :value="null">Selecione um tipo de evento</option>
              <option v-for="type in eventTypes" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="batch-event-date">Data e Hora:</label>
            <input type="datetime-local" id="batch-event-date" v-model="batchEventForm.date" class="input" required />
          </div>

          <div class="form-group">
            <label for="batch-event-location">Localização:</label>
            <input type="text" id="batch-event-location" v-model="batchEventForm.location" class="input" />
          </div>

          <div class="form-group full-width">
            <label for="batch-event-observations">Observações:</label>
            <textarea id="batch-event-observations" v-model="batchEventForm.observations" class="textarea"></textarea>
          </div>

          <div v-if="batchEventForm.event_type_name === 'movimento'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes do Movimento</h4>
            <div class="form-group">
              <label for="batch-origin-property">Propriedade Origem:</label>
              <select id="batch-origin-property" v-model.number="batchEventForm.movement_details.origin_property" class="select" required>
                <option disabled :value="null">Selecione a propriedade de origem</option>
                <option v-for="prop in properties" :key="prop.id" :value="prop.id">{{ prop.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="batch-destination-property">Propriedade Destino:</label>
              <select id="batch-destination-property" v-model.number="batchEventForm.movement_details.destination_property" class="select" required>
                <option disabled :value="null">Selecione a propriedade de destino</option>
                <option v-for="prop in properties" :key="prop.id" :value="prop.id">{{ prop.name }}</option>
              </select>
            </div>
            <div class="form-group full-width">
              <label for="batch-movement-reason">Razão:</label>
              <textarea id="batch-movement-reason" v-model="batchEventForm.movement_details.reason" class="textarea"></textarea>
            </div>
          </div>

          <div v-else-if="batchEventForm.event_type_name === 'pesagem'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Pesagem</h4>
            <div class="form-group">
              <label for="batch-weight">Peso (kg):</label>
              <input id="batch-weight" v-model.number="batchEventForm.weighing_details.weight" type="number" step="0.01" class="input" required />
            </div>
          </div>

          <div v-else-if="batchEventForm.event_type_name === 'vacinação'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Vacina</h4>
            <div class="form-group">
              <label for="batch-vacine-name">Nome:</label>
              <input id="batch-vacine-name" v-model="batchEventForm.vacine_details.name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-vacine-manufacturer">Fabricante:</label>
              <input id="batch-vacine-manufacturer" v-model="batchEventForm.vacine_details.manufacturer" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="batch-vacine-batch">Lote:</label>
              <input id="batch-vacine-batch" v-model="batchEventForm.vacine_details.batch" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="batch-vacine-validity">Validade:</label>
              <input id="batch-vacine-validity" v-model="batchEventForm.vacine_details.validity" type="date" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-vacine-dose">Dose:</label>
              <input id="batch-vacine-dose" v-model.number="batchEventForm.vacine_details.dose" type="number" step="0.01" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-vacine-next">Próxima Dose:</label>
              <input id="batch-vacine-next" v-model="batchEventForm.vacine_details.next_dose_date" type="datetime-local" class="input" />
            </div>
          </div>

          <div v-else-if="batchEventForm.event_type_name === 'medicação'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Medicação</h4>
            <div class="form-group">
              <label for="batch-med-name">Nome:</label>
              <input id="batch-med-name" v-model="batchEventForm.medicine_details.name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-med-manufacturer">Fabricante:</label>
              <input id="batch-med-manufacturer" v-model="batchEventForm.medicine_details.manufacturer" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="batch-med-batch">Lote:</label>
              <input id="batch-med-batch" v-model="batchEventForm.medicine_details.batch" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="batch-med-validity">Validade:</label>
              <input id="batch-med-validity" v-model="batchEventForm.medicine_details.validity" type="date" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-med-dose">Dose:</label>
              <input id="batch-med-dose" v-model.number="batchEventForm.medicine_details.dose" type="number" step="0.01" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-med-next">Próxima Dose:</label>
              <input id="batch-med-next" v-model="batchEventForm.medicine_details.next_dose_date" type="datetime-local" class="input" />
            </div>
            <div class="form-group">
              <label for="batch-med-reason">Razão:</label>
              <textarea id="batch-med-reason" v-model="batchEventForm.medicine_details.reason" class="textarea"></textarea>
            </div>
            <div class="form-group">
              <label for="batch-med-withdrawal">Tempo de Retirada (dias):</label>
              <input id="batch-med-withdrawal" v-model.number="batchEventForm.medicine_details.withdrawal_time" type="number" class="input" />
            </div>
          </div>

          <div v-else-if="batchEventForm.event_type_name === 'reprodução'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Reprodução</h4>
            <div class="form-group">
              <label for="batch-rep-type">Tipo:</label>
              <select id="batch-rep-type" v-model="batchEventForm.reproduction_details.reproduction_type" class="select" required>
                <option disabled value="">Selecione o tipo</option>
                <option value="natural">Natural</option>
                <option value="artificial">Artificial</option>
              </select>
            </div>
            <div class="form-group">
              <label for="batch-rep-male">Macho (ID):</label>
              <input id="batch-rep-male" v-model.number="batchEventForm.reproduction_details.male_id" type="number" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-rep-female">Fêmea (ID):</label>
              <input id="batch-rep-female" v-model.number="batchEventForm.reproduction_details.female_id" type="number" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-rep-result">Resultado:</label>
              <select id="batch-rep-result" v-model="batchEventForm.reproduction_details.result" class="select">
                <option :value="null">(Opcional)</option>
                <option value="positive">Positivo</option>
                <option value="negative">Negativo</option>
              </select>
            </div>
          </div>

          <div v-else-if="batchEventForm.event_type_name === 'abate'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes do Abate</h4>
            <div class="form-group">
              <label for="batch-sl-location">Local:</label>
              <input id="batch-sl-location" v-model="batchEventForm.slaughter_details.location" type="text" class="input" />
            </div>
            <div class="form-group">
              <label for="batch-sl-weight">Peso Final (kg):</label>
              <input id="batch-sl-weight" v-model.number="batchEventForm.slaughter_details.final_weight" type="number" step="0.01" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-sl-inspection">Resultado da Inspeção:</label>
              <select id="batch-sl-inspection" v-model="batchEventForm.slaughter_details.inspection_result" class="select">
                <option :value="null">(Opcional)</option>
                <option value="passed">Aprovado</option>
                <option value="failed">Reprovado</option>
              </select>
            </div>
          </div>

          <div v-else-if="batchEventForm.event_type_name === 'ocorrencia especial'" class="dynamic-form full-width">
            <h4 class="sub-title">Detalhes da Ocorrência Especial</h4>
            <div class="form-group">
              <label for="batch-occ-type">Tipo:</label>
              <input id="batch-occ-type" v-model="batchEventForm.special_occurrences_details.occurrence_type" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="batch-occ-desc">Descrição:</label>
              <textarea id="batch-occ-desc" v-model="batchEventForm.special_occurrences_details.description" class="textarea"></textarea>
            </div>
            <div class="form-group">
              <label for="batch-occ-actions">Ações Tomadas:</label>
              <textarea id="batch-occ-actions" v-model="batchEventForm.special_occurrences_details.actions_taken" class="textarea"></textarea>
            </div>
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="button button-primary" :disabled="batchEventForm.animal_ids.length === 0">
              Registrar Eventos
            </button>
            <button type="button" class="button button-secondary" @click="closeBatchEventRegistrationModal">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <NotificationModal
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
      @close="notification.show = false"
    />
  </section>
</template>

<script>
import {
  registerEvent,
  updateEvent,
  getEvents,
  deleteEvent,
  getEventDetails,
  registerMovement,
  registerWeighing,
  registerVacine,
  registerMedicine,
  registerReproduction,
  registerSlaughter,
  registerSpecialOccurrence,
  getMovements,
  getWeighings,
  getVacines,
  getMedicines,
  getReproductions,
  getSlaughters,
  getSpecialOccurrences,
  registerBatchEvent // Importa a função de registro em lote
} from '@/services/eventService';
import { getEventTypes, getProperties } from '@/services/lookupService';
import { getUserProfile } from '@/services/userService';
import { getAnimals } from '@/services/animalService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'EventContent',
  components: {
    NotificationModal
  },
  data() {
    return {
      showModal: false, // Modal para registro/edição individual
      showBatchEventModal: false, // NOVO: Modal para registro em lote
      editing: false,
      editingId: null,
      user: null,
      animals: [],
      properties: [], // Propriedades para eventos de Movimentação
      events: [], // Lista de eventos para a tabela

      // Formulário para registro/edição INDIVIDUAL
      form: {
        animal: null,
        date: '',
        location: '',
        observations: '',
        event_type: null // ID do tipo de evento
      },
      // Detalhes específicos dos eventos INDIVIDUAIS
      movement: { event: null, origin_property: null, destination_property: null, reason: '' },
      weighing: { event: null, weight: null },
      vaccine: { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '' },
      medicine: { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null },
      reproduction: { event: null, reproduction_type: '', male_id: null, female_id: null, result: null },
      slaughter: { event: null, location: '', final_weight: null, inspection_result: null },
      occurrence: { event: null, occurrence_type: '', description: '', actions_taken: '' },
      
      eventTypes: [], // Lista de tipos de evento

      // NOVO: Formulário para registro em LOTE
      batchEventForm: {
        animal_ids: [], // IDs dos animais selecionados
        event_type: null,
        event_type_name: '', // Nome do tipo para controle condicional
        date: '',
        location: '',
        observations: '',
        // Detalhes específicos para cada tipo de evento (lote)
        movement_details: { origin_property: null, destination_property: null, reason: '' },
        weighing_details: { weight: null },
        vacine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '' },
        medicine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null },
        reproduction_details: { reproduction_type: '', male_id: null, female_id: null, result: null },
        slaughter_details: { location: '', final_weight: null, inspection_result: null },
        special_occurrences_details: { occurrence_type: '', description: '', actions_taken: '' },
      },

      // Para o modal de notificação
      notification: {
        show: false,
        message: '',
        type: 'success'
      }
    };
  },
  computed: {
    selectedEventTypeName() {
      // Retorna o nome do tipo de evento selecionado no formulário INDIVIDUAL
      const selectedType = this.eventTypes.find(type => type.id === this.form.event_type);
      return selectedType ? selectedType.name.toLowerCase() : '';
    },
    // Mapeia IDs de animais para suas identificações para exibição na tabela
    animalIdToIdentificationMap() {
        return this.animals.reduce((acc, animal) => {
            acc[animal.id] = animal.identification;
            return acc;
        }, {});
    }
  },
  watch: {
    // Monitora a mudança do tipo de evento no formulário de LOTE para atualizar o nome
    'batchEventForm.event_type'(newVal) {
      if (newVal) {
        const selectedType = this.eventTypes.find(type => type.id === newVal);
        this.batchEventForm.event_type_name = selectedType ? selectedType.name.toLowerCase() : '';
      } else {
        this.batchEventForm.event_type_name = '';
      }
      this.resetBatchEventSpecificDetails(); // Limpa detalhes específicos ao mudar o tipo
    }
  },
  methods: {
    // Exibe a notificação
    showNotification(message, type) {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      setTimeout(() => {
        this.notification.show = false;
      }, 3000);
    },
    async loadUserAndAnimals() {
      try {
        this.user = await getUserProfile();
        // Carrega animais do usuário com status "ativo" (ID 1)
        const list = await getAnimals({ owner: this.user.id, status: 1 });
        this.animals = list;
      } catch (e) {
        console.error('Erro ao carregar usuário ou animais:', e);
        this.showNotification('Erro ao carregar dados iniciais (usuário/animais).', 'error');
      }
    },
    async loadEventData() {
        try {
            // Carrega todos os eventos para o usuário logado
            if (this.user && this.user.id) {
                // Assume que getEvents() já filtra por usuário logado ou que o backend fará isso.
                // Se precisar filtrar explicitamente: await filterEvents({ recorded_by: this.user.id });
                this.events = await getEvents();
            }
        } catch (e) {
            console.error('Erro ao carregar eventos:', e);
            this.showNotification('Erro ao carregar a lista de eventos.', 'error');
        }
    },
    async loadEventTypesAndProperties() {
      try {
        this.eventTypes = await getEventTypes();
        this.properties = await getProperties(); // Carrega as propriedades
      } catch (e) {
        console.error('Erro ao carregar tipos de evento ou propriedades:', e);
        this.showNotification('Erro ao carregar tipos de evento ou propriedades.', 'error');
      }
    },

    // Métodos para Modal de Registro/Edição Individual
    openModal() {
      this.resetIndividualForm();
      this.editing = false;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.resetIndividualForm(); // Garante que o form individual está limpo
    },
    async editEvent(eventItem) {
        this.resetIndividualForm(); // Limpa o formulário e detalhes antes de preencher
        this.editing = true;
        this.editingId = eventItem.id;

        try {
            // Primeiro preenche os dados gerais do evento
            this.form.animal = eventItem.animal;
            this.form.date = eventItem.date ? new Date(eventItem.date).toISOString().slice(0, 16) : ''; // Formato datetime-local
            this.form.location = eventItem.location;
            this.form.observations = eventItem.observations;
            this.form.event_type = eventItem.event_type; // Este é o ID do event_type

            // Agora busca os detalhes específicos
            // A função getEventDetails já lida com qual service chamar
            const fullEventDetails = await getEventDetails(eventItem.id, eventItem.event_type);
            const details = fullEventDetails.details; // Os detalhes específicos estarão aqui

            if (details) {
                const eventTypeName = this.selectedEventTypeName; // Usa o computed para obter o nome em minúsculas
                
                // Preenche os objetos de detalhes específicos
                if (eventTypeName === 'movimento') {
                    this.movement = { ...details };
                } else if (eventTypeName === 'pesagem') {
                    this.weighing = { ...details };
                } else if (eventTypeName === 'vacinação') {
                    this.vaccine = { 
                        ...details,
                        validity: details.validity ? new Date(details.validity).toISOString().slice(0, 10) : '',
                        next_dose_date: details.next_dose_date ? new Date(details.next_dose_date).toISOString().slice(0, 16) : '',
                    };
                } else if (eventTypeName === 'medicação') {
                    this.medicine = { 
                        ...details,
                        validity: details.validity ? new Date(details.validity).toISOString().slice(0, 10) : '',
                        next_dose_date: details.next_dose_date ? new Date(details.next_dose_date).toISOString().slice(0, 16) : '',
                    };
                } else if (eventTypeName === 'reprodução') {
                    this.reproduction = {
                        ...details,
                        date: details.date ? new Date(details.date).toISOString().slice(0, 10) : '', // Data da reprodução, não do evento principal
                    };
                } else if (eventTypeName === 'abate') {
                    this.slaughter = { 
                        ...details,
                        date: details.date ? new Date(details.date).toISOString().slice(0, 10) : '', // Data do abate, não do evento principal
                    };
                } else if (eventTypeName === 'ocorrência especial') {
                    this.occurrence = { 
                        ...details,
                        date: details.date ? new Date(details.date).toISOString().slice(0, 10) : '', // Data da ocorrência, não do evento principal
                    };
                }
            }
            this.showModal = true;
        } catch (e) {
            console.error('Erro ao carregar evento para edição:', e);
            this.showNotification('Erro ao carregar evento para edição.', 'error');
        }
    },
    handleEventTypeChange() {
      // Reseta os detalhes específicos do formulário individual
      this.resetIndividualSpecificDetails();
    },
    async handleSubmit() {
      // Validação básica
      if (this.form.animal === null || !this.form.date || this.form.event_type === null) {
        this.showNotification('Por favor, preencha todos os campos obrigatórios do evento principal.', 'error');
        return;
      }

      let eventData = { ...this.form };
      
      const eventTypeId = this.form.event_type;
      const eventTypeName = this.eventTypes.find(type => type.id === eventTypeId)?.name.toLowerCase();

      let specificEventPayload = null;

      // Constrói o payload para o evento específico com base no tipo
      if (eventTypeName === 'movimento') {
        if (this.movement.origin_property === null || this.movement.destination_property === null) {
          this.showNotification('Preencha as propriedades de origem e destino para o movimento.', 'error');
          return;
        }
        specificEventPayload = { ...this.movement, date: this.form.date }; // Associa data do evento principal
      } else if (eventTypeName === 'pesagem') {
        if (this.weighing.weight === null) {
          this.showNotification('Preencha o peso para a pesagem.', 'error');
          return;
        }
        specificEventPayload = { ...this.weighing, date: this.form.date };
      } else if (eventTypeName === 'vacinação') {
        if (!this.vaccine.name || !this.vaccine.validity || this.vaccine.dose === null) {
          this.showNotification('Preencha nome, validade e dose da vacina.', 'error');
          return;
        }
        specificEventPayload = { ...this.vaccine, date: this.form.date };
      } else if (eventTypeName === 'medicação') {
        if (!this.medicine.name || !this.medicine.validity || this.medicine.dose === null) {
          this.showNotification('Preencha nome, validade e dose do medicamento.', 'error');
          return;
        }
        specificEventPayload = { ...this.medicine, date: this.form.date };
      } else if (eventTypeName === 'reprodução') {
        if (!this.reproduction.reproduction_type || this.reproduction.male_id === null || this.reproduction.female_id === null) {
          this.showNotification('Preencha tipo, ID do macho e ID da fêmea para reprodução.', 'error');
          return;
        }
        specificEventPayload = { ...this.reproduction, date: this.form.date }; // Reprodução usa a data do evento principal
      } else if (eventTypeName === 'abate') {
        if (this.slaughter.final_weight === null) {
          this.showNotification('Preencha o peso final do abate.', 'error');
          return;
        }
        specificEventPayload = { ...this.slaughter, date: this.form.date }; // Abate usa a data do evento principal
      } else if (eventTypeName === 'ocorrência especial') {
        if (!this.occurrence.occurrence_type) {
          this.showNotification('Preencha o tipo de ocorrência especial.', 'error');
          return;
        }
        specificEventPayload = { ...this.occurrence, date: this.form.date }; // Ocorrência usa a data do evento principal
      }

      try {
        let resEvent;
        if (this.editing) {
          resEvent = await updateEvent(this.editingId, eventData);
          if (specificEventPayload) {
            specificEventPayload.event = resEvent.id;
            const existingDetails = await getEventDetails(resEvent.id, resEvent.event_type);
            const detailId = existingDetails.details ? existingDetails.details.id : null;
            
            if (detailId) {
                // Atualiza o detalhe existente
                if (eventTypeName === 'movimento') await updateMovement(detailId, specificEventPayload);
                else if (eventTypeName === 'pesagem') await updateWeighing(detailId, specificEventPayload);
                else if (eventTypeName === 'vacinação') await updateVacine(detailId, specificEventPayload);
                else if (eventTypeName === 'medicação') await updateMedicine(detailId, specificEventPayload);
                else if (eventTypeName === 'reprodução') await updateReproduction(detailId, specificEventPayload);
                else if (eventTypeName === 'abate') await updateSlaughter(detailId, specificEventPayload);
                else if (eventTypeName === 'ocorrência especial') await updateSpecialOccurrence(detailId, specificEventPayload);
            } else {
                // Caso não exista um detalhe (improvável na edição, mas para robustez)
                if (eventTypeName === 'movimento') await registerMovement(specificEventPayload);
                else if (eventTypeName === 'pesagem') await registerWeighing(specificEventPayload);
                else if (eventTypeName === 'vacinação') await registerVacine(specificEventPayload);
                else if (eventTypeName === 'medicação') await registerMedicine(specificEventPayload);
                else if (eventTypeName === 'reprodução') await registerReproduction(specificEventPayload);
                else if (eventTypeName === 'abate') await registerSlaughter(specificEventPayload);
                else if (eventTypeName === 'ocorrência especial') await registerSpecialOccurrence(specificEventPayload);
            }
          }
          this.showNotification('Evento atualizado com sucesso!', 'success');
        } else {
          resEvent = await registerEvent(eventData);
          if (specificEventPayload) {
            specificEventPayload.event = resEvent.id; // Vincula ao evento principal
            if (eventTypeName === 'movimento') await registerMovement(specificEventPayload);
            else if (eventTypeName === 'pesagem') await registerWeighing(specificEventPayload);
            else if (eventTypeName === 'vacinação') await registerVacine(specificEventPayload);
            else if (eventTypeName === 'medicação') await registerMedicine(specificEventPayload);
            else if (eventTypeName === 'reprodução') await registerReproduction(specificEventPayload);
            else if (eventTypeName === 'abate') await registerSlaughter(specificEventPayload);
            else if (eventTypeName === 'ocorrência especial') await registerSpecialOccurrence(specificEventPayload);
          }
          this.showNotification('Evento registrado com sucesso!', 'success');
        }
        
        this.closeModal();
        await this.loadEventData(); // Recarrega a tabela de eventos
      } catch (e) {
        console.error('Erro ao salvar evento:', e);
        let errorMessage = 'Erro ao salvar evento.';
        if (e.response && e.response.data) {
            errorMessage += ' Detalhes: ' + Object.values(e.response.data).map(err => (Array.isArray(err) ? err.join(', ') : err)).join('; ');
        }
        this.showNotification(errorMessage, 'error');
      }
    },
    async confirmDelete(id) {
        if (confirm('Tem certeza que deseja deletar este evento?')) {
            try {
                await deleteEvent(id);
                this.showNotification('Evento deletado com sucesso!', 'success');
                await this.loadEventData(); // Recarrega a lista
            } catch (e) {
                console.error('Erro ao deletar evento:', e);
                this.showNotification('Erro ao deletar evento.', 'error');
            }
        }
    },

    // NOVO: Métodos para o Modal de Registro de Evento em Lote
    openBatchEventRegistrationModal() {
        this.resetBatchForm(); // Limpa o formulário de lote
        this.showBatchEventModal = true;
    },
    closeBatchEventRegistrationModal() {
        this.showBatchEventModal = false;
        this.resetBatchForm();
    },
    handleBatchEventTypeChange() {
        // Redefine os detalhes específicos do formulário de lote quando o tipo muda
        this.resetBatchEventSpecificDetails();
    },
    async handleBatchEventSubmit() {
        if (this.batchEventForm.animal_ids.length === 0) {
            this.showNotification('Por favor, selecione pelo menos um animal para registrar o evento.', 'error');
            return;
        }
        if (this.batchEventForm.event_type === null || !this.batchEventForm.date) {
            this.showNotification('Por favor, preencha o tipo de evento e a data.', 'error');
            return;
        }

        const payload = {
            animal_ids: this.batchEventForm.animal_ids,
            event_type: this.batchEventForm.event_type,
            date: this.batchEventForm.date,
            location: this.batchEventForm.location || null,
            observations: this.batchEventForm.observations || null,
        };

        const eventTypeName = this.eventTypes.find(type => type.id === this.batchEventForm.event_type)?.name.toLowerCase();

        // Adiciona detalhes específicos do evento ao payload de lote
        if (eventTypeName === 'movimento') {
            if (this.batchEventForm.movement_details.origin_property === null || this.batchEventForm.movement_details.destination_property === null) {
                this.showNotification('Preencha as propriedades de origem e destino para o movimento.', 'error');
                return;
            }
            payload.movement_details = {
                origin_property: this.batchEventForm.movement_details.origin_property,
                destination_property: this.batchEventForm.movement_details.destination_property,
                reason: this.batchEventForm.movement_details.reason || null,
                date: this.batchEventForm.date, // Data do evento principal
            };
        } else if (eventTypeName === 'pesagem') {
            if (this.batchEventForm.weighing_details.weight === null) {
                this.showNotification('Preencha o peso para a pesagem.', 'error');
                return;
            }
            payload.weighing_details = {
                weight: this.batchEventForm.weighing_details.weight,
                date: this.batchEventForm.date,
            };
        } else if (eventTypeName === 'vacinação') {
            if (!this.batchEventForm.vacine_details.name || !this.batchEventForm.vacine_details.validity || this.batchEventForm.vacine_details.dose === null) {
                this.showNotification('Preencha nome, validade e dose da vacina.', 'error');
                return;
            }
            payload.vacine_details = {
                name: this.batchEventForm.vacine_details.name,
                manufacturer: this.batchEventForm.vacine_details.manufacturer || null,
                batch: this.batchEventForm.vacine_details.batch || null,
                validity: this.batchEventForm.vacine_details.validity,
                dose: this.batchEventForm.vacine_details.dose,
                next_dose_date: this.batchEventForm.vacine_details.next_dose_date || null,
                date: this.batchEventForm.date,
            };
        } else if (eventTypeName === 'medicação') {
            if (!this.batchEventForm.medicine_details.name || !this.batchEventForm.medicine_details.validity || this.batchEventForm.medicine_details.dose === null) {
                this.showNotification('Preencha nome, validade e dose do medicamento.', 'error');
                return;
            }
            payload.medicine_details = {
                name: this.batchEventForm.medicine_details.name,
                manufacturer: this.batchEventForm.medicine_details.manufacturer || null,
                batch: this.batchEventForm.medicine_details.batch || null,
                validity: this.batchEventForm.medicine_details.validity,
                dose: this.batchEventForm.medicine_details.dose,
                next_dose_date: this.batchEventForm.medicine_details.next_dose_date || null,
                reason: this.batchEventForm.medicine_details.reason || null,
                withdrawal_time: this.batchEventForm.medicine_details.withdrawal_time || null,
                date: this.batchEventForm.date,
            };
        } else if (eventTypeName === 'reprodução') {
            if (!this.batchEventForm.reproduction_details.reproduction_type || this.batchEventForm.reproduction_details.male_id === null || this.batchEventForm.reproduction_details.female_id === null) {
                this.showNotification('Preencha tipo, ID do macho e ID da fêmea para reprodução.', 'error');
                return;
            }
            payload.reproduction_details = {
                reproduction_type: this.batchEventForm.reproduction_details.reproduction_type,
                male_id: this.batchEventForm.reproduction_details.male_id,
                female_id: this.batchEventForm.reproduction_details.female_id,
                result: this.batchEventForm.reproduction_details.result || null,
                date: this.batchEventForm.date,
            };
        } else if (eventTypeName === 'abate') {
            if (this.batchEventForm.slaughter_details.final_weight === null) {
                this.showNotification('Preencha o peso final do abate.', 'error');
                return;
            }
            payload.slaughter_details = {
                location: this.batchEventForm.slaughter_details.location || null,
                final_weight: this.batchEventForm.slaughter_details.final_weight,
                inspection_result: this.batchEventForm.slaughter_details.inspection_result || null,
                date: this.batchEventForm.date,
            };
        } else if (eventTypeName === 'ocorrência especial') {
            if (!this.batchEventForm.special_occurrences_details.occurrence_type) {
                this.showNotification('Preencha o tipo de ocorrência especial.', 'error');
                return;
            }
            payload.special_occurrences_details = {
                occurrence_type: this.batchEventForm.special_occurrences_details.occurrence_type,
                description: this.batchEventForm.special_occurrences_details.description || null,
                actions_taken: this.batchEventForm.special_occurrences_details.actions_taken || null,
                date: this.batchEventForm.date,
            };
        }

        try {
            const response = await registerBatchEvent(payload);
            this.showNotification(response.message, 'success');
            this.closeBatchEventRegistrationModal();
            await this.loadEventData(); // Recarrega a tabela de eventos
        } catch (error) {
            console.error('Erro ao registrar evento em lote:', error);
            let errorMessage = 'Erro ao registrar evento em lote.';
            if (error.response && error.response.data) {
                if (error.response.data.error) {
                    errorMessage += ` ${error.response.data.error}`;
                } else {
                    errorMessage += ' Detalhes: ' + Object.values(error.response.data).map(e => (Array.isArray(e) ? e.join(', ') : e)).join('; ');
                }
            }
            this.showNotification(errorMessage, 'error');
        }
    },

    // Funções de reset
    resetIndividualForm() {
      this.form = { animal: null, date: '', location: '', observations: '', event_type: null };
      this.resetIndividualSpecificDetails();
    },
    resetIndividualSpecificDetails() {
        this.movement = { event: null, origin_property: null, destination_property: null, reason: '' };
        this.weighing = { event: null, weight: null };
        this.vaccine = { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '' };
        this.medicine = { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null };
        this.reproduction = { event: null, reproduction_type: '', male_id: null, female_id: null, result: null };
        this.slaughter = { event: null, location: '', final_weight: null, inspection_result: null };
        this.occurrence = { event: null, occurrence_type: '', description: '', actions_taken: '' };
    },
    resetBatchForm() {
        this.batchEventForm = {
            animal_ids: [],
            event_type: null,
            event_type_name: '',
            date: '',
            location: '',
            observations: '',
            movement_details: { origin_property: null, destination_property: null, reason: '' },
            weighing_details: { weight: null },
            vacine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '' },
            medicine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null },
            reproduction_details: { reproduction_type: '', male_id: null, female_id: null, result: null },
            slaughter_details: { location: '', final_weight: null, inspection_result: null },
            special_occurrences_details: { occurrence_type: '', description: '', actions_taken: '' },
        };
    },
    resetBatchEventSpecificDetails() {
        this.batchEventForm.movement_details = { origin_property: null, destination_property: null, reason: '' };
        this.batchEventForm.weighing_details = { weight: null };
        this.batchEventForm.vacine_details = { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '' };
        this.batchEventForm.medicine_details = { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '' };
        this.batchEventForm.reproduction_details = { reproduction_type: '', male_id: null, female_id: null, result: null };
        this.batchEventForm.slaughter_details = { location: '', final_weight: null, inspection_result: null };
        this.batchEventForm.special_occurrences_details = { occurrence_type: '', description: '', actions_taken: '' };
    },

    // Funções auxiliares para exibição
    getAnimalIdentification(animalId) {
        return this.animalIdToIdentificationMap[animalId] || 'Desconhecido';
    },
    getEventTypeName(eventTypeId) {
        const type = this.eventTypes.find(t => t.id === eventTypeId);
        return type ? type.name : 'Desconhecido';
    },
    formatDateTime(dateTimeString) {
        if (!dateTimeString) return 'N/A';
        const date = new Date(dateTimeString);
        // Formata para 'dd/mm/yyyy hh:mm'
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }
  },
  async mounted() {
    await this.loadUserAndAnimals();
    await this.loadEventTypesAndProperties();
    await this.loadEventData(); // Carrega os eventos ao montar o componente
  }
};
</script>

<style scoped>
/* ============================
    Estilos Específicos para EventContent
    (Baseados no style.css global para consistência)
   ============================ */

/* Importa as variáveis e estilos base do seu arquivo global */
/* Para garantir que as variáveis CSS sejam carregadas, você pode precisar importá-las
   no seu arquivo main.js ou App.vue, ou certificar-se de que elas são acessíveis globalmente.
   Assumindo que :root {...} do style.css já está no escopo global. */

.content-panel {
  background-color: var(--color-bg);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); /* Sombra mais suave */
  margin-bottom: var(--sp-xl);
}

.panel-title {
  text-align: center;
  color: var(--color-text); /* Cor de texto padrão para títulos */
  margin-bottom: var(--sp-sm); /* Espaçamento menor para o título */

}

.panel-description {
  text-align: center;
  color: var(--color-text);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.header-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-md);
  margin-bottom: var(--sp-lg);
  padding-bottom: var(--sp-md);
  border-bottom: 1px solid var(--color-border);
}

.button {
  /* Já definido no style.css, mas podemos adicionar variações */
  font-size: var(--fs-base); /* Tamanho de fonte padrão para botões */
  padding: var(--sp-sm) var(--sp-md);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.button-primary {
  background-color: var(--color-accent);
  color: var(--color-bg);
  border: 2px solid var(--color-accent);
}
.button-primary:hover, .button-primary:focus {
  background-color: transparent;
  color: var(--color-accent);
}

.button-accent { /* Novo estilo para o botão de lote */
  background-color: var(--color-muted);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
}
.button-accent:hover, .button-accent:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
}

/* Tabela de Dados */
.table-container {
    overflow-x: auto;
    margin-top: var(--sp-md);
    border: 1px solid var(--color-border);
    border-radius: var(--sp-sm);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 800px; /* Garante que a tabela não fique muito estreita */
}

.data-table th,
.data-table td {
    text-align: left;
    padding: var(--sp-sm) var(--sp-md);
    border-bottom: 1px solid var(--color-border);
    font-size: var(--fs-base);
}

.data-table th {
    background-color: var(--color-muted);
    color: var(--color-text);
    font-weight: 600;
    text-transform: uppercase;
    font-size: var(--fs-small);
}

.data-table tbody tr:last-child td {
    border-bottom: none;
}

.data-table tbody tr:hover {
    background-color: var(--color-muted);
}

.data-table .text-right {
    text-align: right;
}

.data-table .truncate {
    max-width: 250px; /* Limita a largura para observações */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.actions-cell {
    white-space: nowrap; /* Evita quebra de linha nos botões de ação */
    text-align: right;
}

.button-action {
    font-size: var(--fs-small);
    padding: 0.3rem 0.6rem;
    border-radius: var(--sp-xs);
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    margin-left: var(--sp-xs);
    border: 1px solid; /* Adiciona borda para consistência */
}

.button-edit {
    background-color: var(--color-accent); /* Azul */
    color: var(--color-bg);
    border-color: var(--color-accent);
}
.button-edit:hover {
    background-color: #145CBF; /* Tom mais escuro */
    box-shadow: 0 2px 5px rgba(26, 115, 232, 0.2);
}

.button-delete {
    background-color: #E74C3C; /* Vermelho */
    color: var(--color-bg);
    border-color: #E74C3C;
}
.button-delete:hover {
    background-color: #C0392B; /* Tom mais escuro */
    box-shadow: 0 2px 5px rgba(231, 76, 60, 0.2);
}

.empty-state {
    text-align: center;
    color: var(--color-text);
    padding: var(--sp-lg);
    font-size: var(--fs-base);
}

/* Modal - Reutilizado do style.css global e aprimorado */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); /* Fundo mais escuro para modals */
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}
.modal-content {
  background-color: var(--color-bg);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%; max-width: 600px; /* Ajuste para o tamanho do modal */
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  text-align: center;
  position: relative;
  animation: fadeInScale 0.3s ease-out;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--color-border); /* Adiciona borda para consistência visual */
}
.large-modal {
    max-width: 800px; /* Permite mais espaço para formulários maiores */
}
.modal-title {
  font-family: var(--font-heading);
  color: var(--color-text);
  margin-bottom: var(--sp-md);
  font-size: var(--fs-large);
  font-weight: 700;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--sp-sm);
}
.modal-description {
    font-size: var(--fs-base);
    color: var(--color-text);
    margin-bottom: var(--sp-lg);
}

/* Formulários dentro dos Modais */
.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Duas colunas por padrão */
    gap: var(--sp-md);
    text-align: left;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: var(--sp-sm); /* Espaçamento menor entre label e input */
}

.form-group.full-width {
    grid-column: 1 / -1; /* Ocupa todas as colunas */
}

.form-group label {
    font-weight: 600;
    color: var(--color-text);
    font-size: var(--fs-base);
}

.input, .select, .textarea { /* Usa as classes globais */
    padding: var(--sp-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--sp-sm);
    width: 100%;
    font-size: var(--fs-base);
    background-color: var(--color-bg);
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
    box-sizing: border-box;
}

.select {
  appearance: none;
  background-image: url('data:image/svg+xml;utf8,<svg fill="%23000000" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'); /* Seta preta */
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 20px;
}
.input:focus, .textarea:focus, .select:focus {
  border-color: var(--color-accent);
  outline: none;
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2); /* Sombra azul */
}

.dynamic-form {
  grid-column: 1 / -1;
  margin-top: var(--sp-md);
  padding: var(--sp-md);
  background: var(--color-muted); /* Fundo "muted" para seções dinâmicas */
  border-radius: var(--sp-sm);
  border: 1px solid var(--color-border);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-md);
}

.dynamic-form h4.sub-title {
  grid-column: 1 / -1;
  margin-top: 0;
  margin-bottom: var(--sp-md);
  font-family: var(--font-heading);
  color: var(--color-text);
  font-size: 1.2rem;
  font-weight: 600;
  border-bottom: 1px dashed var(--color-border);
  padding-bottom: var(--sp-sm);
}

.form-actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-md);
  margin-top: var(--sp-lg);
  padding-top: var(--sp-md);
  border-top: 1px solid var(--color-border);
}

/* Lista de Checkboxes de Animais (para lote) */
.animal-checkbox-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* Auto-ajusta colunas */
    gap: var(--sp-sm);
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--sp-sm);
    padding: var(--sp-sm);
    background-color: var(--color-muted);
}

.animal-checkbox-item {
    display: flex;
    align-items: center;
    gap: var(--sp-xs);
    font-size: var(--fs-base);
    color: var(--color-text);
}

.animal-checkbox-item input[type="checkbox"] {
    transform: scale(1.1);
    cursor: pointer;
}

.selected-count, .empty-selection {
    font-size: var(--fs-small);
    color: var(--color-text);
    margin-top: var(--sp-sm);
    text-align: left;
}

/* Animações */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Responsividade */
@media (max-width: 768px) {
    .form-grid, .dynamic-form {
        grid-template-columns: 1fr; /* Uma coluna em telas menores */
    }
    .data-table {
        min-width: 500px; /* Reduz o min-width para telas menores */
    }
    .header-actions {
        flex-direction: column; /* Botões um abaixo do outro */
        align-items: stretch;
    }
    .button {
        width: 100%; /* Botões ocupam largura total */
    }
}
</style>