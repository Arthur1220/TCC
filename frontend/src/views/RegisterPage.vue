<template>
    <div class="register-page">
      <AppHeader />
      <main class="auth-page">
        <CadastroContent @navigate="goToLogin" />
      </main>
      <AppFooter />
    </div>
  </template>
  
  <script>
  import AppHeader from '@/components/AppHeader.vue';
  import AppFooter from '@/components/AppFooter.vue';
  import CadastroContent from '@/components/CadastroUser.vue';
  export default {
    name: 'RegisterPage',
    components: { AppHeader, CadastroContent, AppFooter },
    methods: {
      goToLogin() {
        this.$router.push({ name: 'Login' });
      }
    }
  };
  </script>
  
  <style scoped>
  .register-page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .auth-page {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--sp-lg);
    background: var(--color-light-gray);
  }
  </style>