<template>
    <div>
      <h2>Visualizar Evento por Animal</h2>
      <form @submit.prevent="handleViewEvent">
        <label for="animal_id">ID do Animal:</label>
        <input type="number" v-model.number="animal_id" id="animal_id" />
  
        <label for="index">Índice do Evento (opcional):</label>
        <input type="number" v-model.number="index" id="index" />
  
        <button type="submit">Buscar Evento</button>
      </form>
      <div v-if="eventData">
        <h3>Evento:</h3>
        <pre>{{ eventData }}</pre>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import { getEventByAnimal } from '@/services/contractService';
  export default {
    name: 'ViewEventByAnimal',
    data() {
      return {
        animal_id: null,
        index: 0,
        eventData: null,
        message: ''
      };
    },
    methods: {
      async handleViewEvent() {
        try {
          const result = await getEventByAnimal(this.animal_id, this.index);
          this.eventData = result;
          this.message = '';
        } catch (error) {
          this.message = `Erro: ${error.error || error}`;
        }
      }
    }
  };
  </script>
  