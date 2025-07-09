<template>
  <div class="auth-page-wrapper">
    <div class="welcome-panel">
      <div class="welcome-content">
        <h1 class="logo-welcome" @click="goHome">AnimalTracking</h1>
        <p class="welcome-text">
          Junte-se à nossa plataforma e tenha controlo total sobre a rastreabilidade do seu rebanho.
        </p>
      </div>
    </div>

    <main class="auth-form-panel">
      <CadastroUser @navigate="goToLogin" />
    </main>
  </div>
</template>

<script>
import CadastroUser from '@/components/CadastroUser.vue';

export default {
  name: 'RegisterPage',
  components: { CadastroUser },
  methods: {
    goToLogin() {
      this.$router.push({ name: 'Login' });
    },
    goHome() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
/* Estilos reutilizados da LoginPage para consistência */
.auth-page-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 100%;
  min-height: 100vh;
  background-color: var(--color-bg-component);
}

.welcome-panel {
  background: linear-gradient(135deg, rgba(26, 115, 232, 0.9), rgba(29, 83, 162, 0.95)), url('@/assets/images/farm-background.jpg') no-repeat center center;
  background-size: cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: var(--sp-xxl);
  color: var(--color-white);
  text-align: center;
}

.welcome-content {
  max-width: 450px;
}

.logo-welcome {
  color: var(--color-white);
  font-family: var(--font-heading);
  font-size: var(--fs-h1-2);
  font-weight: var(--fw-black);
  cursor: pointer;
  margin-bottom: var(--sp-md);
  line-height: 1.1;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
}

.welcome-text {
  font-size: var(--fs-large);
  opacity: 0.9;
  line-height: 1.6;
}

.auth-form-panel {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--sp-lg);
  background-color: var(--color-bg-body);
}

/* Responsividade */
@media (max-width: 992px) {
  .auth-page-wrapper {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
  }

  .welcome-panel {
    min-height: auto;
    padding: var(--sp-xl) var(--sp-md);
  }

  .logo-welcome {
      font-size: var(--fs-h2);
  }
  
  .welcome-text {
      font-size: var(--fs-base);
  }

  .auth-form-panel {
      padding: var(--sp-xl) var(--sp-md);
  }
}
</style>