<!-- File: src/components/EventContent.vue -->
<template>
  <section class="content-panel">
    <h2 class="panel-title">Eventos</h2>
    <p class="panel-description">
      Nesta tela você pode registrar novos eventos para seus animais ou editar registros existentes.
    </p>

    <!-- Botão para abrir modal de registrar -->
    <div class="add-button-wrapper">
      <button class="button-primary" @click="openModal">
        + Registrar Evento
      </button>
    </div>

    <!-- Modal de Cadastrar/Editar Evento -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">{{ editing ? 'Editar Evento' : 'Registrar Evento' }}</h3>
        <form @submit.prevent="handleSubmit" class="form-group">
          <!-- Campos Comuns -->
          <label for="animal">ID do Animal</label>
          <input id="animal" v-model.number="form.animal" type="number" required />

          <label for="date">Data</label>
          <input id="date" v-model="form.date" type="date" required />

          <label for="location">Localização</label>
          <input id="location" v-model="form.location" type="text" required />

          <label for="observations">Observações</label>
          <textarea id="observations" v-model="form.observations"></textarea>

          <label for="eventType">Tipo de Evento</label>
          <select id="eventType" v-model.number="form.event_type" @change="handleEventTypeChange" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in eventTypes" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>

          <!-- Campos Dinâmicos -->
          <div v-if="selectedEventType === 'movement'" class="dynamic-form">
            <h4>Movimento</h4>
            <label for="origin">Propriedade Origem</label>
            <input id="origin" v-model.number="movement.origin_property" type="number" required />
            <label for="destination">Propriedade Destino</label>
            <input id="destination" v-model.number="movement.destination_property" type="number" required />
            <label for="reason">Razão</label>
            <input id="reason" v-model="movement.reason" type="text" required />
          </div>

          <div v-else-if="selectedEventType === 'weighing'" class="dynamic-form">
            <h4>Pesagem</h4>
            <label for="weight">Peso (kg)</label>
            <input id="weight" v-model.number="weighing.weight" type="number" step="0.01" required />
          </div>

          <div v-else-if="selectedEventType === 'vacine'" class="dynamic-form">
            <h4>Vacina</h4>
            <label for="vacine-name">Nome</label>
            <input id="vacine-name" v-model="vaccine.name" type="text" required />
            <label for="vacine-manufacturer">Fabricante</label>
            <input id="vacine-manufacturer" v-model="vaccine.manufacturer" type="text" required />
            <label for="vacine-batch">Lote</label>
            <input id="vacine-batch" v-model="vaccine.batch" type="text" required />
            <label for="vacine-validity">Validade</label>
            <input id="vacine-validity" v-model="vaccine.validity" type="date" required />
            <label for="vacine-dose">Dose</label>
            <input id="vacine-dose" v-model="vaccine.dose" type="text" required />
            <label for="vacine-next">Próxima Dose</label>
            <input id="vacine-next" v-model="vaccine.next_dose_date" type="date" />
          </div>

          <div v-else-if="selectedEventType === 'medicine'" class="dynamic-form">
            <h4>Medicação</h4>
            <label for="med-name">Nome</label>
            <input id="med-name" v-model="medicine.name" type="text" required />
            <label for="med-manufacturer">Fabricante</label>
            <input id="med-manufacturer" v-model="medicine.manufacturer" type="text" required />
            <label for="med-batch">Lote</label>
            <input id="med-batch" v-model="medicine.batch" type="text" required />
            <label for="med-validity">Validade</label>
            <input id="med-validity" v-model="medicine.validity" type="date" required />
            <label for="med-dose">Dose</label>
            <input id="med-dose" v-model="medicine.dose" type="text" required />
            <label for="med-next">Próxima Dose</label>
            <input id="med-next" v-model="medicine.next_dose_date" type="date" />
            <label for="med-reason">Razão</label>
            <input id="med-reason" v-model="medicine.reason" type="text" required />
            <label for="med-withdrawal">Tempo de Retirada</label>
            <input id="med-withdrawal" v-model="medicine.withdrawal_time" type="text" />
          </div>

          <div v-else-if="selectedEventType === 'reproduction'" class="dynamic-form">
            <h4>Reprodução</h4>
            <label for="rep-type">Tipo</label>
            <input id="rep-type" v-model="reproduction.reproduction_type" type="text" required />
            <label for="rep-male">ID Macho</label>
            <input id="rep-male" v-model.number="reproduction.male_id" type="number" required />
            <label for="rep-female">ID Fêmea</label>
            <input id="rep-female" v-model.number="reproduction.female_id" type="number" required />
            <label for="rep-date">Data</label>
            <input id="rep-date" v-model="reproduction.date" type="date" required />
            <label for="rep-result">Resultado</label>
            <input id="rep-result" v-model="reproduction.result" type="text" />
          </div>

          <div v-else-if="selectedEventType === 'slaughter'" class="dynamic-form">
            <h4>Abate</h4>
            <label for="sl-date">Data</label>
            <input id="sl-date" v-model="slaughter.date" type="date" required />
            <label for="sl-location">Local</label>
            <input id="sl-location" v-model="slaughter.location" type="text" required />
            <label for="sl-weight">Peso Final (kg)</label>
            <input id="sl-weight" v-model.number="slaughter.final_weight" type="number" step="0.01" required />
            <label for="sl-inspection">Inspeção</label>
            <input id="sl-inspection" v-model="slaughter.inspection_result" type="text" required />
          </div>

          <div v-else-if="selectedEventType === 'occurrence'" class="dynamic-form">
            <h4>Ocorrência Especial</h4>
            <label for="occ-type">Tipo</label>
            <input id="occ-type" v-model="occurrence.occurrence_type" type="text" required />
            <label for="occ-desc">Descrição</label>
            <textarea id="occ-desc" v-model="occurrence.description"></textarea>
            <label for="occ-date">Data</label>
            <input id="occ-date" v-model="occurrence.date" type="date" required />
            <label for="occ-actions">Ações Tomadas</label>
            <textarea id="occ-actions" v-model="occurrence.actions_taken"></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="button-primary">
              {{ editing ? 'Atualizar Evento' : 'Cadastrar Evento' }}
            </button>
            <button type="button" class="button-secondary" @click="closeModal">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import {
  registerEvent,
  updateEvent,
  registerMovement,
  registerWeighing,
  registerVacine,
  registerMedicine,
  registerReproduction,
  registerSlaughter,
  registerSpecialOccurrence
} from '@/services/eventService';
import { getEventTypes } from '@/services/lookupService';

export default {
  name: 'EventContent',
  data() {
    return {
      showModal: false,
      editing: false,
      editingId: null,
      form: {
        animal: '',
        date: '',
        location: '',
        observations: '',
        event_type: ''
      },
      eventTypes: [],
      movement: { origin_property: '', destination_property: '', reason: '' },
      weighing: { weight: '' },
      vaccine: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '' },
      medicine: { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: '' },
      reproduction: { reproduction_type: '', male_id: '', female_id: '', date: '', result: '' },
      slaughter: { date: '', location: '', final_weight: '', inspection_result: '' },
      occurrence: { occurrence_type: '', description: '', date: '', actions_taken: '' }
    };
  },
  computed: {
    selectedEventType() {
      const map = {
        1: 'movement',
        2: 'weighing',
        3: 'vacine',
        4: 'medicine',
        5: 'reproduction',
        6: 'slaughter',
        7: 'occurrence'
      };
      return map[this.form.event_type] || '';
    }
  },
  methods: {
    openModal() {
      this.resetAll();
      this.editing = false;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async loadEventTypes() {
      try {
        this.eventTypes = await getEventTypes();
      } catch (e) {
        console.error('Erro ao carregar tipos de evento:', e);
      }
    },
    handleEventTypeChange() {
      // limpa dados do subform conforme tipo
      const type = this.selectedEventType;
      if (type === 'movement') this.movement = { origin_property: '', destination_property: '', reason: '' };
      else if (type === 'weighing') this.weighing = { weight: '' };
      else if (type === 'vacine') this.vaccine = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '' };
      else if (type === 'medicine') this.medicine = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: '' };
      else if (type === 'reproduction') this.reproduction = { reproduction_type: '', male_id: '', female_id: '', date: '', result: '' };
      else if (type === 'slaughter') this.slaughter = { date: '', location: '', final_weight: '', inspection_result: '' };
      else if (type === 'occurrence') this.occurrence = { occurrence_type: '', description: '', date: '', actions_taken: '' };
    },
    async handleSubmit() {
      try {
        const res = this.editing
          ? await updateEvent(this.editingId, this.form)
          : await registerEvent(this.form);
        const eid = res.id;
        // dispara subevento
        const type = this.selectedEventType;
        if (type === 'movement') await registerMovement({ event: eid, ...this.movement });
        else if (type === 'weighing') await registerWeighing({ event: eid, ...this.weighing });
        else if (type === 'vacine') await registerVacine({ event: eid, ...this.vaccine });
        else if (type === 'medicine') await registerMedicine({ event: eid, ...this.medicine });
        else if (type === 'reproduction') await registerReproduction({ event: eid, ...this.reproduction });
        else if (type === 'slaughter') await registerSlaughter({ event: eid, ...this.slaughter });
        else if (type === 'occurrence') await registerSpecialOccurrence({ event: eid, ...this.occurrence });

        alert('Evento salvo com sucesso.');
        this.closeModal();
      } catch (e) {
        console.error('Erro ao salvar evento:', e);
        alert('Erro ao salvar evento.');
      }
    },
    resetAll() {
      this.form = { animal: '', date: '', location: '', observations: '', event_type: '' };
      this.movement = { origin_property: '', destination_property: '', reason: '' };
      this.weighing = { weight: '' };
      this.vaccine = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '' };
      this.medicine = { name: '', manufacturer: '', batch: '', validity: '', dose: '', next_dose_date: '', reason: '', withdrawal_time: '' };
      this.reproduction = { reproduction_type: '', male_id: '', female_id: '', date: '', result: '' };
      this.slaughter = { date: '', location: '', final_weight: '', inspection_result: '' };
      this.occurrence = { occurrence_type: '', description: '', date: '', actions_taken: '' };
    }
  },
  mounted() {
    this.loadEventTypes();
  }
};
</script>

<style scoped>
.content-panel {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: var(--sp-xl);
}
.panel-title {
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-xs);
}
.panel-description {
  text-align: center;
  color: var(--color-dark-gray);
  margin-bottom: var(--sp-md);
}
.add-button-wrapper {
  text-align: right;
  margin-bottom: var(--sp-md);
}
/* Modal */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%; max-width: 600px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  /*  ← Novas linhas: */
  max-height: 80vh;    /* limita altura total do painel */
  overflow-y: auto;    /* habilita scroll quando ultrapassar */
}
.modal-title {
  text-align: center;
  font-family: var(--font-heading);
  margin-bottom: var(--sp-md);
}
.form-group {
  display: flex; flex-direction: column; gap: var(--sp-md);
}
.form-group label {
  font-weight: 500;
}
.form-group input,
.form-group select,
.form-group textarea {
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-base);
}
.dynamic-form {
  margin-top: var(--sp-md);
  padding: var(--sp-md);
  background: var(--color-light-gray);
  border-radius: var(--sp-sm);
  border: 1px solid var(--color-border);
}
/* Empilha label+campo em .dynamic-form */
.dynamic-form label {
  display: block;
  margin-bottom: var(--sp-xs);
  font-weight: 500;
  color: var(--color-dark-gray);
}
.dynamic-form input,
.dynamic-form select,
.dynamic-form textarea {
  display: block;
  width: 100%;
  padding: var(--sp-sm);
  margin-bottom: var(--sp-md);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-base);
  box-sizing: border-box;
}
/* Título do subform */
.dynamic-form h4 {
  margin-bottom: var(--sp-md);
  font-family: var(--font-heading);
  color: var(--color-primary);
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-sm);
  margin-top: var(--sp-md);
}
/* Botões */
.button-primary {
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  padding: var(--sp-sm) var(--sp-lg);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
.button-secondary {
  background-color: var(--color-bg);
  color: #e74c3c;
  border: 2px solid #e74c3c;
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-secondary:hover,
.button-secondary:focus {
  background-color: #e74c3c;
  color: var(--color-bg);
  outline: none;
}
</style>
