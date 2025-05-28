<template>
  <section class="content-panel event-content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Gerenciar Eventos dos Animais</h2>
      <div class="panel-actions header-actions-event">
        <button class="button button-primary" @click="openModal">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
          Registrar Evento Individual
        </button>
        <button class="button button-secondary" @click="openBatchEventRegistrationModal">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9h-4v4h-2v-4H9V9h4V5h2v4h4v2z"/></svg>
          Registrar Evento em Lote
        </button>
      </div>
    </div>
    <p class="panel-description">
      Nesta tela você pode registrar novos eventos para seus animais, editar registros existentes ou registrar um evento para um lote/grupo de animais de uma vez, garantindo a rastreabilidade completa.
    </p>

    <div v-if="isLoadingEvents" class="loading-state">
        <p>Carregando eventos...</p>
    </div>
    <div v-else-if="events.length" class="table-responsive-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Animal</th>
            <th>Tipo de Evento</th>
            <th>Data</th>
            <th>Localização</th>
            <th class="th-observations">Observações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="eventItem in sortedEvents" :key="eventItem.id" class="table-row-hover">
            <td data-label="Animal">{{ getAnimalIdentification(eventItem.animal) }}</td>
            <td data-label="Tipo de Evento">{{ getEventTypeName(eventItem.event_type) }}</td>
            <td data-label="Data">{{ formatDateTime(eventItem.date) }}</td>
            <td data-label="Localização">{{ eventItem.location || 'N/A' }}</td>
            <td data-label="Observações" class="truncate-text" :title="eventItem.observations || ''">{{ eventItem.observations || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="empty-state card">
      <p>Nenhum evento registrado para seus animais ainda.</p>
      <button class="button button-primary" @click="openModal">Registrar Primeiro Evento</button>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content card large-modal">
        <div class="modal-header">
            <h3 class="modal-title-text">{{ editing ? 'Editar Evento Individual' : 'Registrar Novo Evento Individual' }}</h3>
            <button @click="closeModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <form @submit.prevent="handleSubmit" class="modal-form form-grid">
          <div class="form-group">
            <label for="event-animal" class="form-label">Animal*</label>
            <select id="event-animal" v-model.number="form.animal" class="select" required>
              <option disabled :value="nullPlaceholder.animal">Selecione um animal</option>
              <option v-for="a in animals" :key="a.id" :value="a.id">{{ a.identification }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="event-type" class="form-label">Tipo de Evento*</label>
            <select id="event-type" v-model.number="form.event_type" @change="handleEventTypeChange" class="select" required>
              <option disabled :value="nullPlaceholder.event_type">Selecione um tipo</option>
              <option v-for="o in eventTypes" :key="o.id" :value="o.id">{{ o.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="event-date" class="form-label">Data e Hora*</label>
            <input id="event-date" v-model="form.date" type="datetime-local" class="input" required />
          </div>
          <div class="form-group">
            <label for="event-location" class="form-label">Localização</label>
            <input id="event-location" v-model="form.location" type="text" class="input" placeholder="Ex: Pasto A, Curral 2"/>
          </div>
          <div class="form-group full-width">
            <label for="event-observations" class="form-label">Observações</label>
            <textarea id="event-observations" v-model="form.observations" class="textarea" rows="3"></textarea>
          </div>

          <div v-if="selectedEventTypeName === 'movimentação' || selectedEventTypeName === 'movimento'" class="dynamic-form-section card full-width">
            <h4 class="dynamic-form-title">Detalhes do Movimento</h4>
            <div class="form-grid nested-grid">
                <div class="form-group">
                    <label for="origin-property" class="form-label">Propriedade Origem*</label>
                    <select id="origin-property" v-model.number="movement.origin_property" class="select" required>
                        <option disabled :value="nullPlaceholder.property">Selecione a origem</option>
                        <option v-for="prop in properties" :key="`orig-${prop.id}`" :value="prop.id">{{ prop.name }}</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="destination-property" class="form-label">Propriedade Destino*</label>
                    <select id="destination-property" v-model.number="movement.destination_property" class="select" required>
                        <option disabled :value="nullPlaceholder.property">Selecione o destino</option>
                        <option v-for="prop in properties" :key="`dest-${prop.id}`" :value="prop.id">{{ prop.name }}</option>
                    </select>
                </div>
                <div class="form-group full-width">
                    <label for="movement-reason" class="form-label">Razão/Motivo</label>
                    <textarea id="movement-reason" v-model="movement.reason" class="textarea" rows="2"></textarea>
                </div>
            </div>
          </div>
          <div v-else-if="selectedEventTypeName === 'pesagem'" class="dynamic-form-section card full-width">
            <h4 class="dynamic-form-title">Detalhes da Pesagem</h4>
            <div class="form-group">
                <label for="weight" class="form-label">Peso (kg)*</label>
                <input id="weight" v-model.number="weighing.weight" type="number" step="0.01" class="input" required />
            </div>
          </div>
          <div v-else-if="selectedEventTypeName === 'vacinação'" class="dynamic-form-section card full-width">
              <h4 class="dynamic-form-title">Detalhes da Vacinação</h4>
              <div class="form-grid nested-grid">
                  <div class="form-group"><label for="vacine-name" class="form-label">Nome da Vacina*</label><input id="vacine-name" v-model="vaccine.name" type="text" class="input" required /></div>
                  
                  <div class="form-group">
                      <label for="vacine-dose" class="form-label">Dose (Valor Numérico)*</label>
                      <input id="vacine-dose" v-model.number="vaccine.dose" type="number" step="any" class="input" placeholder="Ex: 0.5" required />
                      </div>

                  <div class="form-group"><label for="vacine-manufacturer" class="form-label">Fabricante</label><input id="vacine-manufacturer" v-model="vaccine.manufacturer" type="text" class="input" /></div>
                  <div class="form-group"><label for="vacine-batch" class="form-label">Lote</label><input id="vacine-batch" v-model="vaccine.batch" type="text" class="input" /></div>
                  <div class="form-group"><label for="vacine-validity" class="form-label">Validade da Vacina*</label><input id="vacine-validity" v-model="vaccine.validity" type="date" class="input" required /></div>
                  <div class="form-group"><label for="vacine-next" class="form-label">Próxima Dose</label><input id="vacine-next" v-model="vaccine.next_dose_date" type="datetime-local" class="input" /></div>
              </div>
          </div>
            <div v-else-if="selectedEventTypeName === 'medicação'" class="dynamic-form-section card full-width">
                <h4 class="dynamic-form-title">Detalhes da Medicação</h4>
                <div class="form-grid nested-grid">
                    <div class="form-group"><label for="med-name" class="form-label">Nome do Medicamento*</label><input id="med-name" v-model="medicine.name" type="text" class="input" required /></div>
                    
                    <div class="form-group">
                        <label for="med-dose" class="form-label">Dose Administrada (Valor Numérico)*</label>
                        <input id="med-dose" v-model.number="medicine.dose" type="number" step="any" class="input" required placeholder="Ex: 10"/>
                        </div>

                    <div class="form-group"><label for="med-manufacturer" class="form-label">Fabricante</label><input id="med-manufacturer" v-model="medicine.manufacturer" type="text" class="input" /></div>
                    <div class="form-group"><label for="med-batch" class="form-label">Lote</label><input id="med-batch" v-model="medicine.batch" type="text" class="input" /></div>
                    <div class="form-group"><label for="med-validity" class="form-label">Validade do Medicamento*</label><input id="med-validity" v-model="medicine.validity" type="date" class="input" required /></div>
                    <div class="form-group"><label for="med-next" class="form-label">Próxima Dose</label><input id="med-next" v-model="medicine.next_dose_date" type="datetime-local" class="input" /></div>
                    <div class="form-group full-width"><label for="med-reason" class="form-label">Motivo/Indicação</label><textarea id="med-reason" v-model="medicine.reason" class="textarea" rows="2"></textarea></div>
                    <div class="form-group"><label for="med-withdrawal" class="form-label">Período de Carência (dias)</label><input id="med-withdrawal" v-model.number="medicine.withdrawal_time" type="number" class="input" min="0" /></div>
                </div>
            </div>
            <div v-else-if="selectedEventTypeName === 'reprodução'" class="dynamic-form-section card full-width">
                <h4 class="dynamic-form-title">Detalhes da Reprodução</h4>
                <div class="form-grid nested-grid">
                    <div class="form-group">
                        <label for="reproduction-type" class="form-label">Tipo de Reprodução*</label>
                        <input id="reproduction-type" v-model="reproduction.reproduction_type" type="text" class="input" placeholder="Ex: Inseminação Artificial, Monta Natural" required />
                    </div>
                    <div class="form-group">
                        <label for="reproduction-male" class="form-label">Macho (Reprodutor)*</label>
                        <select id="reproduction-male" v-model.number="reproduction.male_id" class="select" required>
                            <option disabled :value="nullPlaceholder.animal">Selecione o macho</option>
                            <option v-for="a in animals" :key="`male-${a.id}`" :value="a.id">{{ a.identification }}</option>
                        </select>
                    </div>
                     <div class="form-group">
                        <label for="reproduction-female" class="form-label">Fêmea (Matriz)*</label>
                        <select id="reproduction-female" v-model.number="reproduction.female_id" class="select" required :disabled="form.animal === nullPlaceholder.animal">
                            <option disabled :value="nullPlaceholder.animal">Selecione a fêmea</option>
                            <option v-if="form.animal !== nullPlaceholder.animal" :value="form.animal">{{ getAnimalIdentification(form.animal) }} (Animal do Evento)</option>
                            <option v-for="a in animals.filter(an => an.id !== form.animal)" :key="`female-${a.id}`" :value="a.id">{{ a.identification }}</option>
                        </select>
                        <p class="form-text" v-if="form.animal !== nullPlaceholder.animal">A fêmea é o animal principal do evento.</p>
                    </div>
                    <div class="form-group">
                        <label for="reproduction-result" class="form-label">Resultado</label>
                        <input id="reproduction-result" v-model="reproduction.result" type="text" class="input" placeholder="Ex: Positivo, Negativo, Nascimento de X"/>
                    </div>
                    <div class="form-group">
                        <label for="reproduction-specific-date" class="form-label">Data da Reprodução/Diagnóstico</label>
                        <input id="reproduction-specific-date" v-model="reproduction.date" type="datetime-local" class="input"/>
                         <p class="form-text">Se diferente da data geral do evento.</p>
                    </div>
                </div>
            </div>
            <div v-else-if="selectedEventTypeName === 'abate'" class="dynamic-form-section card full-width">
                <h4 class="dynamic-form-title">Detalhes do Abate</h4>
                <div class="form-grid nested-grid">
                    <div class="form-group">
                        <label for="slaughter-location" class="form-label">Local do Abate*</label>
                        <input id="slaughter-location" v-model="slaughter.location" type="text" class="input" placeholder="Ex: Frigorífico X" required />
                    </div>
                    <div class="form-group">
                        <label for="slaughter-weight" class="form-label">Peso Final (kg)*</label>
                        <input id="slaughter-weight" v-model.number="slaughter.final_weight" type="number" step="0.01" class="input" required />
                    </div>
                    <div class="form-group">
                        <label for="slaughter-inspection" class="form-label">Resultado da Inspeção</label>
                        <input id="slaughter-inspection" v-model="slaughter.inspection_result" type="text" class="input" placeholder="Ex: Aprovado, Condenado"/>
                    </div>
                </div>
            </div>
            <div v-else-if="selectedEventTypeName === 'ocorrência especial'" class="dynamic-form-section card full-width">
                <h4 class="dynamic-form-title">Detalhes da Ocorrência Especial</h4>
                <div class="form-grid nested-grid">
                    <div class="form-group">
                        <label for="occurrence-type" class="form-label">Tipo da Ocorrência*</label>
                        <input id="occurrence-type" v-model="occurrence.occurrence_type" type="text" class="input" placeholder="Ex: Acidente, Doença Súbita, Fuga" required />
                    </div>
                    <div class="form-group full-width">
                        <label for="occurrence-description" class="form-label">Descrição Detalhada</label>
                        <textarea id="occurrence-description" v-model="occurrence.description" class="textarea" rows="3"></textarea>
                    </div>
                    <div class="form-group full-width">
                        <label for="occurrence-actions" class="form-label">Ações Tomadas</label>
                        <textarea id="occurrence-actions" v-model="occurrence.actions_taken" class="textarea" rows="2"></textarea>
                    </div>
                </div>
            </div>

          <div class="form-actions full-width">
            <button type="submit" class="button button-primary">
              {{ editing ? 'Atualizar Evento' : 'Salvar Evento' }}
            </button>
            <button type="button" class="button button-secondary" @click="closeModal">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showBatchEventModal" class="modal-overlay" @click.self="closeBatchEventRegistrationModal">
      <div class="modal-content card large-modal">
           <div class="modal-header">
              <h3 class="modal-title-text">Registrar Evento em Lote</h3>
              <button @click="closeBatchEventRegistrationModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <p class="modal-description panel-description">Selecione o lote (grupo de animais) e defina os detalhes do evento que será aplicado a todos eles.</p>

        <form @submit.prevent="handleBatchEventSubmit" class="modal-form form-grid">
          <div class="form-group full-width">
            <label for="batch-animal-group" class="form-label">Lote (Grupo de Animais)*</label>
            <select id="batch-animal-group" v-model.number="batchEventForm.animal_group_id" class="select" required>
              <option disabled :value="nullPlaceholder.animal_group">Selecione um lote/grupo</option>
              <option v-for="group in animalGroups" :key="group.id" :value="group.id">{{ group.name }}</option>
            </select>
            <p v-if="!animalGroups.length && !isLoadingAnimalGroups" class="form-text text-warning">Nenhum grupo de animais disponível. Cadastre grupos primeiro.</p>
            <p v-if="isLoadingAnimalGroups" class="form-text">Carregando grupos...</p>
          </div>

          <div class="form-group">
            <label for="batch-event-type" class="form-label">Tipo de Evento*</label>
            <select id="batch-event-type" v-model.number="batchEventForm.event_type" @change="handleBatchEventTypeChange" class="select" required>
              <option disabled :value="nullPlaceholder.event_type">Selecione um tipo</option>
              <option v-for="type in batchAllowedEventTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="batch-event-date" class="form-label">Data e Hora*</label>
            <input type="datetime-local" id="batch-event-date" v-model="batchEventForm.date" class="input" required />
          </div>
          <div class="form-group">
            <label for="batch-event-location" class="form-label">Localização</label>
            <input type="text" id="batch-event-location" v-model="batchEventForm.location" class="input" />
          </div>
          <div class="form-group full-width">
            <label for="batch-event-observations" class="form-label">Observações Gerais</label>
            <textarea id="batch-event-observations" v-model="batchEventForm.observations" class="textarea" rows="3"></textarea>
          </div>

          <div v-if="batchEventForm.event_type_name === 'movimentação' || batchEventForm.event_type_name === 'movimento'" class="dynamic-form-section card full-width">
            <h4 class="dynamic-form-title">Detalhes do Movimento em Lote</h4>
               <div class="form-grid nested-grid">
                <div class="form-group">
                    <label for="batch-origin-property" class="form-label">Propriedade Origem*</label>
                    <select id="batch-origin-property" v-model.number="batchEventForm.movement_details.origin_property" class="select" required>
                        <option disabled :value="nullPlaceholder.property">Selecione a origem</option>
                        <option v-for="prop in properties" :key="`batch-orig-${prop.id}`" :value="prop.id">{{ prop.name }}</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="batch-destination-property" class="form-label">Propriedade Destino*</label>
                    <select id="batch-destination-property" v-model.number="batchEventForm.movement_details.destination_property" class="select" required>
                        <option disabled :value="nullPlaceholder.property">Selecione o destino</option>
                        <option v-for="prop in properties" :key="`batch-dest-${prop.id}`" :value="prop.id">{{ prop.name }}</option>
                    </select>
                </div>
                <div class="form-group full-width">
                    <label for="batch-movement-reason" class="form-label">Razão/Motivo</label>
                    <textarea id="batch-movement-reason" v-model="batchEventForm.movement_details.reason" class="textarea" rows="2"></textarea>
                </div>
            </div>
          </div>
          <div v-else-if="batchEventForm.event_type_name === 'vacinação'" class="dynamic-form-section card full-width">
                <h4 class="dynamic-form-title">Detalhes da Vacinação em Lote</h4>
                <div class="form-grid nested-grid">
                    <div class="form-group"><label for="batch-vacine-name" class="form-label">Nome da Vacina*</label><input id="batch-vacine-name" v-model="batchEventForm.vacine_details.name" type="text" class="input" required /></div>
                    <div class="form-group"><label for="batch-vacine-dose" class="form-label">Dose (ex: mL, Un)*</label><input id="batch-vacine-dose" v-model="batchEventForm.vacine_details.dose" type="text" class="input" required /></div>
                    <div class="form-group"><label for="batch-vacine-manufacturer" class="form-label">Fabricante</label><input id="batch-vacine-manufacturer" v-model="batchEventForm.vacine_details.manufacturer" type="text" class="input" /></div>
                    <div class="form-group"><label for="batch-vacine-batch" class="form-label">Lote</label><input id="batch-vacine-batch" v-model="batchEventForm.vacine_details.batch" type="text" class="input" /></div>
                    <div class="form-group"><label for="batch-vacine-validity" class="form-label">Validade da Vacina*</label><input id="batch-vacine-validity" v-model="batchEventForm.vacine_details.validity" type="date" class="input" required /></div>
                    <div class="form-group"><label for="batch-vacine-next" class="form-label">Próxima Dose</label><input id="batch-vacine-next" v-model="batchEventForm.vacine_details.next_dose_date" type="datetime-local" class="input" /></div>
                </div>
            </div>
          <div v-else-if="batchEventForm.event_type_name === 'medicação'" class="dynamic-form-section card full-width">
              <h4 class="dynamic-form-title">Detalhes da Medicação em Lote</h4>
              <div class="form-grid nested-grid">
                  <div class="form-group"><label for="batch-med-name" class="form-label">Nome do Medicamento*</label><input id="batch-med-name" v-model="batchEventForm.medicine_details.name" type="text" class="input" required /></div>
                  <div class="form-group"><label for="batch-med-dose" class="form-label">Dose Administrada*</label><input id="batch-med-dose" v-model="batchEventForm.medicine_details.dose" type="text" class="input" required placeholder="Ex: 10mL"/></div>
                  <div class="form-group"><label for="batch-med-manufacturer" class="form-label">Fabricante</label><input id="batch-med-manufacturer" v-model="batchEventForm.medicine_details.manufacturer" type="text" class="input" /></div>
                  <div class="form-group"><label for="batch-med-batch" class="form-label">Lote</label><input id="batch-med-batch" v-model="batchEventForm.medicine_details.batch" type="text" class="input" /></div>
                  <div class="form-group"><label for="batch-med-validity" class="form-label">Validade do Medic.*</label><input id="batch-med-validity" v-model="batchEventForm.medicine_details.validity" type="date" class="input" required /></div>
                  <div class="form-group"><label for="batch-med-next" class="form-label">Próxima Dose</label><input id="batch-med-next" v-model="batchEventForm.medicine_details.next_dose_date" type="datetime-local" class="input" /></div>
                  <div class="form-group full-width"><label for="batch-med-reason" class="form-label">Motivo/Indicação</label><textarea id="batch-med-reason" v-model="batchEventForm.medicine_details.reason" class="textarea" rows="2"></textarea></div>
                  <div class="form-group"><label for="batch-med-withdrawal" class="form-label">Período de Carência (dias)</label><input id="batch-med-withdrawal" v-model.number="batchEventForm.medicine_details.withdrawal_time" type="number" class="input" min="0" /></div>
              </div>
          </div>
          <div v-else-if="batchEventForm.event_type_name === 'ocorrência especial'" class="dynamic-form-section card full-width">
              <h4 class="dynamic-form-title">Detalhes da Ocorrência Especial em Lote</h4>
              <div class="form-grid nested-grid">
                  <div class="form-group">
                      <label for="batch-occurrence-type" class="form-label">Tipo da Ocorrência*</label>
                      <input id="batch-occurrence-type" v-model="batchEventForm.special_occurrences_details.occurrence_type" type="text" class="input" placeholder="Ex: Surto de doença, Evento climático" required />
                  </div>
                  <div class="form-group full-width">
                      <label for="batch-occurrence-description" class="form-label">Descrição Detalhada</label>
                      <textarea id="batch-occurrence-description" v-model="batchEventForm.special_occurrences_details.description" class="textarea" rows="3"></textarea>
                  </div>
                  <div class="form-group full-width">
                      <label for="batch-occurrence-actions" class="form-label">Ações Tomadas</label>
                      <textarea id="batch-occurrence-actions" v-model="batchEventForm.special_occurrences_details.actions_taken" class="textarea" rows="2"></textarea>
                  </div>
              </div>
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="button button-primary" :disabled="!batchEventForm.animal_group_id || !batchEventForm.event_type">
              Registrar Eventos em Lote
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
      @close="closeNotification"
    />
  </section>
</template>

<script>
import {
  // Removidas as importações diretas de registerMovement, registerWeighing, etc., pois não serão mais chamadas assim
  // Elas ainda existem no eventService.js caso você precise delas para outros contextos.
  registerEvent, updateEvent, getEvents, deleteEvent, getEventDetails,
  registerBatchEvent 
} from '@/services/eventService';
import { getEventTypes, getProperties, getAnimalGroups } from '@/services/lookupService';
import { getUserProfile } from '@/services/userService';
import { getAnimals } from '@/services/animalService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'EventContent',
  components: {
    NotificationModal
  },
  data() {
    const nullPlaceholderVal = null;
    return {
      showModal: false,
      showBatchEventModal: false,
      editing: false,
      editingId: null, // Para o ID do Evento principal
      editingDetailId: null, // Para o ID do detalhe específico (Movement, Weighing etc.)
      user: null,
      animals: [],
      animalGroups: [],
      properties: [],
      events: [],
      isLoadingEvents: true,
      isLoadingAnimalGroups: false,

      nullPlaceholder: { 
          animal: nullPlaceholderVal,
          event_type: nullPlaceholderVal,
          property: nullPlaceholderVal,
          animal_group: nullPlaceholderVal,
      },

      form: { // Dados gerais do evento
        animal: nullPlaceholderVal,
        date: '',
        location: '',
        observations: '',
        event_type: nullPlaceholderVal
      },
      // Objetos para os detalhes específicos de cada tipo de evento
      movement: { origin_property: nullPlaceholderVal, destination_property: nullPlaceholderVal, reason: '', date: '' },
      weighing: { weight: null, date: '' },
      vaccine: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', date: '' },
      medicine: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null, date: '' },
      reproduction: { reproduction_type: '', male_id: nullPlaceholderVal, female_id: nullPlaceholderVal, result: null, date: '' },
      slaughter: { location: '', final_weight: null, inspection_result: null, date: '' },
      occurrence: { occurrence_type: '', description: '', actions_taken: '', date: '' },
      
      eventTypes: [], 

      batchEventForm: { /* ... (sem alterações aqui, já estava correto para lote) ... */
        animal_group_id: nullPlaceholderVal,
        event_type: nullPlaceholderVal,
        event_type_name: '', 
        date: '',
        location: '',
        observations: '',
        movement_details: { origin_property: nullPlaceholderVal, destination_property: nullPlaceholderVal, reason: '', date: '' },
        vacine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', date: '' },
        medicine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null, date: '' },
        special_occurrences_details: { occurrence_type: '', description: '', actions_taken: '', date: '' },
      },
      notification: { show: false, message: '', type: 'success' }
    };
  },
  computed: { /* ... (sem alterações nas computadas) ... */
    sortedEvents() {
        return [...this.events].sort((a, b) => new Date(b.date) - new Date(a.date));
    },
    selectedEventTypeName() {
      const selectedType = this.eventTypes.find(type => type.id === this.form.event_type);
      return selectedType ? selectedType.name.toLowerCase() : '';
    },
    animalIdToIdentificationMap() {
        return this.animals.reduce((acc, animal) => {
            acc[animal.id] = animal.identification;
            return acc;
        }, {});
    },
    batchAllowedEventTypes() {
      if (!this.eventTypes || this.eventTypes.length === 0) return [];
      const allowedNames = ['medicação', 'movimentação', 'ocorrência especial', 'vacinação'];
      return this.eventTypes.filter(type => type && type.name && allowedNames.includes(type.name.toLowerCase()));
    }
  },
  watch: { /* ... (sem alterações nos watchers) ... */
    'batchEventForm.event_type'(newVal) {
      if (newVal) {
        const selectedType = this.eventTypes.find(type => type.id === newVal);
        const isAllowed = this.batchAllowedEventTypes.some(allowedType => allowedType.id === newVal);
        if (selectedType && isAllowed) {
            this.batchEventForm.event_type_name = selectedType.name.toLowerCase();
        } else {
            this.batchEventForm.event_type_name = '';
            if(!isAllowed && newVal !== this.nullPlaceholder.event_type) {
                this.batchEventForm.event_type = this.nullPlaceholder.event_type; 
                 this.showAppNotification('Tipo de evento inválido para operação em lote.', 'warning');
            }
        }
      } else {
        this.batchEventForm.event_type_name = '';
      }
      this.resetBatchEventSpecificDetails(); 
    },
    'form.animal'(newAnimalId) {
        if (this.selectedEventTypeName === 'reprodução') {
            this.reproduction.female_id = newAnimalId || this.nullPlaceholder.animal;
        }
    },
    'form.event_type'(newEventTypeId) {
        const typeName = this.eventTypes.find(type => type.id === newEventTypeId)?.name.toLowerCase();
        if (typeName === 'reprodução') {
            this.reproduction.female_id = this.form.animal || this.nullPlaceholder.animal;
        }
    }
  },
  methods: {
    showAppNotification(message, type = 'success', duration = 3000) {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      if (duration) {
        setTimeout(() => { this.notification.show = false; }, duration);
      }
    },
    closeNotification() { this.notification.show = false; },
    
    async loadUserAndAnimals() { /* ... (sem alterações) ... */
      try {
        this.user = await getUserProfile();
        const list = await getAnimals({ owner: this.user.id, is_active: true });
        this.animals = list.sort((a,b) => a.identification.localeCompare(b.identification));
      } catch (e) {
        console.error('Erro ao carregar usuário ou animais:', e.response?.data || e);
        this.showAppNotification('Erro ao carregar dados de usuário/animais.', 'error');
      }
    },
    async loadAnimalGroups() { /* ... (sem alterações) ... */
        this.isLoadingAnimalGroups = true;
        try {
            this.animalGroups = await getAnimalGroups();
        } catch (e) {
            console.error('Erro ao carregar grupos de animais:', e.response?.data || e);
            this.showAppNotification('Erro ao carregar grupos de animais (lotes).', 'error');
        } finally {
            this.isLoadingAnimalGroups = false;
        }
    },
    async loadEventData() { /* ... (sem alterações) ... */
        this.isLoadingEvents = true;
        try {
            if (this.user && this.user.id) {
                this.events = await getEvents(); 
            } else {
                this.events = [];
            }
        } catch (e) {
            console.error('Erro ao carregar eventos:', e.response?.data || e);
            this.showAppNotification('Erro ao carregar a lista de eventos.', 'error');
            this.events = [];
        } finally {
            this.isLoadingEvents = false;
        }
    },
    async loadEventTypesAndProperties() { /* ... (sem alterações) ... */
      try {
        [this.eventTypes, this.properties] = await Promise.all([
            getEventTypes(),
            getProperties()
        ]);
      } catch (e) {
        console.error('Erro ao carregar tipos de evento ou propriedades:', e.response?.data || e);
        this.showAppNotification('Erro ao carregar tipos de evento ou propriedades.', 'error');
      }
    },
    openModal() { /* ... (sem alterações) ... */
      this.resetIndividualForm();
      this.editing = false;
      this.editingId = null;
      this.editingDetailId = null; // Resetar ID do detalhe também
      this.form.date = new Date().toISOString().slice(0, 16);
      this.showModal = true;
    },
    closeModal() { /* ... (sem alterações) ... */
      this.showModal = false;
      this.resetIndividualForm(); 
    },
    async editEvent(eventItem) {
        this.resetIndividualForm(); 
        this.editing = true;
        this.editingId = eventItem.id; 
        try {
            const fullEventDetails = await getEventDetails(eventItem.id, eventItem.event_type);
            if (!fullEventDetails) {
                this.showAppNotification('Erro: Detalhes do evento não encontrados.', 'error');
                this.closeModal();
                return;
            }
            
            this.form.animal = fullEventDetails.animal;
            this.form.date = fullEventDetails.date ? new Date(fullEventDetails.date).toISOString().slice(0, 16) : '';
            this.form.location = fullEventDetails.location;
            this.form.observations = fullEventDetails.observations;
            this.form.event_type = fullEventDetails.event_type;
            
            const details = fullEventDetails.details;
            if (details) {
                this.editingDetailId = details.id; // Guarda o ID do detalhe para atualização
                const eventTypeName = this.eventTypes.find(type => type.id === fullEventDetails.event_type)?.name.toLowerCase();
                const detailDateToUse = details.date ? new Date(details.date).toISOString().slice(0,16) : this.form.date;

                // Preenche os respectivos objetos de detalhes
                if (eventTypeName === 'movimentação' || eventTypeName === 'movimento') this.movement = { ...this.movement, ...details, date: detailDateToUse };
                else if (eventTypeName === 'pesagem') this.weighing = { ...this.weighing, ...details, date: detailDateToUse };
                else if (eventTypeName === 'vacinação') this.vaccine = { ...this.vaccine, ...details, validity: details.validity ? new Date(details.validity).toISOString().slice(0, 10) : '', next_dose_date: details.next_dose_date ? new Date(details.next_dose_date).toISOString().slice(0, 16) : '', date: detailDateToUse };
                else if (eventTypeName === 'medicação') this.medicine = { ...this.medicine, ...details, validity: details.validity ? new Date(details.validity).toISOString().slice(0, 10) : '', next_dose_date: details.next_dose_date ? new Date(details.next_dose_date).toISOString().slice(0, 16) : '', date: detailDateToUse };
                else if (eventTypeName === 'reprodução') this.reproduction = { ...this.reproduction, ...details, date: details.date ? new Date(details.date).toISOString().slice(0,16) : this.form.date };
                else if (eventTypeName === 'abate') this.slaughter = { ...this.slaughter, ...details, date: detailDateToUse };
                else if (eventTypeName === 'ocorrência especial') this.occurrence = { ...this.occurrence, ...details, date: detailDateToUse };
            } else {
                this.editingDetailId = null; // Não há detalhe para editar
            }
            this.showModal = true;
        } catch (e) {
            console.error('Erro ao carregar evento para edição:', e.response?.data || e);
            this.showAppNotification('Erro ao carregar evento para edição.', 'error');
        }
    },
    handleEventTypeChange() { 
        this.editingDetailId = null; // Reseta o ID do detalhe ao mudar o tipo
        this.resetIndividualSpecificDetails(); 
    },

    // MÉTODO handleSubmit AJUSTADO
    async handleSubmit() {
        if (this.form.animal === this.nullPlaceholder.animal || !this.form.date || this.form.event_type === this.nullPlaceholder.event_type) {
            this.showAppNotification('Por favor, preencha animal, tipo de evento e data.', 'warning'); return;
        }

        // Monta o payload principal
        let payload = { 
            ...this.form, 
            recorded_by: this.user.id,
            details: null // Inicializa o campo de detalhes
        };
        
        const eventTypeName = this.selectedEventTypeName;
        const detailDate = this.form.date; // Data base para os detalhes

        // Adiciona os detalhes específicos ao payload, se aplicável
        if (eventTypeName === 'movimentação' || eventTypeName === 'movimento') {
            if (this.movement.origin_property === this.nullPlaceholder.property || this.movement.destination_property === this.nullPlaceholder.property) { this.showAppNotification('Preencha origem e destino do movimento.', 'warning'); return; }
            payload.details = { ...this.movement, date: this.movement.date || detailDate };
        } else if (eventTypeName === 'pesagem') {
            if (this.weighing.weight === null || String(this.weighing.weight).trim() === '') { this.showAppNotification('Preencha o peso.', 'warning'); return; }
            payload.details = { ...this.weighing, date: this.weighing.date || detailDate };
        } else if (eventTypeName === 'vacinação') {
            if (!this.vaccine.name || !this.vaccine.validity || !this.vaccine.dose) { this.showAppNotification('Preencha nome, validade e dose da vacina.', 'warning'); return; }
            payload.details = { ...this.vaccine, date: this.vaccine.date || detailDate };
        } else if (eventTypeName === 'medicação') {
            if (!this.medicine.name || !this.medicine.validity || !this.medicine.dose) { this.showAppNotification('Preencha nome, validade e dose do medicamento.', 'warning'); return; }
            payload.details = { ...this.medicine, date: this.medicine.date || detailDate };
        } else if (eventTypeName === 'reprodução') {
            if (!this.reproduction.reproduction_type || this.reproduction.female_id === this.nullPlaceholder.animal) { this.showAppNotification('Preencha tipo de reprodução e fêmea.', 'warning'); return; }
            payload.details = { ...this.reproduction, date: this.reproduction.date || detailDate };
        } else if (eventTypeName === 'abate') {
            if (!this.slaughter.location || this.slaughter.final_weight === null || String(this.slaughter.final_weight).trim() === '') { this.showAppNotification('Preencha local e peso final do abate.', 'warning'); return; }
            payload.details = { ...this.slaughter, date: this.slaughter.date || detailDate };
        } else if (eventTypeName === 'ocorrência especial') {
            if (!this.occurrence.occurrence_type) { this.showAppNotification('Preencha o tipo de ocorrência especial.', 'warning'); return; }
            payload.details = { ...this.occurrence, date: this.occurrence.date || detailDate };
        }
        // Se o evento não tiver detalhes específicos, payload.details permanecerá null (o backend deve lidar com isso)

        // Remove o campo 'event' dos sub-objetos de detalhes, pois ele será criado no backend.
        // O backend espera os dados dos detalhes, e ele mesmo fará a associação com o Evento principal.
        if (payload.details && payload.details.hasOwnProperty('event')) {
            delete payload.details.event;
        }
        
        try {
            let apiResponse;
            if (this.editing) {
                // Na edição, o backend `EventViewSet.update` também espera 'details' aninhado
                // e o ID do detalhe específico se já existir para atualização.
                // Adicionamos `editingDetailId` ao payload se estivermos editando um detalhe existente.
                if (this.editingDetailId && payload.details) {
                    payload.details.id = this.editingDetailId;
                }
                apiResponse = await updateEvent(this.editingId, payload);
                this.showAppNotification('Evento atualizado com sucesso!', 'success');
            } else { // Criando novo evento
                apiResponse = await registerEvent(payload);
                this.showAppNotification('Evento registrado com sucesso!', 'success');
            }
            this.closeModal(); 
            await this.loadEventData();
        } catch (e) {
            console.error('Erro ao salvar evento:', e.response?.data || e);
            let errorMessage = 'Erro ao salvar evento.';
            if (e.response?.data && typeof e.response.data === 'object') {
                errorMessage += ' Detalhes: ' + Object.entries(e.response.data).map(([k, v]) => {
                    if (k === 'details' && typeof v === 'object') {
                        return 'Detalhes: ' + Object.entries(v).map(([dk, dv]) => `${dk}: ${Array.isArray(dv) ? dv.join(', ') : dv}`).join(', ');
                    }
                    return `${k}: ${Array.isArray(v) ? v.join(', ') : v}`;
                }).join('; ');
            } else if (e.response?.data) { errorMessage += ` ${e.response.data}`; }
            this.showAppNotification(errorMessage, 'error');
        }
    },
    async confirmDelete(id) { /* ... (sem alterações) ... */
        if (confirm('Tem certeza que deseja deletar este evento? Esta ação não pode ser desfeita.')) {
            try { await deleteEvent(id); this.showAppNotification('Evento deletado!', 'success'); await this.loadEventData(); }
            catch (e) { console.error('Erro ao deletar evento:', e.response?.data || e); this.showAppNotification('Erro ao deletar evento.', 'error'); }
        }
    },
    openBatchEventRegistrationModal() { this.resetBatchForm(); this.batchEventForm.date = new Date().toISOString().slice(0, 16); this.showBatchEventModal = true; },
    closeBatchEventRegistrationModal() { this.showBatchEventModal = false; this.resetBatchForm(); },
    handleBatchEventTypeChange() { this.resetBatchEventSpecificDetails(); },
    async handleBatchEventSubmit() { 
      if (this.batchEventForm.animal_group_id === this.nullPlaceholder.animal_group) { this.showAppNotification('Selecione um lote/grupo de animais.', 'warning'); return; }
      if (this.batchEventForm.event_type === this.nullPlaceholder.event_type || !this.batchEventForm.date) { this.showAppNotification('Preencha tipo de evento e data para o lote.', 'warning'); return; }
      
      const eventTypeName = this.batchEventForm.event_type_name;
      const payload = { 
          animal_group_id: this.batchEventForm.animal_group_id, 
          event_type: this.batchEventForm.event_type, 
          date: this.batchEventForm.date, 
          location: this.batchEventForm.location || null, 
          observations: this.batchEventForm.observations || null, 
          recorded_by: this.user.id 
      };
      const detailDate = this.batchEventForm.date;

      if (eventTypeName === 'movimentação' || eventTypeName === 'movimento') {
          if (this.batchEventForm.movement_details.origin_property === this.nullPlaceholder.property || this.batchEventForm.movement_details.destination_property === this.nullPlaceholder.property) { this.showAppNotification('Preencha origem e destino do movimento em lote.', 'warning'); return; }
          payload.movement_details = { ...this.batchEventForm.movement_details, date: detailDate };
      } else if (eventTypeName === 'vacinação') {
          if (!this.batchEventForm.vacine_details.name || !this.batchEventForm.vacine_details.validity || !this.batchEventForm.vacine_details.dose) { this.showAppNotification('Preencha nome, validade e dose da vacina para o lote.', 'warning'); return; }
          payload.vacine_details = { ...this.batchEventForm.vacine_details, date: detailDate };
      } else if (eventTypeName === 'medicação') {
          if (!this.batchEventForm.medicine_details.name || !this.batchEventForm.medicine_details.validity || !this.batchEventForm.medicine_details.dose) { this.showAppNotification('Preencha nome, validade e dose do medicamento para o lote.', 'warning'); return; }
          payload.medicine_details = { ...this.batchEventForm.medicine_details, date: detailDate };
      } else if (eventTypeName === 'ocorrência especial') {
          if (!this.batchEventForm.special_occurrences_details.occurrence_type) { this.showAppNotification('Preencha o tipo de ocorrência especial para o lote.', 'warning'); return; }
          payload.special_occurrences_details = { ...this.batchEventForm.special_occurrences_details, date: detailDate };
      }

      try {
          const response = await registerBatchEvent(payload);
          this.showAppNotification(response.message || `Evento em lote registrado com sucesso para o grupo!`, 'success');
          this.closeBatchEventRegistrationModal(); 
          await this.loadEventData();
      } catch (error) {
          console.error('Erro ao registrar evento em lote:', error.response?.data || error);
          let errorMessage = 'Erro ao registrar evento em lote.';
          if (error.response?.data && typeof error.response.data === 'object') {
            errorMessage += ' Detalhes: ' + Object.entries(error.response.data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join('; ');
          } else if (error.response?.data) { errorMessage += ` ${error.response.data}`; }
          this.showAppNotification(errorMessage, 'error');
      }
    },
    resetIndividualForm() { /* ... (sem alterações) ... */
        const currentDate = new Date().toISOString().slice(0, 16);
        this.form = { animal: this.nullPlaceholder.animal, date: currentDate, location: '', observations: '', event_type: this.nullPlaceholder.event_type };
        this.editingDetailId = null; // Limpa o ID do detalhe também
        this.resetIndividualSpecificDetails(currentDate);
    },
    resetIndividualSpecificDetails(dateToUse) { /* ... (sem alterações) ... */
        const eventDate = dateToUse || new Date().toISOString().slice(0, 16);
        this.movement = { origin_property: this.nullPlaceholder.property, destination_property: this.nullPlaceholder.property, reason: '', date: eventDate };
        this.weighing = { weight: null, date: eventDate };
        this.vaccine = { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', date: eventDate /*, dose_unit: '' */ };
        this.medicine = { name: '', manufacturer: '', batch: '', validity: '', dose: null, next_dose_date: '', reason: '', withdrawal_time: null, date: eventDate /*, dose_unit: '' */ };
        this.reproduction = { reproduction_type: '', male_id: this.nullPlaceholder.animal, female_id: this.nullPlaceholder.animal, result: null, date: eventDate };
        this.slaughter = { location: '', final_weight: null, inspection_result: null, date: eventDate };
        this.occurrence = { occurrence_type: '', description: '', actions_taken: '', date: eventDate };
    },
    resetBatchForm() { /* ... (sem alterações) ... */
        const currentDate = new Date().toISOString().slice(0, 16);
        this.batchEventForm = {
            animal_group_id: this.nullPlaceholder.animal_group, 
            event_type: this.nullPlaceholder.event_type, 
            event_type_name: '',
            date: currentDate, 
            location: '', 
            observations: '',
            movement_details: { origin_property: this.nullPlaceholder.property, destination_property: this.nullPlaceholder.property, reason: '', date: currentDate },
            vacine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: currentDate },
            medicine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: currentDate },
            special_occurrences_details: { occurrence_type: '', description: '', actions_taken: '', date: currentDate },
        };
    },
    resetBatchEventSpecificDetails(dateToUse) { /* ... (sem alterações) ... */
        const eventDate = dateToUse || this.batchEventForm.date || new Date().toISOString().slice(0, 16);
        this.batchEventForm.movement_details = { origin_property: this.nullPlaceholder.property, destination_property: this.nullPlaceholder.property, reason: '', date: eventDate };
        this.batchEventForm.vacine_details = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: eventDate };
        this.batchEventForm.medicine_details = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: eventDate };
        this.batchEventForm.special_occurrences_details = { occurrence_type: '', description: '', actions_taken: '', date: eventDate };
    },
    getAnimalIdentification(animalId) { return this.animalIdToIdentificationMap[animalId] || 'N/D'; },
    getEventTypeName(eventTypeId) { const type = this.eventTypes.find(t => t.id === eventTypeId); return type ? type.name : 'N/D'; },
    formatDateTime(dateTimeString) { /* ... (sem alterações) ... */
        if (!dateTimeString) return 'N/A';
        try {
            const date = new Date(dateTimeString);
            if (isNaN(date.getTime())) return 'Data Inválida';
            return date.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
        } catch (e) { return "Data Inválida"; }
    }
  },
  async mounted() { /* ... (sem alterações) ... */
    this.isLoadingEvents = true;
    await this.loadUserAndAnimals();
    await this.loadEventTypesAndProperties();
    await this.loadAnimalGroups();
    if (this.user && this.user.id) {
        await this.loadEventData(); 
    } else {
        this.isLoadingEvents = false;
    }
  }
};
</script>

<style scoped>
/* Seu CSS Scoped Existente ... */
.form-text.text-warning {
  color: var(--color-warning); 
  font-weight: var(--fw-medium);
}
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
.panel-actions.header-actions-event {
  display: flex;
  gap: var(--sp-sm);
}
.panel-actions .button {
    font-size: var(--fs-small);
    padding: var(--sp-xs) var(--sp-sm);
    display: flex;
    align-items: center;
    gap: var(--sp-xs);
}
.panel-actions .button svg {
    margin-right: 0;
}

.panel-description {
  text-align: left;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
  max-width: none;
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
  min-width: 700px;
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
.data-table .th-observations {
    min-width: 200px;
}
.data-table .truncate-text {
  max-width: 200px;
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
    gap: var(--sp-xxs);
}

.empty-state.card {
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
}
.empty-state p {
    color: var(--color-text-muted);
    margin-bottom: var(--sp-md);
}
.empty-state .button {
    margin-top: var(--sp-sm);
}

.modal-description {
  text-align: left;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-md);
  font-size: var(--fs-base);
}

.dynamic-form-section {
  grid-column: 1 / -1;
  margin-top: var(--sp-md);
  padding: var(--sp-md);
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
}
.dynamic-form-title {
  grid-column: 1 / -1;
  font-family: var(--font-heading);
  color: var(--color-text-primary);
  font-size: var(--fs-large);
  font-weight: var(--fw-semibold);
  margin-top: 0;
  margin-bottom: var(--sp-md);
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) dashed var(--color-border);
}

.form-text {
    display: block;
    margin-top: var(--sp-xxs);
    font-size: var(--fs-small);
    color: var(--color-text-muted);
}

@media (max-width: 768px) {
  .panel-header {
      flex-direction: column;
      align-items: stretch;
      gap: var(--sp-sm);
  }
  .panel-title-text {
      text-align: center;
      margin-bottom: var(--sp-md);
  }
  .panel-actions.header-actions-event {
    flex-direction: column;
    align-items: stretch;
  }
  .panel-actions .button {
    width: 100%;
  }

  .form-grid, .form-grid.nested-grid, .dynamic-form-section .form-grid {
    grid-template-columns: 1fr;
  }
  .data-table {
    min-width: auto;
  }
  .data-table th, .data-table td {
      padding: var(--sp-xs) var(--sp-sm);
  }
  .actions-cell .button {
    margin-bottom: var(--sp-xxs);
    margin-left: 0;
    margin-right: var(--sp-xs);
  }
  .actions-cell .button:last-child {
      margin-right: 0;
  }
}

.loading-state {
    text-align: center;
    padding: var(--sp-xl);
    color: var(--color-text-muted);
    font-size: var(--fs-large);
}
</style>