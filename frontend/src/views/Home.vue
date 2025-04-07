<template>
  <div class="app-container">
    <Header :LoginStatus="LoginStatus" :contractStatus="contractStatus" />

    <div class="main-content">
        <!-- Passa a propriedade selectedItem para o Uperbar -->
        <Uperbar :items="menuItems" :selectedItem="selectedItem" @selectItem="handleSelection" />
      
        <!-- Espaço reservado para o conteúdo dinâmico -->
        <section class="content-area">
            <component :is="currentComponent" @switchComponent="handleSwitchComponent" />
        </section>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header_MVP.vue";
import Uperbar from "@/components/Uperbar_MVP.vue";
import Footer from "@/components/Footer_MVP.vue";
import Login from "@/components/Login.vue";
import CadastroUser from "@/components/CadastroUser.vue";

export default {
    name: "Home",
    components: {
        Header,
        Uperbar,
        Footer,
        Login,
        CadastroUser
    },
    data() {
        return {
            // Status simulados (atualize via backend conforme necessário)
            LoginStatus: "off",
            contractStatus: "Ativo",
            selectedItem: "Login",
            // Menu com rótulos e componentes correspondentes (os componentes podem ser importados ou mapeados)
            menuItems: [
                { label: "Login", component: "Login" },
                { label: "Cadastro", component: "CadastroUser" },
            ]
        };
    },
    computed: {
        currentComponent() {
            const selected = this.menuItems.find(item => item.label === this.selectedItem);
            return selected ? selected.component : "div";
        }
    },
    methods: {
        handleSelection(item) {
            this.selectedItem = item.label;
        },
        // Método para receber o evento emitido pelos componentes filhos
        handleSwitchComponent(componentName) {
            this.selectedItem = componentName;
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
