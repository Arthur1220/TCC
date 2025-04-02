<template>
    <header class="app-header">
      <div class="header-left">
        <!-- Substitua pelo caminho correto da sua logo, se desejar -->
        <img src="@/assets/logo.png" alt="Logo" class="logo" />
        <h1>AnimalTracking</h1>
      </div>
      <div class="header-right">
        <!-- Exibindo status do backend e do contrato -->
        <span :class="statusClass(backendStatus)">Backend: {{ backendStatus }}</span>
        <span :class="statusClass(contractStatus)">Contrato: {{ contractStatus }}</span>
      </div>
    </header>
  </template>
  
  <script>
  export default {
    name: "Header",
    props: {
      backendStatus: {
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
        // Retorna uma classe diferente se estiver "Ativo" ou "Inativo"
        return status === "Ativo" ? "status-active" : "status-inactive";
      }
    }
  };
  </script>
  
  <style scoped>
  .app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background-color: var(--color-white);
    border-bottom: 1px solid var(--color-light-gray);
  }
  
  .header-left {
    display: flex;
    align-items: center;
  }
  
  .logo {
    width: 50px;
    height: 50px;
    margin-right: 0.75rem;
  }
  
  .header-right {
    display: flex;
    gap: 1rem;
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
  