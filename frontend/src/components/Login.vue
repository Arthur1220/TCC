<template>
  <div class="auth-form-container">
    <h2 class="auth-title">Acesse sua Conta</h2>
    <p class="auth-subtitle">Bem-vindo de volta! Por favor, insira os seus dados.</p>
    
    <form @submit.prevent="handleLogin" class="form">
      <div class="form-group">
        <label for="username" class="form-label">Usuário ou E-mail</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          placeholder="ex: joao.silva"
          class="input"
          required
          :disabled="isSubmitting"
        />
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Senha</label>
        <div class="password-input-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="form.password"
            placeholder="••••••••"
            class="input"
            required
            :disabled="isSubmitting"
          />
          <button
            type="button"
            class="password-toggle-button"
            @click="togglePassword"
            :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
            :disabled="isSubmitting"
          >
          <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.44-4.75C21.27 7.61 17 4.5 12 4.5c-1.6 0-3.14.35-4.54.98l2.28 2.28C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
            </button>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>

      <button type="submit" class="button button-primary button-block" :disabled="isSubmitting">
        <svg v-if="isSubmitting" class="button-spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
        <span v-else>Entrar</span>
      </button>
    </form>

    <p class="switch-text">
      Não tem uma conta?
      <a @click.prevent="$emit('navigate','register')" href="#" class="link">Cadastre-se agora</a>
    </p>

    <Teleport to="body">
      <NotificationModal
        :show="notification.show"
        :title="notification.title"
        :message="notification.message"
        :type="notification.type"
        @close="handleNotificationClose"
      />
    </Teleport>
  </div>
</template>

<script>
import { login } from '@/services/authService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'Login',
  components: {
    NotificationModal
  },
  emits: ['navigate', 'login-redirect'],
  data() {
    return {
      form: { username: '', password: '' },
      error: null,
      showPassword: false,
      isSubmitting: false,
      countdown: 3,
      timer: null,
      notification: {
        show: false,
        title: '',
        message: '',
        type: 'success',
        autoCloseDelay: null
      }
    };
  },
  methods: {
    async handleLogin() {
      this.error = null;
      this.notification.show = false;
      this.isSubmitting = true;
      if (this.timer) clearInterval(this.timer);

      try {
        await login(this.form);
        
        this.countdown = 3;
        this.notification = {
            show: true,
            title: "Login Realizado!",
            message: `Login bem-sucedido! Redirecionando em ${this.countdown}s...`,
            type: "success",
            autoCloseDelay: (this.countdown * 1000) + 500
        };

        this.timer = setInterval(() => {
          this.countdown--;
          if (this.countdown > 0) {
            // Atualiza a mensagem da notificação existente
            this.notification.message = `Login bem-sucedido! Redirecionando em ${this.countdown}s...`;
          } else {
            this.handleNotificationCloseAndRedirect();
          }
        }, 1000);

      } catch (err) {
        console.error("Erro de login:", err.response?.data || err);
        let errorMessage = 'Usuário ou senha inválidos.';
        if (err.response && err.response.data) {
            const errorData = err.response.data;
            if (errorData.detail) {
                errorMessage = errorData.detail;
            } else if (typeof errorData === 'object' && errorData.non_field_errors) {
                errorMessage = Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors.join(' ') : errorData.non_field_errors;
            } else if (typeof errorData === 'object' && Object.keys(errorData).length > 0) {
                const firstKey = Object.keys(errorData)[0];
                const firstError = Array.isArray(errorData[firstKey]) ? errorData[firstKey][0] : errorData[firstKey];
                // Evitar mostrar nomes de campos técnicos como 'username' diretamente se a mensagem for genérica
                if (errorData[firstKey] && typeof errorData[firstKey] === 'string' && errorData[firstKey].toLowerCase().includes('field is required')) {
                    errorMessage = `O campo '${firstKey}' é obrigatório.`
                } else {
                    errorMessage = `${firstKey.replace("_", " ")}: ${firstError}`;
                }
            }
        } else if (err.message && !err.response) { // Erros de rede, etc.
            errorMessage = 'Ocorreu um erro de conexão. Tente novamente.';
        }
        this.error = errorMessage;
      } finally {
          this.isSubmitting = false;
      }
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    handleNotificationClose() { // Chamado quando o NotificationModal emite 'close'
        this.notification.show = false;
        // Se o timer ainda estiver rodando (usuário fechou manualmente o toast),
        // limpa o timer e redireciona imediatamente.
        if (this.timer) {
            this.handleNotificationCloseAndRedirect();
        }
    },
    handleNotificationCloseAndRedirect() {
        if (this.timer) clearInterval(this.timer);
        this.timer = null;
        this.notification.show = false;
        this.$emit('login-redirect');
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
};
</script>

<style scoped>
.auth-form-container {
  width: 100%;
  max-width: 400px;
  padding: var(--sp-xl);
  background: var(--color-bg-component);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
}

.auth-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--sp-xs);
}

.auth-subtitle {
    text-align: center;
    color: var(--color-text-secondary);
    margin-bottom: var(--sp-xl);
}

.form-group { margin-bottom: var(--sp-lg); }

.password-input-wrapper {
  position: relative;
}
.password-input-wrapper .input {
  padding-right: 40px;
}
.password-toggle-button {
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  background: none; border: none;
  padding: var(--sp-sm);
  color: var(--color-text-muted);
  cursor: pointer;
}

.button-block {
    display: block;
    width: 100%;
    padding: var(--sp-md);
    font-size: var(--fs-large);
    font-weight: var(--fw-semibold);
    margin-top: var(--sp-lg);
}

.switch-text {
  text-align: center;
  margin-top: var(--sp-xl);
  font-size: var(--fs-base);
}
.switch-text .link {
  font-weight: var(--fw-semibold);
  color: var(--color-primary);
}

.alert { margin-top: var(--sp-md); }

/* Animação do Spinner (semelhante ao anterior) */
.button-spinner { animation: rotate 0.8s linear infinite; width: 1.2em; height: 1.2em; }
.button-spinner .path { stroke: currentColor; stroke-linecap: round; animation: dash 1.5s ease-in-out infinite; }
@keyframes rotate { 100% { transform: rotate(360deg); } }
@keyframes dash {
  0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
  50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
}
</style>