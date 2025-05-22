<!-- File: src/views/AdminPage.vue -->
<template>
  <div class="admin-page">
    <AppHeader />

    <div class="admin-body">
      <!-- Sidebar de Admin -->
      <aside class="sidebar">
        <nav aria-label="Admin Navigation">
          <ul>
            <li :class="{ 'active-link': activeSection === 'overview' }">
              <a href="#" @click.prevent="selectSection('overview')">Visão Geral</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'register' }">
              <a href="#" @click.prevent="selectSection('register')">Registrar Carteira</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'remove' }">
              <a href="#" @click.prevent="selectSection('remove')">Remover Carteira</a>
            </li>
            <li :class="{ 'active-link': activeSection === 'pause' }">
              <a href="#" @click.prevent="selectSection('pause')">
                {{ contractActive ? 'Pausar Contrato' : 'Ativar Contrato' }}
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'events' }">
              <a href="#" @click.prevent="selectSection('events')">Visualizar Eventos</a>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Conteúdo Principal -->
      <main class="admin-content">
        <!-- Visão Geral -->
        <section v-if="activeSection === 'overview'" class="card stats-overview">
          <h2>Visão Geral do Sistema</h2>
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

        <!-- Registrar Carteira -->
        <section v-else-if="activeSection === 'register'" class="card form-section">
          <AddWallet />
        </section>

        <!-- Remover Carteira -->
        <section v-else-if="activeSection === 'remove'" class="card form-section">
          <RemoveWallet />
        </section>

        <!-- Pausar / Ativar Contrato -->
        <section v-else-if="activeSection === 'pause'" class="card form-section">
          <h2 class="section-title">{{ contractActive ? 'Pausar Contrato' : 'Ativar Contrato' }}</h2>
          <button
            class="button-primary"
            @click="contractActive ? handlePause() : handleUnpause()"
          >
            {{ contractActive ? 'Pausar' : 'Ativar' }}
          </button>
        </section>

        <!-- Visualização de Eventos -->
        <section v-else-if="activeSection === 'events'" class="card">
          <VisualizacaoContent />
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

import { getUserProfile } from '@/services/userService'
import { getAnimals } from '@/services/animalService'
import { getNumberOfEvents, checkContractStatus, pauseContract, unpauseContract } from '@/services/contractService'

export default {
  name: 'AdminPage',
  components: {
    AppHeader,
    AppFooter,
    AddWallet,
    RemoveWallet,
    VisualizacaoContent
  },
  data() {
    return {
      stats: { animals: 0, events: 0 },
      contractActive: false,
      activeSection: 'overview'
    }
  },
  async mounted() {
    // carrega total de animais
    const animals = await getAnimals().catch(() => [])
    this.stats.animals = animals.length

    // soma total de eventos
    let total = 0
    for (const a of animals) {
      const { count = 0 } = await getNumberOfEvents(a.id).catch(() => ({}))
      total += count
    }
    this.stats.events = total

    // status do contrato
    const { active = false } = await checkContractStatus().catch(() => ({}))
    this.contractActive = active
  },
  methods: {
    selectSection(sec) {
      this.activeSection = sec
    },
    async handlePause() {
      try {
        await pauseContract()
        this.contractActive = false
        alert('Contrato pausado.')
      } catch {
        alert('Erro ao pausar contrato.')
      }
    },
    async handleUnpause() {
      try {
        await unpauseContract()
        this.contractActive = true
        alert('Contrato ativado.')
      } catch {
        alert('Erro ao ativar contrato.')
      }
    }
  }
}
</script>

<style scoped>
.admin-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.admin-body {
  display: flex;
  flex: 1;
  background: var(--color-light-gray);
}
/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--color-white);
  border-right: 1px solid var(--color-border);
  padding: var(--sp-lg) 0;
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
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
}
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
.stats-overview h2,
.form-section h2 {
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
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover,
.stat-card:focus {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transform: translateY(-4px);
  outline: none;
}
.stat-card h3 {
  font-size: 2rem;
  margin-bottom: var(--sp-sm);
}
.button-primary {
  padding: var(--sp-sm) var(--sp-lg);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
</style>
