<template>
  <div class="cadastro-form auth-form">
    <h2>Cadastro</h2>
    <form @submit.prevent="handleRegister">
      <!-- Usuário -->
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

      <!-- Nome -->
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

      <!-- Sobrenome -->
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

      <!-- E-mail -->
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

      <!-- Senha -->
      <div class="form-group password-group">
        <label for="password">Senha</label>
        <div class="password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="form.password"
            placeholder="Crie uma senha"
            required
          />
          <button
            type="button"
            class="toggle-password"
            @click="showPassword = !showPassword"
            :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
          >
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
      </div>

      <!-- Repita a senha -->
      <div class="form-group password-group">
        <label for="confirm_password">Repita a senha</label>
        <div class="password-wrapper">
          <input
            :type="showConfirm ? 'text' : 'password'"
            id="confirm_password"
            v-model="form.confirm_password"
            placeholder="Repita sua senha"
            required
          />
          <button
            type="button"
            class="toggle-password"
            @click="showConfirm = !showConfirm"
            :aria-label="showConfirm ? 'Ocultar senha' : 'Mostrar senha'"
          >
            {{ showConfirm ? '🙈' : '👁️' }}
          </button>
        </div>
      </div>

      <!-- Telefone -->
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

      <!-- Botão -->
      <button type="submit" class="button-primary">Cadastrar</button>
    </form>

    <!-- Mensagens -->
    <div v-if="success" class="success-message">
      Cadastro realizado com sucesso! Você será redirecionado em {{ countdown }}s...
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- Link para login -->
    <p class="switch-text">
      Já tem conta? <a @click.prevent="$emit('navigate','login')" href="#">Faça login</a>
    </p>
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
        confirm_password: '',
        phone: ''
      },
      showPassword: false,
      showConfirm: false,
      error: null,
      success: false,
      countdown: 3,
      timer: null
    };
  },
  methods: {
    async handleRegister() {
      this.error = null;

      if (this.form.password !== this.form.confirm_password) {
        this.error = 'As senhas não coincidem.';
        return;
      }

      const { confirm_password, ...payload } = this.form;

      try {
        await registerUser(payload);
        this.success = true;
        this.countdown = 3;
        this.timer = setInterval(() => {
          this.countdown--;
          if (this.countdown === 0) {
            clearInterval(this.timer);
            this.$emit('navigate', 'login');
          }
        }, 1000);
      } catch (err) {
        this.error = err.message || 'Erro no cadastro';
      }
    }
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer);
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

/* wrapper e botão de toggle */
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

/* botão primário */
.button-primary {
  width: 100%;
  padding: var(--sp-md);
  background-color: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: var(--sp-sm);
  font-size: var(--font-size-large);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  margin-top: var(--sp-md);
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-primary-dark);
  outline: none;
}

/* mensagens */
.success-message {
  margin-top: var(--sp-md);
  padding: var(--sp-sm);
  background: var(--color-secondary-light);
  color: var(--color-white);
  text-align: center;
  border-radius: var(--sp-sm);
  font-weight: 500;
}
.error-message {
  margin-top: var(--sp-sm);
  color: var(--color-secondary);
  text-align: center;
  font-size: var(--font-size-small);
}

.switch-text {
  text-align: center;
  margin-top: var(--sp-lg);
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
</style>
