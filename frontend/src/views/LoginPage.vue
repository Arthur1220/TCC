<template>
  <div class="login-page-wrapper">
    <AppHeader />
    <main class="auth-page-container">
      <Login @navigate="goToRegister" @login-redirect="performRedirect" />
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import Login from '@/components/Login.vue';
import { getUserProfile } from '@/services/userService'; // Importar para buscar perfil

// !!! IMPORTANTE: Confirme estes IDs e nomes com seu backend !!!
// Este mapa pode ser centralizado em um arquivo de constantes se usado em múltiplos lugares
const ROLE_ID_MAP = {
  1: 'administrador', // Exemplo
  2: 'gerente',       // Exemplo
  3: 'usuario',       // Exemplo
  // Certifique-se que os nomes aqui (minúsculos) correspondem aos usados na lógica de verificação
};

export default {
  name: 'LoginPage',
  components: { AppHeader, Login, AppFooter },
  methods: {
    goToRegister() {
      this.$router.push({ name: 'RegisterPage' }); // Certifique-se que 'RegisterPage' é o nome da sua rota
    },
    async performRedirect() {
      // Este método é chamado após o modal de sucesso do Login.vue ser fechado.
      // A AppHeader.vue já deve ter atualizado o estado de autenticação e o userProfile.
      // Podemos tentar buscar o perfil aqui novamente para garantir os dados mais recentes para redirecionamento.
      try {
        const userProfile = await getUserProfile(); // Busca o perfil atualizado

        if (userProfile && userProfile.roles && Array.isArray(userProfile.roles)) {
          const roleNamesLower = userProfile.roles
            .map(userRoleObject => ROLE_ID_MAP[userRoleObject.role])
            .filter(name => name !== undefined);

          if (roleNamesLower.includes('administrador') || roleNamesLower.includes('gerente')) {
            this.$router.push({ name: 'AdminPage' }); // Nome da rota admin
          } else if (roleNamesLower.includes('usuario')) {
            this.$router.push({ name: 'DashboardPage' }); // Nome da rota dashboard
          } else {
            console.warn('Usuário logado sem role de redirecionamento definida. Indo para Dashboard por padrão.');
            this.$router.push({ name: 'DashboardPage' });
          }
        } else {
          console.error('Perfil do usuário ou roles não encontrados após login para redirecionamento.');
          this.$router.push({ name: 'DashboardPage' }); // Fallback
        }
      } catch (error) {
        console.error('Erro ao buscar perfil para redirecionamento:', error.response?.data || error);
        // Em caso de erro ao buscar o perfil (ex: token expirou entre o login e aqui),
        // talvez redirecionar para a home ou forçar logout.
        this.$router.push('/');
      }
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