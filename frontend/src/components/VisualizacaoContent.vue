<template>
    <div class="visualizacao-content">
      <h2>Visualização de Eventos</h2>
      
      <div v-if="loading">
        <p>Carregando eventos...</p>
      </div>
      
      <div v-else>
        <div v-if="events.length">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>ID do Animal</th>
                <th>Tipo do Evento</th>
                <th>Data</th>
                <th>Local</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="event in events" :key="event.id">
                <td>{{ event.id }}</td>
                <td>{{ event.animal }}</td>
                <td>{{ getEventTypeName(event.event_type) }}</td>
                <td>{{ event.date }}</td>
                <td>{{ event.location }}</td>
                <td>
                  <button @click="loadEventDetails(event)">Detalhes</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <p>Nenhum evento encontrado.</p>
        </div>
      </div>
      
      <div v-if="selectedEvent">
        <h3>Detalhes do Evento</h3>
        <pre>{{ selectedEvent }}</pre>
        <!-- Aqui você pode também exibir informações adicionais a partir dos registros específicos,
             de acordo com o tipo do evento (por exemplo, se o evento for de Vacina, chamar o serviço de Vacina). -->
        <button @click="closeDetails">Fechar Detalhes</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { getEvents } from '@/services/eventService'; // Implemente essa função para retornar a lista de eventos
  import { getEventTypes } from '@/services/lookupService'; // Função para obter os tipos de evento
  
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
          events.value = await getEvents(); // Ajuste conforme sua implementação do service
        } catch (error) {
          console.error('Erro ao carregar eventos:', error);
        } finally {
          loading.value = false;
        }
      };
  
      const loadEventTypes = async () => {
        try {
          eventTypes.value = await getEventTypes();
        } catch (error) {
          console.error('Erro ao carregar tipos de evento:', error);
        }
      };
  
      const getEventTypeName = (eventTypeId) => {
        const found = eventTypes.value.find(type => type.id === eventTypeId);
        return found ? found.name : 'Desconhecido';
      };
  
      const loadEventDetails = (event) => {
        // Aqui você pode chamar um serviço para buscar os detalhes específicos do evento de acordo com o seu tipo.
        // Por exemplo, se for Vacina, chamar um endpoint: getVacinaDetails(event.id)
        // Neste exemplo, apenas armazenamos o evento selecionado:
        selectedEvent.value = event;
      };
  
      const closeDetails = () => {
        selectedEvent.value = null;
      };
  
      onMounted(() => {
        loadEvents();
        loadEventTypes();
      });
  
      return {
        events,
        eventTypes,
        selectedEvent,
        loading,
        getEventTypeName,
        loadEventDetails,
        closeDetails
      };
    }
  };
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
  }
  table th,
  table td {
    padding: 0.5rem;
    border: 1px solid #ccc;
    text-align: left;
  }
  button {
    padding: 0.3rem 0.6rem;
    cursor: pointer;
  }
  </style>
  