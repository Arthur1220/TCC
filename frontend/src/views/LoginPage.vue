<template>
  <div class="login-page-wrapper">
    <AppHeader />
    <main class="auth-page-container">
      <Login @navigate="goToRegister" @login-redirect="handleLoginSuccess" />
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import Login from '@/components/Login.vue';
// Não precisamos mais de getUserProfile ou ROLE_ID_MAP aqui, pois o router cuidará disso.

export default {
  name: 'LoginPage',
  components: { AppHeader, Login, AppFooter },
  methods: {
    goToRegister() {
      // CORREÇÃO: O nome da rota é 'Register', não 'RegisterPage'
      this.$router.push({ name: 'Register' }); 
    },
    handleLoginSuccess() {
      // MELHORIA PRINCIPAL:
      // Em vez de duplicar a lógica de verificação de perfil,
      // simplesmente navegamos para a raiz do site ('/').
      // O nosso guarda de rotas (`router.beforeEach`) que já está configurado
      // vai interceptar essa navegação, ver que o usuário está logado e
      // redirecioná-lo AUTOMATICAMENTE para a página correta (/admin ou /dashboard).
      // Isso centraliza a lógica e evita erros.
      this.$router.push({ path: '/' });
    }
  }
};
</script>

<style scoped>
.login-page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 130vh;
  background-color: var(--color-bg-body);
}

.auth-page-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--sp-lg) var(--sp-md);
}
</style>