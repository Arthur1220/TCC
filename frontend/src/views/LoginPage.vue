<template>
  <div class="auth-page-wrapper">
    <div class="welcome-panel">
      <div class="welcome-content">
        <h1 class="logo-welcome" @click="goHome" tabindex="0">AnimalTracking</h1>
        <p class="welcome-text">
          A plataforma definitiva para a rastreabilidade e gestão do seu rebanho.
        </p>
      </div>
    </div>

    <main class="auth-form-panel">
      <Login @navigate="goToRegister" @login-redirect="handleLoginSuccess" />
    </main>
  </div>
</template>

<script>
import Login from '@/components/Login.vue';

export default {
  name: 'LoginPage',
  components: { Login },
  methods: {
    goToRegister() {
      this.$router.push({ name: 'Register' }); 
    },
    goHome() {
      this.$router.push('/');
    },
    handleLoginSuccess() {
      const redirectPath = this.$route.query.redirect || '/dashboard'; // Redireciona para o dashboard por padrão
      this.$router.push(redirectPath);
    }
  }
};
</script>

<style scoped>
.auth-page-wrapper {
  display: grid;
  width: 100%;
  min-height: 100vh;
  /* Layout padrão para desktop (2 colunas) */
  grid-template-columns: 1fr 1fr;
}

.welcome-panel {
  background: linear-gradient(135deg, rgba(26, 115, 232, 0.9), rgba(29, 83, 162, 0.95)), url('@/assets/farm-background.jpg') no-repeat center center;
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

/* ============================
   RESPONSIVIDADE CORRIGIDA
   ============================ */
@media (max-width: 992px) {
  .auth-page-wrapper {
    /* Altera o layout para uma única coluna em telas menores */
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr; /* O painel de boas-vindas tem altura automática, o formulário ocupa o resto */
  }

  .welcome-panel {
    /* O painel de boas-vindas torna-se um cabeçalho menor */
    min-height: auto;
    padding: var(--sp-xl) var(--sp-md); /* Reduz o padding */
  }

  .logo-welcome {
      font-size: var(--fs-h1); /* Reduz o tamanho da logo */
  }
  
  .welcome-text {
      font-size: var(--fs-base); /* Reduz o texto de boas-vindas */
  }

  .auth-form-panel {
      padding: var(--sp-xl) var(--sp-md);
  }
}
</style>