<template>
  <div class="login-form auth-form">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Usuário ou E-mail</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          placeholder="Digite seu usuário ou e-mail"
          required
        />
      </div>
      <div class="form-group password-group">
        <label for="password">Senha</label>
        <div class="password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="form.password"
            placeholder="Digite sua senha"
            required
          />
          <button
            type="button"
            class="toggle-password"
            @click="togglePassword"
            :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
          >
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
      </div>
      <button type="submit" class="button-primary">Entrar</button>
    </form>
    <p class="switch-text">
      Não tem conta? 
      <a @click.prevent="$emit('navigate','register')" href="#">Cadastre-se</a>
    </p>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import { login } from '@/services/authService';
export default {
  name: 'Login',
  data() {
    return {
      form: { username: '', password: '' },
      error: null,
      showPassword: false
    };
  },
  methods: {
    async handleLogin() {
      this.error = null;
      try {
        await login(this.form);
        this.$router.push({ name: 'MVPContract' });
      } catch (err) {
        this.error = err.error || 'Usuário ou senha inválidos';
      }
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
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
.login-form h2 {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: var(--color-primary);
  text-align: center;
  margin-bottom: var(--sp-md);
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
.password-wrapper {
  position: relative;
}
.password-wrapper input {
  padding-right: calc(var(--sp-lg) + var(--sp-sm));
}
.toggle-password {
  position: absolute;
  top: 50%;
  right: var(--sp-sm);
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: var(--font-size-large);
  cursor: pointer;
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