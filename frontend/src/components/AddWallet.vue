<template>
    <div>
      <h2>Adicionar Carteira</h2>
      <form @submit.prevent="handleAddWallet">
        <label for="registrar">Endereço da Carteira:</label>
        <input type="text" v-model="registrar" id="registrar" placeholder="0x..." />
        <button type="submit">Adicionar</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import { addRegistrar } from '@/services/contractService';
  export default {
    name: 'AddWallet',
    data() {
      return {
        registrar: '',
        message: ''
      };
    },
    methods: {
      async handleAddWallet() {
        try {
          const result = await addRegistrar(this.registrar);
          this.message = `Registrador adicionado com sucesso: ${result.tx_hash}`;
        } catch (error) {
          this.message = `Erro: ${error.error || error}`;
        }
      }
    }
  };
  </script>
  