<template>
  <div class="dashboard-page">
    <AppHeader />

    <div class="dashboard-body">
      <!-- Sidebar Navigation -->
      <aside class="sidebar">
        <nav aria-label="Main Navigation">
          <ul>
            <li :class="{ 'active-link': activeContent === 'home' }">
              <a href="#" @click.prevent="selectContent('home')">Home</a>
            </li>
            <li :class="{ 'active-link': activeContent === 'properties' }">
              <a href="#" @click.prevent="selectContent('properties')">Propriedades</a>
            </li>
            <li :class="{ 'active-link': activeContent === 'animals' }">
              <a href="#" @click.prevent="selectContent('animals')">Animais</a>
            </li>
            <li :class="{ 'active-link': activeContent === 'events' }">
              <a href="#" @click.prevent="selectContent('events')">Eventos</a>
            </li>
            <li :class="{ 'active-link': activeContent === 'blockchain' }">
              <a href="#" @click.prevent="selectContent('blockchain')">Blockchain</a>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="dashboard-content">
        <!-- Search & Filter (Home only) -->
        <div
          class="search-filter-group"
          v-if="activeContent === 'home'"
        >
          <input
            type="text"
            class="search-input"
            placeholder="Buscar animais, lotes ou propriedades..."
            v-model="searchQuery"
            @input="onSearch"
            aria-label="Busca"
          />
          <select
            class="filter-select"
            v-model="filterOption"
            @change="onFilter"
            aria-label="Filtro"
          >
            <option value="all">Todos</option>
            <option value="animals">Animais</option>
            <option value="lots">Lotes</option>
            <option value="properties">Propriedades</option>
          </select>
        </div>

        <!-- Home Overview -->
        <section v-if="activeContent === 'home'" class="home-overview">
          <div class="welcome-section">
            <h2 class="welcome-title">Bem-vindo, Usuário X!</h2>
            <p class="last-event">
              Último evento registrado: <strong>{{ lastEvent.description }}</strong>
              em {{ lastEvent.date }}
            </p>
          </div>
          <div class="stats-grid">
            <div class="stat-card" tabindex="0">
              <h4>{{ stats.animals }}</h4>
              <p>Animais</p>
            </div>
            <div class="stat-card" tabindex="0">
              <h4>{{ stats.lots }}</h4>
              <p>Lotes</p>
            </div>
            <div class="stat-card" tabindex="0">
              <h4>{{ stats.properties }}</h4>
              <p>Propriedades</p>
            </div>
          </div>
        </section>

        <!-- Dynamic Content -->
        <AnimalContent
          v-if="activeContent === 'animals'"
          :search-query="searchQuery"
          :filter-option="filterOption"
        />
        <PropertyContent
          v-if="activeContent === 'properties'"
          :search-query="searchQuery"
          :filter-option="filterOption"
        />

        <EventContent
          v-if="activeContent === 'events'"
          :search-query="searchQuery"
          :filter-option="filterOption"
        />
        <BlockchainContent
          v-if="activeContent === 'blockchain'"
          :search-query="searchQuery"
          :filter-option="filterOption"
        />
      </main>
    </div>

    <AppFooter />

    <!-- Sticky New Event Button -->
    <button
      class="sticky-new-event button-primary"
      @click="goToNewEvent"
      aria-label="Registrar novo evento"
    >
      + Novo Evento
    </button>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import AnimalContent from '@/components/AnimalContent.vue'
import PropertyContent from '@/components/PropertyContent.vue'
import EventContent from '@/components/EventContent.vue'
import BlockchainContent from '@/components/BlockchainContent.vue'

export default {
  name: 'DashboardPage',
  components: {
    AppHeader,
    AppFooter,
    AnimalContent,
    PropertyContent,
    EventContent,
    BlockchainContent
  },
  data() {
    return {
      stats: { animals: 120, lots: 8, properties: 3 },
      lastEvent: { description: 'Vacinação do Animal 042', date: '2025-04-30' },
      searchQuery: '',
      filterOption: 'all',
      activeContent: 'home'
    }
  },
  methods: {
    selectContent(tab) {
      this.activeContent = tab
      this.searchQuery = ''
      this.filterOption = 'all'
    },
    goToNewEvent() {
      this.$router.push({ name: 'NewEvent' })
    },
    onSearch() {
      console.log('Buscando:', this.searchQuery)
    },
    onFilter() {
      console.log('Filtrando por:', this.filterOption)
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  height: 120vh; /* Forçar rolagem para que footer fique mais abaixo */
}
.dashboard-body {
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
/* Main Content */
.dashboard-content {
  flex: 1;
  padding: var(--sp-lg);
  overflow-y: auto;
}
.search-filter-group {
  width: 100%;
  display: flex;
  gap: var(--sp-md);
  margin-bottom: var(--sp-xl);
}
.search-input,
.filter-select {
  flex: 1;
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-base);
  transition: border-color 0.2s;
}
.search-input:focus,
.filter-select:focus {
  border-color: var(--color-primary);
  outline: none;
}
.filter-select {
  max-width: 200px;
}
/* Home Overview */
.home-overview {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.welcome-section {
  text-align: center;
  margin-bottom: var(--sp-lg);
}
.welcome-title {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: var(--color-primary);
  margin-bottom: var(--sp-sm);
}
.last-event {
  font-size: var(--font-size-base);
  color: var(--color-secondary);
  margin-bottom: var(--sp-lg);
}
.stats-grid {
  display: flex;
  justify-content: center;
  gap: var(--sp-lg);
}
.stat-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  padding: var(--sp-md);
  width: 120px;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover,
.stat-card:focus {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transform: translateY(-4px);
  outline: none;
}
.stat-card h4 {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  margin-bottom: var(--sp-sm);
  color: var(--color-secondary);
}
.stat-card p {
  font-size: var(--font-size-small);
  color: var(--color-dark-gray);
}
/* Sticky Button */
.sticky-new-event {
  position: fixed;
  bottom: var(--sp-xxl);
  right: var(--sp-lg);
  z-index: 100;
  transition: transform 0.2s, box-shadow 0.2s;
  width: 10%;
  padding: var(--sp-sm);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  border-radius: var(--sp-sm);
  font-size: var(--font-size-small);
  cursor: pointer;
}
.sticky-new-event:hover,
.sticky-new-event:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  transform: scale(1.1);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  outline: none;
}
@media (max-width: 768px) {
  .dashboard-body {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }
  .search-filter-group {
    flex-direction: column;
  }
  .stats-grid {
    flex-direction: column;
  }
}
</style>
