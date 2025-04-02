<template>
  <div class="app-container">
    <Header :backendStatus="backendStatus" :contractStatus="contractStatus" />

    <div class="main-content">
      <Sidebar :items="menuItems" @selectItem="handleSelection" />
      
      <!-- Conteúdo dinâmico via componente -->
      <section class="content-area">
        <component :is="currentComponent" />
      </section>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Sidebar from "@/components/Sidebar.vue";
import Footer from "@/components/Footer.vue";

// Importação dos componentes de conteúdo
//import UsuarioContent from "@/components/content/UsuarioContent.vue";
//import AnimalContent from "@/components/content/AnimalContent.vue";
//import PropriedadeContent from "@/components/content/PropriedadeContent.vue";
//import EventoContent from "@/components/content/EventoContent.vue";
//import LoginContent from "@/components/content/LoginContent.vue";
//import VisualizacaoContent from "@/components/content/VisualizacaoContent.vue";
//import BlockchainContent from "@/components/content/BlockchainContent.vue";
//import VerificarAtividadeContent from "@/components/content/VerificarAtividadeContent.vue";

export default {
  name: "MainLayout",
  components: {
    Header,
    Sidebar,
    Footer,
    //UsuarioContent,
    //AnimalContent,
    //PropriedadeContent,
    //EventoContent,
    //LoginContent,
    //VisualizacaoContent,
    //BlockchainContent,
    //VerificarAtividadeContent
  },
  data() {
    return {
      // Status simulados (podem ser atualizados via backend)
      backendStatus: "Ativo",
      contractStatus: "Ativo",
      selectedItem: null,
      // Menu com rótulos e componentes correspondentes
      menuItems: [
        { label: "usuario", component: "UsuarioContent" },
        { label: "animal", component: "AnimalContent" },
        { label: "propriedade", component: "PropriedadeContent" },
        { label: "evento", component: "EventoContent" },
        { label: "login", component: "LoginContent" },
        { label: "visualizacao", component: "VisualizacaoContent" },
        { label: "blockchain", component: "BlockchainContent" },
        { label: "verificar atividade", component: "VerificarAtividadeContent" }
      ]
    };
  },
  computed: {
    currentComponent() {
      if (!this.selectedItem) {
        return "div"; // Exibe um container vazio se nada estiver selecionado
      }
      const selected = this.menuItems.find(item => item.label === this.selectedItem);
      return selected ? selected.component : "div";
    }
  },
  methods: {
    handleSelection(item) {
      this.selectedItem = item.label;
    }
  }
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Área principal com Sidebar e Conteúdo */
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Sidebar com largura fixa */
.sidebar {
  width: 200px;
  min-width: 200px;
}

/* Área de conteúdo dinâmico */
.content-area {
  flex: 1;
  padding: 1rem;
  background-color: var(--color-light-gray);
  overflow-y: auto;
}

/* Responsividade */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    min-width: auto;
  }
  .content-area {
    padding: 1rem;
  }
}
</style>
