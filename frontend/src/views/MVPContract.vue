<template>
  <div class="app-container">
    <Header :LoginStatus="LoginStatus" :contractStatus="contractStatus" />
    <div class="main-content">
      <Uperbar :items="menuItems" :selectedItem="selectedItem" @selectItem="handleSelection" />
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

// Importe os componentes de contrato
import AddWallet from "@/components/AddWallet.vue";
import RemoveWallet from "@/components/RemoveWallet.vue";
import RegisterEvent from "@/components/RegisterEvent.vue";
import ViewEventByAnimal from "@/components/ViewEventByAnimal.vue";
import ViewEventCount from "@/components/ViewEventCount.vue";

export default {
  name: "MVPContract",
  components: {
    Header,
    Uperbar,
    Footer,
    AddWallet,
    RemoveWallet,
    RegisterEvent,
    ViewEventByAnimal,
    ViewEventCount
  },
  data() {
    return {
      LoginStatus: "off",
      contractStatus: "Ativo",
      selectedItem: null,
      menuItems: [
        { label: "Adicionar Carteira", component: "AddWallet" },
        { label: "Remover Carteira", component: "RemoveWallet" },
        { label: "Registrar Evento", component: "RegisterEvent" },
        { label: "Visualizar por Animal", component: "ViewEventByAnimal" },
        { label: "Visualizar Número de Eventos", component: "ViewEventCount" }
      ]
    };
  },
  computed: {
    currentComponent() {
      if (!this.selectedItem) {
        return "div";
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