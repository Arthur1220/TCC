<template>
    <div>
      <h2>Visualizar Número de Eventos</h2>
      <form @submit.prevent="handleViewCount">
        <label for="animal_id">ID do Animal:</label>
        <input type="number" v-model.number="animal_id" id="animal_id" />
        <button type="submit">Buscar Número de Eventos</button>
      </form>
      <div v-if="count !== null">
        <h3>Número de Eventos: {{ count }}</h3>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import { getNumberOfEvents } from '@/services/contractService';
  export default {
    name: 'ViewEventCount',
    data() {
      return {
        animal_id: null,
        count: null,
        message: ''
      };
    },
    methods: {
      async handleViewCount() {
        try {
          const result = await getNumberOfEvents(this.animal_id);
          this.count = result.count;
          this.message = '';
        } catch (error) {
          this.message = `Erro: ${error.error || error}`;
        }
      }
    }
  };
  </script>
  