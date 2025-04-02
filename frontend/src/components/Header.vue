<template>
  <header class="app-header">
    <div class="header-left">
      <img src="@/assets/logo_blue.png" alt="Logo" class="logo" />
      <h1>AnimalTracking</h1>
    </div>
    <div class="header-right">
      <!-- Exibindo status do backend e do contrato -->
      <span :class="statusClass(LoginStatus)">Login: {{ LoginStatus }}</span>
      <span :class="statusClass(contractStatus)">Contrato: {{ contractStatus }}</span>
    </div>
  </header>
</template>
  
<script>
export default {
  name: "Header",
  props: {
    LoginStatus: {
      type: String,
      default: "Desconhecido"
    },
    contractStatus: {
      type: String,
      default: "Inativo"
    }
  },
  methods: {
    statusClass(status) {
      return status === "Ativo" ? "status-active" : "status-inactive";
    }
  }
};
</script>
  
<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}
  
.header-left {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
}

.header-left h1 {
  margin-left: 0.5rem;
  margin-bottom: 0rem;
}
  
.logo {
  width: 50px;
  height: 50px;
  margin-right: 0.75rem;
}
  
.header-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: var(--font-size-small);
  text-align: center;
  gap: 0.2rem;
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
  