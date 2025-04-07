<template>
  <div class="login-form">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Usuário ou E-mail:</label>
        <input type="text" id="username" v-model="form.username" placeholder="Digite seu usuário ou e-mail" required />
      </div>
      <div>
        <label for="password">Senha:</label>
        <input type="password" id="password" v-model="form.password" placeholder="Digite sua senha" required />
      </div>
      <button type="submit">Entrar</button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { login } from '@/services/authService';

export default {
  name: "Login",
  data() {
    return {
      form: {
        username: "",
        password: ""
      },
      error: null
    };
  },
  methods: {
    async handleLogin() {
      try {
        // O payload será um objeto simples: { username: "teste", password: "123" }
        const response = await login(this.form);
        // Após o login bem-sucedido, redirecione para a rota desejada
        this.$router.push({ name: "MVP" });
      } catch (err) {
        this.error = err.error || "Erro no login";
        console.error("Erro no login:", err);
      }
    }
  }
};
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
