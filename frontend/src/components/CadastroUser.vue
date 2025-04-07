<template>
    <div class="cadastro-form">
      <h2>Cadastro</h2>
      <form @submit.prevent="handleRegister">
        <div>
          <label for="username">Usuário:</label>
          <input type="text" id="username" v-model="form.username" required />
        </div>
        <div>
          <label for="first_name">Nome:</label>
          <input type="text" id="first_name" v-model="form.first_name" required />
        </div>
        <div>
          <label for="last_name">Sobrenome:</label>
          <input type="text" id="last_name" v-model="form.last_name" required />
        </div>
        <div>
          <label for="email">E-mail:</label>
          <input type="email" id="email" v-model="form.email" required />
        </div>
        <div>
          <label for="password">Senha:</label>
          <input type="password" id="password" v-model="form.password" required />
        </div>
        <div>
          <label for="phone">Telefone:</label>
          <input type="text" id="phone" v-model="form.phone" required />
        </div>
        <button type="submit">Cadastrar</button>
      </form>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import { registerUser } from '@/services/userService';
  
  export default {
    name: "CadastroContent",
    data() {
      return {
        form: {
          username: "",
          first_name: "",
          last_name: "",
          email: "",
          password: "",
          phone: ""
        },
        error: null
      };
    },
    methods: {
      async handleRegister() {
        try {
          await registerUser(this.form);
          // Após cadastro, alterna para o componente de Login
          this.$emit("switchComponent", "Login");
        } catch (err) {
          this.error = err.message || "Erro no cadastro";
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .cadastro-form {
    max-width: 400px;
    margin: 0 auto;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  