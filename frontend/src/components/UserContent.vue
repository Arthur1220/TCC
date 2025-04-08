<!-- src/components/UsuarioContent.vue -->
<template>
    <div class="usuario-content">
      <h2>Perfil do Usuário</h2>
      <!-- Exibe os dados do usuário -->
      <div v-if="user">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Nome:</strong> {{ user.first_name }} {{ user.last_name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Telefone:</strong> {{ user.phone }}</p>
        <p><strong>Hash de Usuario:</strong> {{ user.user_hash }}</p>
        <!-- Botões para editar e deletar -->
        <button @click="toggleEdit">Editar Perfil</button>
        <button @click="deleteAccount" class="delete-btn">Deletar Conta</button>
      </div>
      <div v-else>
        <p>Carregando perfil...</p>
      </div>
  
      <!-- Formulário de edição -->
      <div v-if="editing">
        <h3>Editar Perfil</h3>
        <form @submit.prevent="saveChanges">
          <label>
            Primeiro Nome:
            <input type="text" v-model="editData.first_name" />
          </label>
          <label>
            Último Nome:
            <input type="text" v-model="editData.last_name" />
          </label>
          <label>
            Email:
            <input type="email" v-model="editData.email" />
          </label>
          <label>
            Telefone:
            <input type="text" v-model="editData.phone" />
          </label>
          <button type="submit">Salvar</button>
          <button type="button" @click="cancelEdit">Cancelar</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { getUserProfile, updateUserProfile, deleteUserAccount } from '@/services/userService';
  
  export default {
    name: 'UsuarioContent',
    data() {
      return {
        user: null,
        editing: false,
        editData: {},
      };
    },
    created() {
      this.fetchUserProfile();
    },
    methods: {
      async fetchUserProfile() {
        try {
          const data = await getUserProfile();
          this.user = data;
        } catch (error) {
          console.error('Erro ao carregar perfil:', error);
          // Dependendo do erro, você pode redirecionar para a página de login
        }
      },
      toggleEdit() {
        this.editing = !this.editing;
        if (this.editing && this.user) {
          // Inicia o formulário com os valores atuais
          this.editData = { ...this.user };
        }
      },
      async saveChanges() {
        try {
          const updated = await updateUserProfile(this.editData);
          this.user = updated;
          this.editing = false;
          alert('Perfil atualizado com sucesso!');
        } catch (error) {
          console.error('Erro ao atualizar perfil:', error);
          alert('Erro ao atualizar perfil.');
        }
      },
      async deleteAccount() {
        if (confirm('Tem certeza que deseja deletar sua conta? Esta ação é irreversível.')) {
          try {
            await deleteUserAccount();
            alert('Conta deletada com sucesso.');
            // Redirecione o usuário para a página de login ou home
            this.$router.push({ name: 'Login' });
          } catch (error) {
            console.error('Erro ao deletar conta:', error);
            alert('Erro ao deletar conta.');
          }
        }
      },
      cancelEdit() {
        this.editing = false;
        this.editData = {};
      }
    }
  };
  </script>
  
  <style scoped>
  .usuario-content {
    padding: 1rem;
  }
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  input[type="text"],
  input[type="email"] {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
  }
  button {
    margin-right: 0.5rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
  .delete-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
  }
  </style>
  