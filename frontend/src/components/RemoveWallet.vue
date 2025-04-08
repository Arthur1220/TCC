<template>
    <div>
      <h2>Remover Carteira</h2>
      <form @submit.prevent="handleRemoveWallet">
        <label for="registrar">Endereço da Carteira:</label>
        <input type="text" v-model="registrar" id="registrar" placeholder="0x..." />
        <button type="submit">Remover</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import { removeRegistrar } from '@/services/contractService';
  export default {
    name: 'RemoveWallet',
    data() {
      return {
        registrar: '',
        message: ''
      };
    },
    methods: {
      async handleRemoveWallet() {
        try {
          const result = await removeRegistrar(this.registrar);
          this.message = `Registrador removido com sucesso: ${result.tx_hash}`;
        } catch (error) {
          this.message = `Erro: ${error.error || error}`;
        }
      }
    }
  };
  </script>
  