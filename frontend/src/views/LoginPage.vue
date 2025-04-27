<template>
    <div class="login-page">
      <AppHeader />
      <main class="auth-page">
        <Login @navigate="goToRegister" />
      </main>
      <AppFooter />
    </div>
  </template>
  
  <script>
  import AppHeader from '@/components/AppHeader.vue';
  import AppFooter from '@/components/AppFooter.vue';
  import Login from '@/components/Login.vue';
  
  export default {
    name: 'LoginPage',
    components: { AppHeader, Login, AppFooter },
    methods: {
      goToRegister() {
        this.$router.push({ name: 'Register' });
      }
    }
  };
  </script>
  
  <style scoped>
  .login-page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .auth-page {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: var(--sp-lg);
    background: var(--color-light-gray);
  }
  auth-page .auth-form {
    margin: 0;
  }
  </style>
  