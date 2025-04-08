<!-- src/components/BlockchainContent.vue -->
<template>
    <div class="blockchain-content">
      <h2>Registros na Blockchain</h2>
      
      <!-- Formulário para cadastrar novo registro -->
      <div class="form-container">
        <h3>Cadastrar Novo Registro</h3>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>Animal ID:</label>
            <input v-model.number="form.animal" type="number" required />
          </div>
          <div class="form-group">
            <label>Evento ID:</label>
            <input v-model.number="form.event" type="number" required />
          </div>
          <div class="form-group">
            <label>Transaction Hash:</label>
            <input v-model="form.transaction_hash" type="text" required />
          </div>
          <div class="form-group">
            <label>Status:</label>
            <input v-model="form.status" type="text" required placeholder="Ex: 1 (ativo)" />
          </div>
          <button type="submit">Cadastrar</button>
        </form>
      </div>
  
      <!-- Lista de registros da blockchain -->
      <div class="list-container">
        <h3>Registros Existentes</h3>
        <ul>
          <li v-for="record in blockchains" :key="record.id">
            <strong>ID:</strong> {{ record.id }} |
            <strong>Animal:</strong> {{ record.animal }} |
            <strong>Evento:</strong> {{ record.event }} |
            <strong>Tx Hash:</strong> {{ record.transaction_hash }} |
            <strong>Status:</strong> {{ record.status }}
            <!-- Botões para atualizar/deletar (funções adicionais podem ser implementadas) -->
            <button @click="handleDelete(record.id)">Deletar</button>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { 
    registerBlockchain, 
    getBlockchains, 
    deleteBlockchain 
  } from '@/services/blockchainService';
  
  export default {
    name: 'BlockchainContent',
    setup() {
      const form = ref({
        animal: '',
        event: '',
        transaction_hash: '',
        status: ''
      });
  
      const blockchains = ref([]);
  
      // Função para carregar os registros existentes
      const loadBlockchains = async () => {
        try {
          blockchains.value = await getBlockchains();
        } catch (error) {
          console.error('Erro ao carregar registros de blockchain:', error);
        }
      };
  
      // Função para cadastrar novo registro
      const handleRegister = async () => {
        try {
          const result = await registerBlockchain(form.value);
          alert('Registro cadastrado com sucesso!');
          // Limpa o formulário
          form.value = { animal: '', event: '', transaction_hash: '', status: '' };
          // Recarrega a lista
          loadBlockchains();
        } catch (error) {
          console.error('Erro ao cadastrar registro:', error);
          alert('Erro ao cadastrar registro.');
        }
      };
  
      // Função para deletar um registro
      const handleDelete = async (id) => {
        if (confirm('Deseja realmente deletar este registro?')) {
          try {
            await deleteBlockchain(id);
            alert('Registro deletado com sucesso!');
            loadBlockchains();
          } catch (error) {
            console.error('Erro ao deletar registro:', error);
            alert('Erro ao deletar registro.');
          }
        }
      };
  
      onMounted(() => {
        loadBlockchains();
      });
  
      return {
        form,
        blockchains,
        handleRegister,
        handleDelete
      };
    }
  };
  </script>
  
  <style scoped>
  .blockchain-content {
    padding: 1rem;
  }
  
  .form-container,
  .list-container {
    margin-bottom: 2rem;
    padding: 1rem;
    background-color: var(--color-light-gray);
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.3rem;
  }
  
  input {
    width: 100%;
    padding: 0.4rem;
    box-sizing: border-box;
  }
  
  button {
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
  </style>
  