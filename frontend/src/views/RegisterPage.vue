<template>
  <div class="register-page-wrapper"> <AppHeader />
    <main class="auth-page-container"> <CadastroUser @navigate="goToLogin" />
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import CadastroUser from '@/components/CadastroUser.vue'; // Nome do componente importado

export default {
  name: 'RegisterPage',
  components: { AppHeader, CadastroUser, AppFooter },
  methods: {
    goToLogin() {
      // Certifique-se de que 'LoginPage' é o nome correto da sua rota de login
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
.register-page-wrapper { /* Classe wrapper principal da página */
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-bg-body); /* Fundo global do corpo da página */
}

.auth-page-container { /* Container para centralizar o formulário de autenticação */
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--sp-lg) var(--sp-md); /* Espaçamento global */
  /* O fundo já vem de .register-page-wrapper, a menos que queira um tom diferente aqui */
  /* background-color: var(--color-bg-muted); */
}
</style>