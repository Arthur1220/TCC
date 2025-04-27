<template>
  <div class="cadastro-form auth-form">
    <h2>Cadastro</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Usuário</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          placeholder="Escolha um nome de usuário"
          required
        />
      </div>
      <div class="form-group">
        <label for="first_name">Nome</label>
        <input
          type="text"
          id="first_name"
          v-model="form.first_name"
          placeholder="Digite seu nome"
          required
        />
      </div>
      <div class="form-group">
        <label for="last_name">Sobrenome</label>
        <input
          type="text"
          id="last_name"
          v-model="form.last_name"
          placeholder="Digite seu sobrenome"
          required
        />
      </div>
      <div class="form-group">
        <label for="email">E-mail</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          placeholder="Digite seu e-mail"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Senha</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          placeholder="Crie uma senha"
          required
        />
      </div>
      <div class="form-group">
        <label for="phone">Telefone</label>
        <input
          type="text"
          id="phone"
          v-model="form.phone"
          placeholder="(xx) xxxx-xxxx"
          required
        />
      </div>
      <button type="submit" class="button button-primary">Cadastrar</button>
    </form>
    <p class="switch-text">
      Já tem conta? <a @click.prevent="$emit('navigate','login')" href="#">Faça login</a>
    </p>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import { registerUser } from '@/services/userService';
export default {
  name: 'CadastroContent',
  data() {
    return {
      form: {
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        phone: ''
      },
      error: null
    };
  },
  methods: {
    async handleRegister() {
      this.error = null;
      try {
        await registerUser(this.form);
        this.$emit('navigate','login');
      } catch (err) {
        this.error = err.message || 'Erro no cadastro';
      }
    }
  }
};
</script>

<style scoped>
.auth-form {
  width: 100%;
  max-width: 400px;
  padding: var(--sp-lg);
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  margin: var(--sp-xl) auto;
}
.cadastro-form h2 {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: var(--color-primary);
  text-align: center;
  margin-bottom: var(--sp-lg);
}
.form-group {
  margin-bottom: var(--sp-md);
}
.form-group label {
  display: block;
  margin-bottom: var(--sp-sm);
  color: var(--color-dark-gray);
  font-size: var(--font-size-base);
}
.form-group input {
  width: 100%;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-family: var(--font-body);
  font-size: var(--font-size-base);
}
.button-primary {
  width: 100%;
  padding: var(--sp-md);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-large);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  margin-top: var(--sp-md);
}
.button-primary:hover, .button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
.switch-text {
  text-align: center;
  margin-top: var(--sp-md);
  font-size: var(--font-size-small);
}
.switch-text a {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 500;
}
.switch-text a:hover {
  text-decoration: underline;
}
.error-message {
  margin-top: var(--sp-sm);
  color: var(--color-secondary);
  text-align: center;
  font-size: var(--font-size-small);
}
</style>