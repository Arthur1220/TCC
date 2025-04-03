<template>
  <div class="app-container">
    <Header :LoginStatus="LoginStatus" :contractStatus="contractStatus" />

    <div class="main-content">
      <!-- Passa a propriedade selectedItem para o Uperbar -->
      <Uperbar :items="menuItems" :selectedItem="selectedItem" @selectItem="handleSelection" />
      
      <!-- Espaço reservado para o conteúdo dinâmico -->
      <section class="content-area">
        <component :is="currentComponent" />
      </section>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header_MVP.vue";
import Uperbar from "@/components/Uperbar_MVP.vue";
import Footer from "@/components/Footer_MVP.vue";

export default {
  name: "MVPContract",
  components: {
    Header,
    Uperbar,
    Footer,
  },
  data() {
    return {
      // Status simulados (podem ser atualizados via backend)
      LoginStatus: "off",
      contractStatus: "Ativo",
      selectedItem: null,
      // Menu com rótulos e componentes correspondentes
      menuItems: [
        { label: "Adicionar Carteira", component: "01" },
        { label: "Remover Carteira", component: "02" },
        { label: "Registrar Evento", component: "03" },
        { label: "Visualizar por Animal", component: "04" },
        { label: "Visualizar por Index", component: "05" },
        { label: "Visualizar Numero de Eventos", component: "06" },
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

/* Área que contém a Uperbar e o conteúdo */
.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Espaço reservado para o componente de conteúdo */
.content-area {
  flex: 1;
  margin-top: 1rem; /* Espaço entre a uperbar e o conteúdo */
  padding: 1rem;
  background-color: var(--color-light-gray);
}

/* Responsividade */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
}
</style>