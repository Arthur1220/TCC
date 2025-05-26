<template>
  <div class="admin-page">
    <AppHeader />

    <div class="admin-body">
      <aside class="sidebar">
        <nav aria-label="Admin Navigation">
          <ul>
            <li :class="{ 'active-link': activeSection === 'overview' }">
              <a href="#" @click.prevent="selectSection('overview')">Home</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'carteira' }">
              <a href="#" @click.prevent="selectSection('carteira')">Carteira</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'pause' }">
              <a href="#" @click.prevent="selectSection('pause')">
                {{ contractActive ? 'Pausar Contrato' : 'Ativar Contrato' }}
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'events' }">
              <a href="#" @click.prevent="selectSection('events')">Visualizar Eventos</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'blockchain' }"> <a href="#" @click.prevent="selectSection('blockchain')">Blockchain</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'users' }">
              <a href="#" @click.prevent="selectSection('users')">Usuários</a>
            </li>
          </ul>
        </nav>
      </aside>

      <main class="admin-content">
        <section v-if="activeSection === 'overview'" class="card stats-overview">
          <h2 class="section-title">Visão Geral do Sistema</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <h3>{{ stats.animals }}</h3>
              <p>Total de Animais</p>
            </div>
            <div class="stat-card">
              <h3>{{ stats.events }}</h3>
              <p>Total de Eventos</p>
            </div>
            <div class="stat-card">
              <h3>{{ contractActive ? 'Ativo' : 'Pausado' }}</h3>
              <p>Status do Contrato</p>
            </div>
          </div>
        </section>

        <section v-else-if="activeSection === 'carteira'" class="card form-section">
          <h2 class="section-title">Gerenciar Carteiras</h2>
          <div class="wallet-controls">
            <AddWallet />
            <RemoveWallet />
          </div>
        </section>

        <section v-else-if="activeSection === 'pause'" class="card form-section">
          <PauseContract
            :isActive="contractActive"
            @update:active="contractActive = $event"
          />
        </section>

        <section v-else-if="activeSection === 'events'" class="card">
          <VisualizacaoContent />
        </section>

        <section v-else-if="activeSection === 'blockchain'" class="card">
          <BlockchainViewer />
        </section>

        <section v-else-if="activeSection === 'users'" class="card">
          <RoleManager />
        </section>
      </main>
    </div>

    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

import AddWallet from '@/components/AddWallet.vue'
import RemoveWallet from '@/components/RemoveWallet.vue'
import VisualizacaoContent from '@/components/VisualizacaoContent.vue'
import PauseContract from '@/components/PauseContract.vue'
import RoleManager from '@/components/RoleManager.vue'
import BlockchainViewer from '@/components/BlockchainViewer.vue' // IMPORTAR O NOVO COMPONENTE

import { getAnimals } from '@/services/animalService'
import { getNumberOfEvents, checkContractStatus } from '@/services/contractService'

export default {
  name: 'AdminPage',
  components: {
    AppHeader,
    AppFooter,
    AddWallet,
    RemoveWallet,
    VisualizacaoContent,
    PauseContract,
    RoleManager,
    BlockchainViewer // ADICIONAR AQUI
  },
  data() {
    return {
      stats: { animals: 0, events: 0 },
      contractActive: false,
      activeSection: 'overview'
    }
  },
  async mounted() {
    const animals = await getAnimals().catch(() => [])
    this.stats.animals = animals.length

    let total = 0
    for (const a of animals) {
      const count = await getNumberOfEvents(a.id).catch(() => 0)
      total += count
    }
    this.stats.events = total

    const { active = false } = await checkContractStatus().catch(() => ({}))
    this.contractActive = active
  },
  methods: {
    selectSection(sec) {
      this.activeSection = sec
    }
  }
}
</script>

<style scoped>
/* Seus estilos CSS atuais permanecem aqui. Nenhuma alteração é estritamente necessária,
   a não ser que você queira ajustar o espaçamento ou alinhamento para o novo componente.
   Assegure-se de que as variáveis CSS (:root) estejam definidas ou importadas corretamente.
*/
.admin-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.admin-body {
  display: flex;
  flex: 1;
  background: var(--color-light-gray);
  align-items: center;              /* centraliza verticalmente */
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--color-white);
  border-right: 1px solid var(--color-border);
  padding: var(--sp-lg) 0;
  display: flex;
  flex-direction: column;
  justify-content: center;          /* centraliza verticalmente */
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar nav li {
  margin: var(--sp-sm) 0;
}

.sidebar nav a {
  display: block;
  padding: var(--sp-sm) var(--sp-lg);
  color: var(--color-dark-gray);
  text-decoration: none;
  transition: background 0.2s, transform 0.1s;
}

.sidebar nav a:hover {
  background-color: var(--color-accent);
  color: var(--color-bg);
  transform: translateX(4px);
}

.sidebar nav li.active-link > a {
  background: var(--color-white);
  color: var(--color-accent);
}

/* Conteúdo */
.admin-content {
  flex: 1;
  padding: var(--sp-lg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;          /* centraliza verticalmente */
}

/* Sobrescreve o efeito de hover para os cards dentro do AdminPage */
.admin-content .card:hover,
.admin-content .card:focus-within {
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); /* Mantém a sombra padrão ou 'none' */
  transform: none; /* Remove o efeito de levantar */
}

/* Cartões e seções */
.card {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: var(--sp-lg);
}

.section-title {
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}

.stats-grid {
  display: flex;
  gap: var(--sp-lg);
  justify-content: center;
}

.stat-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  padding: var(--sp-md);
  text-align: center;
}

.stat-card h3 {
  font-size: 2rem;
  margin-bottom: var(--sp-sm);
}

.form-section .wallet-controls {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center; /* Centraliza horizontalmente */
}
</style>