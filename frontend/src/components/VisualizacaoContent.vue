<template>
  <div class="visualizacao-content">
    <h2 class="section-subtitle">Visualização de Eventos</h2>

    <div v-if="loading" class="loading">Carregando eventos...</div>

    <div v-else>
      <table class="events-table" v-if="events.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>ID Animal</th>
            <th>Tipo</th>
            <th>Data</th>
            <th>Local</th>
            <th>Ação</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="evt in events" :key="evt.id">
            <td>{{ evt.id }}</td>
            <td>{{ evt.animal }}</td>
            <td>{{ getEventTypeName(evt.event_type) }}</td>
            <td>{{ evt.date }}</td>
            <td>{{ evt.location }}</td>
            <td>
              <button class="button-secondary" @click="loadEventDetails(evt)">Detalhes</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!events.length" class="empty-state">
        Nenhum evento encontrado.
      </div>
    </div>

    <!-- Modal de Detalhes -->
    <div v-if="selectedEvent" class="modal-overlay" @click.self="closeDetails">
      <div class="modal-content">
        <h3 class="modal-title">Detalhes do Evento</h3>
        <pre>{{ selectedEvent }}</pre>
        <button class="button-primary" @click="closeDetails">Fechar</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getEvents } from '@/services/eventService';
import { getEventTypes } from '@/services/lookupService';

export default {
  name: 'VisualizacaoContent',
  setup() {
    const events = ref([]);
    const eventTypes = ref([]);
    const selectedEvent = ref(null);
    const loading = ref(false);

    const loadEvents = async () => {
      loading.value = true;
      try {
        events.value = await getEvents();
      } catch (e) {
        console.error(e);
      } finally {
        loading.value = false;
      }
    };
    const loadTypes = async () => {
      try {
        eventTypes.value = await getEventTypes();
      } catch (e) {
        console.error(e);
      }
    };
    const getEventTypeName = id => {
      const t = eventTypes.value.find(x => x.id === id);
      return t ? t.name : '—';
    };
    const loadEventDetails = evt => selectedEvent.value = evt;
    const closeDetails = () => selectedEvent.value = null;

    onMounted(() => {
      loadEvents();
      loadTypes();
    });

    return { events, loading, selectedEvent, getEventTypeName, loadEventDetails, closeDetails };
  }
};
</script>

<style scoped>
.section-subtitle {
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.events-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--sp-lg);
}
.events-table th,
.events-table td {
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  text-align: left;
}
.button-secondary,
.button-primary {
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.2s;
  border: none;
}
.button-secondary {
  background: var(--color-muted);
  color: var(--color-text);
}
.button-secondary:hover {
  background: var(--color-accent);
  color: var(--color-bg);
}
.button-primary {
  background: var(--color-primary);
  color: white;
}
.button-primary:hover {
  background: var(--color-primary-dark);
}
.empty-state,
.loading {
  text-align: center;
  color: var(--color-dark-gray);
  margin-top: var(--sp-lg);
}
/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal-content {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
.modal-title {
  margin-bottom: var(--sp-md);
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
}
</style>
