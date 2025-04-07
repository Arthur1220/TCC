<template>
  <header class="app-header">
    <div class="header-left">
      <img src="@/assets/logo_blue.png" alt="Logo" class="logo" />
      <h1>AnimalTracking</h1>
    </div>
    <div class="header-right">
      <!-- Exibe os status dinâmicos -->
      <span :class="statusClass(currentLoginStatus)">Login: {{ currentLoginStatus }}</span>
      <span :class="statusClass(currentContractStatus)">Contrato: {{ currentContractStatus }}</span>
    </div>
  </header>
</template>

<script>
import { getUserProfile } from '@/services/userService';
import { checkContractStatus } from '@/services/contractService';

export default {
  name: "Header",
  data() {
    return {
      currentLoginStatus: "Desconhecido",
      currentContractStatus: "Inativo",
    };
  },
  methods: {
    statusClass(status) {
      return status === "Ativo" ? "status-active" : "status-inactive";
    },
    async checkLoginStatus() {
      try {
        // Tenta obter o perfil do usuário autenticado
        await getUserProfile();
        // Se a requisição for bem-sucedida, o usuário está logado
        this.currentLoginStatus = "Ativo";
      } catch (error) {
        // Se houver erro, assume que o usuário não está autenticado
        this.currentLoginStatus = "Desconhecido";
      }
    },
    async updateContractStatus() {
      try {
        const result = await checkContractStatus();
        this.currentContractStatus = result.active ? "Ativo" : "Inativo";
      } catch (error) {
        console.error("Erro ao obter status do contrato:", error);
        this.currentContractStatus = "Inativo";
      }
    },
  },
  mounted() {
    // Verifica o status de login e do contrato assim que o componente é montado
    this.checkLoginStatus();
    this.updateContractStatus();
  },
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  height: 4rem;
}

.header-left {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.header-left h1 {
  margin-bottom: 0;
}

.logo {
  width: 50px;
  height: 50px;
  margin-right: 0.5rem;
}

.header-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: var(--font-size-small);
  text-align: center;
  gap: 0.2rem;
  position: absolute;
  right: 1.5rem;
}

.status-active {
  color: var(--color-secondary);
  font-weight: 600;
}

.status-inactive {
  color: var(--color-gray);
  font-weight: 400;
}
</style>
