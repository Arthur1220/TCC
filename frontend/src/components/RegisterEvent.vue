<template>
  <div>
    <h2>Registrar Evento</h2>
    <form @submit.prevent="handleRegisterEvent">
      <label for="event_id">ID do Evento:</label>
      <input type="number" v-model.number="event_id" id="event_id" />

      <label for="animal_id">ID do Animal:</label>
      <input type="number" v-model.number="animal_id" id="animal_id" />

      <label for="event_type">Tipo do Evento (número):</label>
      <input type="number" v-model.number="event_type" id="event_type" />

      <label for="data_hash">Hash dos Dados:</label>
      <input type="text" v-model="data_hash" id="data_hash" />

      <label for="user_hash">Hash do Usuário:</label>
      <input type="text" v-model="user_hash" id="user_hash" />

      <button type="submit">Registrar Evento</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import { registerContractEvent } from '@/services/contractService';
export default {
  name: 'RegisterEvent',
  data() {
    return {
      event_id: null,
      animal_id: null,
      event_type: null,
      data_hash: '',
      user_hash: '',
      message: ''
    };
  },
  methods: {
    async handleRegisterEvent() {
      try {
        const payload = {
          event_id: this.event_id,
          animal_id: this.animal_id,
          event_type: this.event_type,
          data_hash: this.data_hash,
          user_hash: this.user_hash
        };
        const result = await registerContractEvent(payload);
        this.message = `Evento registrado com sucesso: ${result.tx_hash}`;
      } catch (error) {
        this.message = `Erro: ${error.error || error}`;
      }
    }
  }
};
</script>
