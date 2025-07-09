<template>
  <div class="auth-form-container">
    <h2 class="auth-title">Crie a Sua Conta</h2>
    <p class="auth-subtitle">Comece a rastrear o seu rebanho hoje mesmo.</p>
    
    <form @submit.prevent="handleRegister" class="form">
      <div class="form-group">
        <label for="username" class="form-label">Usuário*</label>
        <input type="text" id="username" v-model="form.username" placeholder="Escolha um nome de usuário" class="input" required />
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label for="first_name" class="form-label">Nome*</label>
          <input type="text" id="first_name" v-model="form.first_name" placeholder="Digite seu nome" class="input" required />
        </div>
        <div class="form-group">
          <label for="last_name" class="form-label">Sobrenome*</label>
          <input type="text" id="last_name" v-model="form.last_name" placeholder="Digite seu sobrenome" class="input" required />
        </div>
      </div>
      
      <div class="form-group">
        <label for="email" class="form-label">E-mail*</label>
        <input type="email" id="email" v-model="form.email" placeholder="Digite seu e-mail" class="input" required />
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Senha*</label>
        <div class="password-input-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="form.password"
            placeholder="Crie uma senha (mín. 8 caracteres)"
            class="input"
            required
            aria-required="true"
            minlength="8"
          />
          <button
            type="button"
            class="password-toggle-button"
            @click="showPassword = !showPassword"
            :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
            :title="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
          >
            <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.44-4.75C21.27 7.61 17 4.5 12 4.5c-1.6 0-3.14.35-4.54.98l2.28 2.28C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="confirm_password" class="form-label">Repita a senha*</label>
        <div class="password-input-wrapper">
          <input
            :type="showConfirm ? 'text' : 'password'"
            id="confirm_password"
            v-model="form.confirm_password"
            placeholder="Repita sua senha"
            class="input"
            required
            aria-required="true"
            minlength="8"
          />
          <button
            type="button"
            class="password-toggle-button"
            @click="showConfirm = !showConfirm"
            :aria-label="showConfirm ? 'Ocultar senha' : 'Mostrar senha'"
            :title="showConfirm ? 'Ocultar senha' : 'Mostrar senha'"
          >
            <svg v-if="showConfirm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.44-4.75C21.27 7.61 17 4.5 12 4.5c-1.6 0-3.14.35-4.54.98l2.28 2.28C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
          </button>
        </div>
      </div>


      <div class="form-group">
        <label for="phone" class="form-label">Telefone</label>
        <input type="tel" id="phone" v-model="form.phone" placeholder="(xx) xxxxx-xxxx" class="input" />
      </div>

      <button type="submit" class="button button-primary button-block">Criar Conta</button>
    </form>

    <p class="switch-text">
      Já tem uma conta? <a @click.prevent="$emit('navigate','login')" href="#" class="link">Faça login</a>
    </p>

    <Teleport to="body">
      <NotificationModal
        :show="showNotification"
        :title="notification.title"
        :message="notification.message"
        :type="notification.type"
        :auto-close-delay="notification.autoCloseDelay"
        @close="showNotification = false"
      />
    </Teleport>
  </div>
</template>

<script>
import { registerUser } from '@/services/userService';
import NotificationModal from '@/components/NotificationModal.vue'; // Importar

export default {
  name: 'CadastroUser', // Renomeado para corresponder à importação
  components: {
    NotificationModal // Registrar
  },
  emits: ['navigate'],
  data() {
    return {
      form: {
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '', // Mantido para validação no frontend
        phone: ''
      },
      showPassword: false,
      showConfirm: false,
      // Para NotificationModal
      showNotification: false,
      notification: {
        title: '',
        message: '',
        type: 'success', // 'success' ou 'error'
        autoCloseDelay: null, // null para não fechar automaticamente, ou um número em ms
      },
      countdown: 3,
      timer: null
    };
  },
  methods: {
    displayNotification(title, message, type = 'error', autoCloseDelay = 3000) {
        this.notification.title = title;
        this.notification.message = message;
        this.notification.type = type;
        this.notification.autoCloseDelay = autoCloseDelay;
        this.showNotification = true;
    },
    async handleRegister() {
      this.showNotification = false; // Esconde notificações anteriores

      if (this.form.password !== this.form.confirm_password) {
        this.displayNotification('Erro de Validação', 'As senhas não coincidem.', 'error');
        return;
      }
      if (this.form.password.length < 8) {
        this.displayNotification('Erro de Validação', 'A senha deve ter no mínimo 8 caracteres.', 'error');
        return;
      }

      // Não envie confirm_password para o backend
      const { confirm_password, ...payload } = this.form;

      try {
        await registerUser(payload); // userService.registerUser deve enviar os dados corretos

        this.displayNotification(
            'Cadastro Realizado!',
            `Sua conta foi criada com sucesso! Você será redirecionado para o login em ${this.countdown}s...`,
            'success',
            null // Não fecha automaticamente, o timer fará isso
        );
        
        this.timer = setInterval(() => {
          this.countdown--;
          this.notification.message = `Sua conta foi criada com sucesso! Você será redirecionado para o login em ${this.countdown}s...`; // Atualiza mensagem do modal
          if (this.countdown <= 0) {
            clearInterval(this.timer);
            this.timer = null;
            this.showNotification = false; // Fecha o modal antes de navegar
            this.$emit('navigate', 'login'); // Navega para a página de login
          }
        }, 1000);

      } catch (err) {
        console.error("Erro no cadastro:", err.response?.data || err);
        let errorMessage = 'Não foi possível concluir o cadastro.';
        if (err.response && err.response.data) {
            const errors = err.response.data;
            if (typeof errors === 'object') {
                // Concatena todas as mensagens de erro do objeto
                errorMessage += ' Detalhes: ' + Object.entries(errors).map(([key, value]) => {
                    let fieldName = key;
                    if (key === 'username') fieldName = 'Usuário';
                    if (key === 'email') fieldName = 'E-mail';
                    // Adicione mais traduções de campos se necessário
                    return `${fieldName}: ${Array.isArray(value) ? value.join(', ') : value}`;
                }).join('; ');
            } else if (typeof errors === 'string') {
                errorMessage += ` Detalhes: ${errors}`;
            }
        } else if (err.message) {
            errorMessage += ` Detalhes: ${err.message}`;
        }
        this.displayNotification('Erro no Cadastro', errorMessage, 'error');
      }
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
  max-width: 500px;
  padding: var(--sp-xl);
  background: var(--color-bg-component);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
}

.auth-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  text-align: center;
  margin-bottom: var(--sp-xs);
}

.auth-subtitle {
  text-align: center;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-xl);
}

.form-group {
  margin-bottom: var(--sp-lg);
}

.form-grid {
  display: grid;
  gap: var(--sp-lg);
}

@media (min-width: 576px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;
  }
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
}
.switch-text .link {
  font-weight: var(--fw-semibold);
  color: var(--color-primary);
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.password-input-wrapper .input {
   padding-right: calc(var(--sp-lg) + var(--sp-md));
}

.password-toggle-button {
  position: absolute;
  top: 50%;
  right: var(--sp-sm);
  transform: translateY(-50%);
  background: none;
  border: none;
  padding: var(--sp-xs);
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.password-toggle-button:hover, .password-toggle-button:focus {
  color: var(--color-primary);
}
.password-toggle-button svg {
    width: 20px;
    height: 20px;
}
</style>