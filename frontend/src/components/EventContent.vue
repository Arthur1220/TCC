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
            <th class="text-right">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="eventItem in sortedEvents" :key="eventItem.id" class="table-row-hover">
            <td data-label="Animal">{{ getAnimalIdentification(eventItem.animal) }}</td>
            <td data-label="Tipo de Evento">{{ getEventTypeName(eventItem.event_type) }}</td>
            <td data-label="Data">{{ formatDateTime(eventItem.date) }}</td>
            <td data-label="Localização">{{ eventItem.location || 'N/A' }}</td>
            <td data-label="Observações" class="truncate-text" :title="eventItem.observations || ''">{{ eventItem.observations || 'N/A' }}</td>
            <td data-label="Ações" class="actions-cell">
              <button class="button button-outline-primary button-sm" @click="editEvent(eventItem)" title="Editar Evento">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
                Editar
              </button>
              <button class="button button-danger button-sm" @click="confirmDelete(eventItem.id)" title="Deletar Evento">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
                Deletar
              </button>
            </td>
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
                    <div class="form-group"><label for="vacine-dose" class="form-label">Dose (ex: mL, Un)*</label><input id="vacine-dose" v-model="vaccine.dose" type="text" class="input" required /></div>
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
                    <div class="form-group"><label for="med-dose" class="form-label">Dose Administrada*</label><input id="med-dose" v-model="medicine.dose" type="text" class="input" required placeholder="Ex: 10mL, 1 comprimido"/></div>
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
  registerEvent, updateEvent, getEvents, deleteEvent, getEventDetails,
  registerMovement, updateMovement,
  registerWeighing, updateWeighing,
  registerVacine, updateVacine,
  registerMedicine, updateMedicine,
  registerReproduction, updateReproduction,
  registerSlaughter, updateSlaughter,
  registerSpecialOccurrence, updateSpecialOccurrence,
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
      editingId: null,
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

      form: {
        animal: nullPlaceholderVal,
        date: '',
        location: '',
        observations: '',
        event_type: nullPlaceholderVal
      },
      movement: { event: null, origin_property: nullPlaceholderVal, destination_property: nullPlaceholderVal, reason: '', date: '' },
      weighing: { event: null, weight: null, date: '' },
      vaccine: { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: '' },
      medicine: { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: '' },
      reproduction: { event: null, reproduction_type: '', male_id: nullPlaceholderVal, female_id: nullPlaceholderVal, result: null, date: '' },
      slaughter: { event: null, location: '', final_weight: null, inspection_result: null, date: '' },
      occurrence: { event: null, occurrence_type: '', description: '', actions_taken: '', date: '' },
      
      eventTypes: [], 

      batchEventForm: {
        animal_group_id: nullPlaceholderVal,
        event_type: nullPlaceholderVal,
        event_type_name: '', 
        date: '',
        location: '',
        observations: '',
        movement_details: { origin_property: nullPlaceholderVal, destination_property: nullPlaceholderVal, reason: '', date: '' },
        vacine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: '' },
        medicine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: '' },
        special_occurrences_details: { occurrence_type: '', description: '', actions_taken: '', date: '' },
        // reproduction_details e slaughter_details removidos daqui pois não estão em batchAllowedEventTypes
      },
      notification: { show: false, message: '', type: 'success' }
    };
  },
  computed: {
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
      // CORREÇÃO APLICADA AQUI: Lista de nomes permitidos para lote
      const allowedNames = ['medicação', 'movimentação', 'ocorrência especial', 'vacinação'];
      return this.eventTypes.filter(type => type && type.name && allowedNames.includes(type.name.toLowerCase()));
    }
  },
  watch: {
    'batchEventForm.event_type'(newVal) {
      if (newVal) {
        const selectedType = this.eventTypes.find(type => type.id === newVal);
        // Certifica-se que o tipo selecionado está entre os permitidos para lote
        const isAllowed = this.batchAllowedEventTypes.some(allowedType => allowedType.id === newVal);
        if (selectedType && isAllowed) {
            this.batchEventForm.event_type_name = selectedType.name.toLowerCase();
        } else {
            // Se por algum motivo um tipo não permitido for setado, limpa o nome
            // e talvez até o event_type em si para evitar inconsistências.
            this.batchEventForm.event_type_name = '';
            if(!isAllowed && newVal !== this.nullPlaceholder.event_type) {
                this.batchEventForm.event_type = this.nullPlaceholder.event_type; // Força reset
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
    
    async loadUserAndAnimals() {
      try {
        this.user = await getUserProfile();
        const list = await getAnimals({ owner: this.user.id, is_active: true });
        this.animals = list.sort((a,b) => a.identification.localeCompare(b.identification));
      } catch (e) {
        console.error('Erro ao carregar usuário ou animais:', e.response?.data || e);
        this.showAppNotification('Erro ao carregar dados de usuário/animais.', 'error');
      }
    },
    async loadAnimalGroups() {
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
    async loadEventData() {
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
    async loadEventTypesAndProperties() {
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
    openModal() {
      this.resetIndividualForm();
      this.editing = false;
      this.editingId = null;
      this.form.date = new Date().toISOString().slice(0, 16);
      this.showModal = true;
    },
    closeModal() {
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
                const eventTypeName = this.eventTypes.find(type => type.id === fullEventDetails.event_type)?.name.toLowerCase();
                const detailDateToUse = details.date ? new Date(details.date).toISOString().slice(0,16) : this.form.date;

                if (eventTypeName === 'movimentação' || eventTypeName === 'movimento') this.movement = { ...this.movement, ...details, date: detailDateToUse };
                else if (eventTypeName === 'pesagem') this.weighing = { ...this.weighing, ...details, date: detailDateToUse };
                else if (eventTypeName === 'vacinação') this.vaccine = { ...this.vaccine, ...details, validity: details.validity ? new Date(details.validity).toISOString().slice(0, 10) : '', next_dose_date: details.next_dose_date ? new Date(details.next_dose_date).toISOString().slice(0, 16) : '', date: detailDateToUse };
                else if (eventTypeName === 'medicação') this.medicine = { ...this.medicine, ...details, validity: details.validity ? new Date(details.validity).toISOString().slice(0, 10) : '', next_dose_date: details.next_dose_date ? new Date(details.next_dose_date).toISOString().slice(0, 16) : '', date: detailDateToUse };
                else if (eventTypeName === 'reprodução') this.reproduction = { ...this.reproduction, ...details, date: details.date ? new Date(details.date).toISOString().slice(0,16) : this.form.date };
                else if (eventTypeName === 'abate') this.slaughter = { ...this.slaughter, ...details, date: detailDateToUse };
                else if (eventTypeName === 'ocorrência especial') this.occurrence = { ...this.occurrence, ...details, date: detailDateToUse };
            }
            this.showModal = true;
        } catch (e) {
            console.error('Erro ao carregar evento para edição:', e.response?.data || e);
            this.showAppNotification('Erro ao carregar evento para edição.', 'error');
        }
    },
    handleEventTypeChange() { this.resetIndividualSpecificDetails(); },
    async handleSubmit() {
        if (this.form.animal === this.nullPlaceholder.animal || !this.form.date || this.form.event_type === this.nullPlaceholder.event_type) {
            this.showAppNotification('Por favor, preencha animal, tipo de evento e data.', 'warning'); return;
        }
        let eventData = { ...this.form, recorded_by: this.user.id };
        const eventTypeName = this.selectedEventTypeName;
        let specificEventPayload = null;
        let specificServiceRegister = null;
        let specificServiceUpdate = null;
        let detailIdToUpdate = null;
        const detailDate = this.form.date;

        if (eventTypeName === 'movimentação' || eventTypeName === 'movimento') {
            if (this.movement.origin_property === this.nullPlaceholder.property || this.movement.destination_property === this.nullPlaceholder.property) { this.showAppNotification('Preencha origem e destino do movimento.', 'warning'); return; }
            specificEventPayload = { ...this.movement, date: detailDate }; specificServiceRegister = registerMovement; specificServiceUpdate = updateMovement;
        } else if (eventTypeName === 'pesagem') {
            if (this.weighing.weight === null || String(this.weighing.weight).trim() === '') { this.showAppNotification('Preencha o peso.', 'warning'); return; }
            specificEventPayload = { ...this.weighing, date: detailDate }; specificServiceRegister = registerWeighing; specificServiceUpdate = updateWeighing;
        } else if (eventTypeName === 'vacinação') {
            if (!this.vaccine.name || !this.vaccine.validity || !this.vaccine.dose) { this.showAppNotification('Preencha nome, validade e dose da vacina.', 'warning'); return; }
            specificEventPayload = { ...this.vaccine, date: detailDate }; specificServiceRegister = registerVacine; specificServiceUpdate = updateVacine;
        } else if (eventTypeName === 'medicação') {
            if (!this.medicine.name || !this.medicine.validity || !this.medicine.dose) { this.showAppNotification('Preencha nome, validade e dose do medicamento.', 'warning'); return; }
            specificEventPayload = { ...this.medicine, date: detailDate }; specificServiceRegister = registerMedicine; specificServiceUpdate = updateMedicine;
        } else if (eventTypeName === 'reprodução') {
            if (!this.reproduction.reproduction_type || this.reproduction.female_id === this.nullPlaceholder.animal) { this.showAppNotification('Preencha tipo de reprodução e fêmea (animal principal do evento).', 'warning'); return; }
            specificEventPayload = { ...this.reproduction, date: this.reproduction.date || detailDate }; 
            specificServiceRegister = registerReproduction; specificServiceUpdate = updateReproduction;
        } else if (eventTypeName === 'abate') {
            if (!this.slaughter.location || this.slaughter.final_weight === null || String(this.slaughter.final_weight).trim() === '') { this.showAppNotification('Preencha local e peso final do abate.', 'warning'); return; }
            specificEventPayload = { ...this.slaughter, date: detailDate }; specificServiceRegister = registerSlaughter; specificServiceUpdate = updateSlaughter;
        } else if (eventTypeName === 'ocorrência especial') {
            if (!this.occurrence.occurrence_type) { this.showAppNotification('Preencha o tipo de ocorrência especial.', 'warning'); return; }
            specificEventPayload = { ...this.occurrence, date: detailDate }; specificServiceRegister = registerSpecialOccurrence; specificServiceUpdate = updateSpecialOccurrence;
        }
        
        try {
            let resEvent;
            if (this.editing) {
                resEvent = await updateEvent(this.editingId, eventData);
                if (specificEventPayload && specificServiceUpdate) {
                    const fullEventDetails = await getEventDetails(resEvent.id, resEvent.event_type);
                    detailIdToUpdate = fullEventDetails.details ? fullEventDetails.details.id : null;
                    if (detailIdToUpdate) {
                        specificEventPayload.event = resEvent.id;
                        await specificServiceUpdate(detailIdToUpdate, specificEventPayload);
                    } else if (specificServiceRegister) { 
                        specificEventPayload.event = resEvent.id;
                        await specificServiceRegister(specificEventPayload);
                    }
                }
                this.showAppNotification('Evento atualizado com sucesso!', 'success');
            } else { 
                resEvent = await registerEvent(eventData);
                if (specificEventPayload && specificServiceRegister) {
                    specificEventPayload.event = resEvent.id;
                    await specificServiceRegister(specificEventPayload);
                }
                this.showAppNotification('Evento registrado com sucesso!', 'success');
            }
            this.closeModal(); await this.loadEventData();
        } catch (e) {
            console.error('Erro ao salvar evento:', e.response?.data || e);
            let errorMessage = 'Erro ao salvar evento.';
            if (e.response?.data && typeof e.response.data === 'object') {
                errorMessage += ' Detalhes: ' + Object.entries(e.response.data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join('; ');
            } else if (e.response?.data) { errorMessage += ` ${e.response.data}`; }
            this.showAppNotification(errorMessage, 'error');
        }
    },
    async confirmDelete(id) {
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
      // Não é necessário adicionar 'abate' e 'reprodução' aqui, pois eles não estão em batchAllowedEventTypes

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
    resetIndividualForm() {
        const currentDate = new Date().toISOString().slice(0, 16);
        this.form = { animal: this.nullPlaceholder.animal, date: currentDate, location: '', observations: '', event_type: this.nullPlaceholder.event_type };
        this.resetIndividualSpecificDetails(currentDate);
    },
    resetIndividualSpecificDetails(dateToUse) {
        const eventDate = dateToUse || new Date().toISOString().slice(0, 16);
        this.movement = { event: null, origin_property: this.nullPlaceholder.property, destination_property: this.nullPlaceholder.property, reason: '', date: eventDate };
        this.weighing = { event: null, weight: null, date: eventDate };
        this.vaccine = { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: eventDate };
        this.medicine = { event: null, name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: eventDate };
        this.reproduction = { event: null, reproduction_type: '', male_id: this.nullPlaceholder.animal, female_id: this.nullPlaceholder.animal, result: null, date: eventDate };
        this.slaughter = { event: null, location: '', final_weight: null, inspection_result: null, date: eventDate };
        this.occurrence = { event: null, occurrence_type: '', description: '', actions_taken: '', date: eventDate };
    },
    resetBatchForm() {
        const currentDate = new Date().toISOString().slice(0, 16);
        this.batchEventForm = {
            animal_group_id: this.nullPlaceholder.animal_group, 
            event_type: this.nullPlaceholder.event_type, 
            event_type_name: '',
            date: currentDate, 
            location: '', 
            observations: '',
            // Reset details objects
            movement_details: { origin_property: this.nullPlaceholder.property, destination_property: this.nullPlaceholder.property, reason: '', date: currentDate },
            vacine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: currentDate },
            medicine_details: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: currentDate },
            special_occurrences_details: { occurrence_type: '', description: '', actions_taken: '', date: currentDate },
        };
    },
    resetBatchEventSpecificDetails(dateToUse) { // Chamado quando o tipo de evento em lote muda
        const eventDate = dateToUse || this.batchEventForm.date || new Date().toISOString().slice(0, 16);
        // Apenas reseta os detalhes dos tipos permitidos
        this.batchEventForm.movement_details = { origin_property: this.nullPlaceholder.property, destination_property: this.nullPlaceholder.property, reason: '', date: eventDate };
        this.batchEventForm.vacine_details = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', date: eventDate };
        this.batchEventForm.medicine_details = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: null, date: eventDate };
        this.batchEventForm.special_occurrences_details = { occurrence_type: '', description: '', actions_taken: '', date: eventDate };
    },
    getAnimalIdentification(animalId) { return this.animalIdToIdentificationMap[animalId] || 'N/D'; },
    getEventTypeName(eventTypeId) { const type = this.eventTypes.find(t => t.id === eventTypeId); return type ? type.name : 'N/D'; },
    formatDateTime(dateTimeString) {
        if (!dateTimeString) return 'N/A';
        try {
            const date = new Date(dateTimeString);
            if (isNaN(date.getTime())) return 'Data Inválida';
            return date.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
        } catch (e) { return "Data Inválida"; }
    }
  },
  async mounted() {
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
  border-radius: var(--border-radius); /* Adicionado para consistência */
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