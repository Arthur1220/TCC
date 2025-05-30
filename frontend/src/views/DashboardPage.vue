<template>
  <div class="dashboard-page">
    <AppHeader />

    <div class="dashboard-body">
      <aside class="sidebar">
        <nav aria-label="Dashboard Navigation">
          <ul>
            <li :class="{ 'active-link': activeContent === 'home' }">
              <a href="#" @click.prevent="selectContent('home')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                Home
              </a>
            </li>
            <li :class="{ 'active-link': activeContent === 'properties' }">
              <a href="#" @click.prevent="selectContent('properties')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                Propriedades
              </a>
            </li>
            <li :class="{ 'active-link': activeContent === 'animals' }">
              <a href="#" @click.prevent="selectContent('animals')">
                <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 0 24 24" width="20px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41s-.23-1.06-.59-1.42zM13 20.99l-9-9V4h7l9 9-7 6.99z"/><circle cx="6.5" cy="6.5" r="1.5"/></svg>
                Animais
              </a>
            </li>
            <li :class="{ 'active-link': activeContent === 'events' }">
              <a href="#" @click.prevent="selectContent('events')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z"/></svg>
                Eventos
              </a>
            </li>
            <li :class="{ 'active-link': activeContent === 'userBlockchain' }">
              <a href="#" @click.prevent="selectContent('userBlockchain')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1s3.1 1.39 3.1 3.1v2z"/></svg> Meus Registros Blockchain
              </a>
            </li>
            <li :class="{ 'active-link': activeContent === 'transferOwnership' }">
              <a href="#" @click.prevent="selectContent('transferOwnership')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M6.99 11L3 15l3.99 4v-3H14v-2H6.99v-3zM21 9l-3.99-4v3H10v2h7.01v3L21 9z"/></svg>
                Transferir Animal
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <main class="dashboard-main-content">
        <div v-if="activeContent === 'home'" class="home-content">
          <div class="search-filter-bar form-group">
             <input
              v-model="searchQuery"
              @keyup.enter="onSearch"
              type="search" class="input search-input-field" placeholder="Buscar animais por identificação..."
              aria-label="Buscar animais"
            />
            <button class="button button-primary search-button" @click="onSearch">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18" style="margin-right: var(--sp-xs);"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
              Buscar
            </button>
          </div>

          <section class="home-overview card">
            <div class="welcome-section">
              <h1 class="welcome-title">Bem-vindo, {{ user.username || 'Usuário' }}!</h1>
              <p class="last-activity-text">
                Última atividade:
                <strong>{{ lastActivity.description || 'Nenhuma atividade recente.' }}</strong>
                <span v-if="lastActivity.date"> em {{ lastActivity.date }}</span>
              </p>
            </div>
            <div class="stats-grid">
              <div class="stat-card card" tabindex="0" @click="selectContent('animals')" @keydown.enter="selectContent('animals')">
                <span class="stat-icon">🐾</span> <h3 class="stat-value">{{ stats.animals }}</h3>
                <p class="stat-label">Animais</p>
              </div>
              <div class="stat-card card" tabindex="0" @click="selectContent('home')"> <span class="stat-icon">📦</span>
                <h3 class="stat-value">{{ stats.lots }}</h3>
                <p class="stat-label">Lotes/Grupos</p>
              </div>
              <div class="stat-card card" tabindex="0" @click="selectContent('properties')" @keydown.enter="selectContent('properties')">
                <span class="stat-icon">🏡</span>
                <h3 class="stat-value">{{ stats.properties }}</h3>
                <p class="stat-label">Propriedades</p>
              </div>
            </div>
          </section>

          <section class="blockchain-costs-overview card">
            <h2 class="section-title">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="22" height="22" style="margin-right: var(--sp-xs); vertical-align: middle;"><path d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6h16l-8 5z"/></svg> Resumo de Custos Blockchain
            </h2>
            <div v-if="isLoadingBlockchainCosts" class="loading-state">
                <p>Carregando resumo de custos...</p>
            </div>
            <div v-else-if="blockchainCostsError" class="empty-state text-danger">
                <p>Não foi possível carregar os custos: {{ blockchainCostsError }}</p>
            </div>
            <div v-else class="costs-content">
              <div class="costs-grid">
                <div class="cost-card card card-interactive">
                  <h3 class="cost-value">{{ blockchainCosts.total_cost_display }} <span class="cost-currency">{{ blockchainCosts.currency_display }}</span></h3>
                  <p class="cost-label">Custo Total Acumulado</p>
                  <p class="cost-detail-wei">(Total em {{ blockchainCosts.currency_wei }}: {{ blockchainCosts.total_cost_wei }})</p>
                </div>
                <div class="cost-card card card-interactive">
                  <h3 class="cost-value">{{ blockchainCosts.current_month_cost_display }} <span class="cost-currency">{{ blockchainCosts.currency_display }}</span></h3>
                  <p class="cost-label">Custo do Mês Atual</p>
                   <p class="cost-detail-wei">(Total em {{ blockchainCosts.currency_wei }}: {{ blockchainCosts.current_month_cost_wei }})</p>
                </div>
                <div class="cost-card card card-interactive">
                  <h3 class="cost-value">{{ blockchainCosts.last_30_days_cost_display }} <span class="cost-currency">{{ blockchainCosts.currency_display }}</span></h3>
                  <p class="cost-label">Custo Últimos 30 Dias</p>
                   <p class="cost-detail-wei">(Total em {{ blockchainCosts.currency_wei }}: {{ blockchainCosts.last_30_days_cost_wei }})</p>
                </div>
              </div>
              <div class="cost-explanation">
                <p><strong>Entenda os Custos:</strong></p>
                <p>Estes valores representam as taxas de gás (<code>gasUsed * effectiveGasPrice</code>) pagas na rede blockchain para registrar os eventos críticos dos seus animais (nascimentos, vacinas, movimentações, etc.). Cada registro garante a imutabilidade e transparência das informações.</p>
                <p>A unidade base para o custo é <strong>{{ blockchainCosts.currency_wei }}</strong>, que é a menor fração da criptomoeda da rede. Para facilitar a visualização, também apresentamos uma conversão aproximada para <strong>{{ blockchainCosts.currency_display }}</strong>.</p>
              </div>
            </div>
          </section>
          </div>

        <div class="dynamic-content-area">
            <AnimalContent
            v-if="activeContent === 'animals'"
            :key="'animals_' + selectedAnimalIdForContent" :search-query-prop="selectedAnimalIdForContent" />
            <PropertyContent
            v-if="activeContent === 'properties'"
            :key="'properties_' + genericSearchQueryForContent"
            :search-query-prop="genericSearchQueryForContent"
            />
            <EventContent
            v-if="activeContent === 'events'"
            ref="eventComp"
            />
            <BlockchainViewer
            v-if="activeContent === 'userBlockchain'"
            mode="user"
            :key="'BlockchainViewer' + user.id" 
            />
            <TransferOwnershipContent
            v-if="activeContent === 'transferOwnership'"
            ref="transferOwnershipComp"
            />
        </div>
      </main>
    </div>

    <AppFooter />

    <button
      class="sticky-action-button button button-primary button-lg"
      @click="goToNewEvent"
      aria-label="Registrar novo evento"
      title="Registrar Novo Evento"
      v-if="canShowStickyButton"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
      <span class="button-text">Novo Evento</span>
    </button>

    <div v-if="showSearchModal" class="modal-overlay" @click.self="closeSearchModal">
      <div class="modal-content card search-modal-content">
        <div class="modal-header">
            <h3 class="modal-title-text">Resultados da Busca por "{{ displayedSearchQuery }}"</h3>
            <button @click="closeSearchModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <div class="modal-body">
            <ul v-if="searchResults.length" class="results-list-modal">
                <li
                    v-for="a in searchResults"
                    :key="a.id"
                    class="result-item-modal"
                    @click="selectSearchResult(a)"
                    tabindex="0"
                    @keydown.enter="selectSearchResult(a)"
                >
                    <strong>{{ a.identification }}</strong> ({{a.breed_name || 'Raça N/D' }})
                </li>
            </ul>
            <p v-else class="empty-state">Nenhum animal encontrado para "{{ displayedSearchQuery }}".</p>
        </div>
        <div class="modal-actions form-actions">
            <button class="button button-secondary" @click="closeSearchModal">Fechar</button>
        </div>
      </div>
    </div>
     <NotificationModal
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
      :title="notification.title" @close="closeNotification"
    />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import AnimalContent from '@/components/AnimalContent.vue';
import PropertyContent from '@/components/PropertyContent.vue';
import EventContent from '@/components/EventContent.vue';
import BlockchainViewer from '@/components/BlockchainViewer.vue';
import TransferOwnershipContent from '@/components/TransferOwnershipContent.vue';
import NotificationModal from '@/components/NotificationModal.vue';

import { getUserProfile } from '@/services/userService';
import { getAnimals } from '@/services/animalService';
import { getAnimalGroups } from '@/services/lookupService';
import { getUserProperties } from '@/services/propertyService';
// Importe o novo serviço ou a função para buscar custos
import { fetchUserBlockchainCostsSummary } from '@/services/blockchainService'; // Crie este arquivo e função

export default {
  name: 'DashboardPage',
  components: {
    AppHeader,
    AppFooter,
    AnimalContent,
    PropertyContent,
    EventContent,
    BlockchainViewer,
    TransferOwnershipContent,
    NotificationModal,
  },
  data() {
    return {
      user: { username: '', id: null },
      stats: { animals: 0, lots: 0, properties: 0, events: 0 },
      lastActivity: { description: 'Nenhuma atividade recente.', date: '' },
      searchQuery: '',
      displayedSearchQuery: '',
      searchResults: [],
      showSearchModal: false,
      selectedAnimalIdForContent: null,
      genericSearchQueryForContent: '',
      activeContent: 'home',
      notification: { show: false, message: '', type: 'success', title: '' }, // Adicionado title
      
      // NOVOS DADOS PARA CUSTOS DA BLOCKCHAIN
      isLoadingBlockchainCosts: false,
      blockchainCostsError: null,
      blockchainCosts: {
        total_cost_wei: '0',
        current_month_cost_wei: '0',
        last_30_days_cost_wei: '0',
        total_cost_display: '0',
        current_month_cost_display: '0',
        last_30_days_cost_display: '0',
        currency_wei: 'WEI',
        currency_display: 'ETH', // Default, será atualizado pela API
      },
    };
  },
  computed: {
      canShowStickyButton() {
        return this.activeContent !== 'events';
      }
  },
  async mounted() {
    this.loadInitialDashboardData();
  },
  methods: {
    showAppNotification(message, type = 'error', title = '') { // Adicionado title opcional
      let notificationTitle = title;
      if (!notificationTitle) {
        if (type === 'success') notificationTitle = 'Sucesso';
        else if (type === 'error') notificationTitle = 'Erro';
        else if (type === 'warning') notificationTitle = 'Atenção';
        else notificationTitle = 'Informação';
      }
      this.notification = { message, type, title: notificationTitle, show: true };
      // O NotificationModal tem seu próprio autoCloseDelay
    },
    closeNotification() {
      this.notification.show = false;
    },
    selectContent(tab) {
      this.activeContent = tab;
      this.searchQuery = '';
      this.selectedAnimalIdForContent = null;
      this.genericSearchQueryForContent = '';
      if (tab !== 'home') {
        this.searchResults = [];
      }
    },
    goToNewEvent() {
      this.selectContent('events');
      this.$nextTick(() => {
        if (this.$refs.eventComp && typeof this.$refs.eventComp.openModal === 'function') {
          this.$refs.eventComp.openModal();
        } else {
          console.warn("Referência para EventContent ou método openModal não encontrado.");
          this.showAppNotification("Não foi possível abrir o formulário de novo evento.", "error", "Erro de Navegação");
        }
      });
    },
    async onSearch() {
      // ... (sua lógica de onSearch existente)
      if (!this.searchQuery.trim()) {
        this.showAppNotification('Digite um termo para buscar.', 'info', 'Busca');
        return;
      }
      this.displayedSearchQuery = this.searchQuery;
      this.selectedAnimalIdForContent = null; 
      this.genericSearchQueryForContent = this.searchQuery;

      try {
        const list = await getAnimals({ identification__icontains: this.searchQuery.trim() });
        this.searchResults = list.map(a => ({
            ...a,
            breed_name: a.breed_name || 'N/D'
        }));
        if (this.searchResults.length === 0) {
            this.showAppNotification(`Nenhum animal encontrado para "${this.displayedSearchQuery}".`, 'info', 'Busca');
        }
        this.showSearchModal = true;
      } catch (error) {
        console.error("Erro na busca de animais:", error.response?.data || error);
        this.showAppNotification("Erro ao buscar animais. Tente novamente.", 'error', 'Erro na Busca');
        this.searchResults = [];
      }
    },
    selectSearchResult(animal) {
      this.showSearchModal = false;
      this.selectedAnimalIdForContent = animal.id;
      this.searchQuery = animal.identification; 
      this.activeContent = 'animals';
    },
    closeSearchModal() {
        this.showSearchModal = false;
    },

    // --- MÉTODOS PARA CARREGAR DADOS DO DASHBOARD ---
    async loadInitialDashboardData() {
      try {
        const profile = await getUserProfile();
        this.user = profile || { username: 'Usuário', id: null };

        // Carrega estatísticas e custos em paralelo
        await Promise.all([
          this.fetchDashboardStats(profile), // Passa o perfil para evitar race condition
          this.fetchUserBlockchainCostsData(),
        ]);
        
        this.setLastActivityMessageBasedOnData();

      } catch (err) {
        console.error('Erro Crítico ao carregar dados do dashboard:', err.response?.data || err);
        this.showAppNotification('Falha crítica ao carregar dados do dashboard. Verifique sua conexão ou contate o suporte.', 'error', 'Erro de Carregamento', null); // Notificação persistente
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          this.$router.push('/login'); // Redireciona para login se não autenticado/autorizado
        }
      }
    },
    async fetchDashboardStats(userProfile) {
      if (!userProfile || !userProfile.id) {
        this.stats = { animals: 0, lots: 0, properties: 0, events: 0 };
        return;
      }
      try {
        const [animalsData, allGroupsData, propsData] = await Promise.allSettled([
          getAnimals({ owner: userProfile.id }),
          getAnimalGroups(),
          getUserProperties(), // Assume que este é filtrado por usuário no backend ou no serviço
        ]);

        this.stats.animals = animalsData.status === 'fulfilled' ? animalsData.value.length : 0;
        
        const userGroups = allGroupsData.status === 'fulfilled' 
          ? allGroupsData.value.filter(g => g.owner === userProfile.id) 
          : [];
        this.stats.lots = userGroups.length;

        this.stats.properties = propsData.status === 'fulfilled' ? propsData.value.length : 0;
      } catch (error) {
        console.error("Erro ao buscar estatísticas do dashboard:", error);
        this.showAppNotification('Falha ao carregar estatísticas.', 'warning', 'Atenção');
      }
    },
    async fetchUserBlockchainCostsData() { // Renomeado para evitar conflito com nome de serviço
      this.isLoadingBlockchainCosts = true;
      this.blockchainCostsError = null;
      try {
        const data = await fetchUserBlockchainCostsSummary(); // Nome da função no serviço
        this.blockchainCosts = {
            total_cost_wei: data.total_cost_wei || '0',
            current_month_cost_wei: data.current_month_cost_wei || '0',
            last_30_days_cost_wei: data.last_30_days_cost_wei || '0',
            total_cost_display: data.total_cost_display || '0',
            current_month_cost_display: data.current_month_cost_display || '0',
            last_30_days_cost_display: data.last_30_days_cost_display || '0',
            currency_wei: data.currency_wei || 'WEI',
            currency_display: data.currency_display || 'ETH'
        };
      } catch (error) {
        console.error('Erro ao buscar custos da blockchain:', error.response?.data || error);
        this.blockchainCostsError = error.response?.data?.detail || 'Não foi possível carregar os custos.';
        // this.showAppNotification('Falha ao carregar os custos da blockchain.', 'error', 'Erro de Custos');
      } finally {
        this.isLoadingBlockchainCosts = false;
      }
    },
    setLastActivityMessageBasedOnData() {
        if (this.stats.animals > 0) {
            this.lastActivity = {
                description: `Você possui ${this.stats.animals} animais registrados.`,
                date: new Date().toLocaleDateString('pt-BR'),
            };
        } else {
            this.lastActivity = { description: 'Nenhuma atividade recente.', date: '' };
        }
    }
  }
};
</script>

<style scoped>
/* Seus estilos existentes para .dashboard-page, .dashboard-body, etc. */
.dashboard-page {
  display: flex;
  flex-direction: column;
  min-height: 130vh; /* Mínimo de 100vh para ocupar a tela inteira */
  background-color: var(--color-bg-body);
}
.dashboard-body {
  display: flex;
  flex: 1;
  overflow: hidden; 
}
.sidebar {
  width: 260px; 
  background: var(--color-bg-component); 
  border-right: var(--border-width) solid var(--color-border);
  padding: var(--sp-lg) 0;
  flex-shrink: 0; 
  overflow-y: auto; 
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar nav li { margin: 0; }
.sidebar nav a {
  display: flex; 
  align-items: center;
  gap: var(--sp-sm); 
  padding: var(--sp-md) var(--sp-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: var(--transition-base);
  border-left: 4px solid transparent;
  font-weight: var(--fw-medium);
}
.sidebar nav a svg { 
    flex-shrink: 0;
    color: var(--color-text-muted); 
    transition: color var(--transition-fast);
}
.sidebar nav a:hover,
.sidebar nav a:focus {
  background-color: var(--color-bg-hover);
  color: var(--color-primary); 
  border-left-color: var(--color-primary-light); 
}
.sidebar nav a:hover svg,
.sidebar nav a:focus svg {
    color: var(--color-primary);
}
.sidebar nav li.active-link > a {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: var(--fw-semibold);
  border-left-color: var(--color-primary);
}
.sidebar nav li.active-link > a svg {
    color: var(--color-primary);
}
.dashboard-main-content { 
  flex: 1;
  padding: var(--sp-lg) var(--sp-xl);
  overflow-y: auto; 
}
.home-content { 
    max-width: 900px; 
    margin: 0 auto; 
}
.search-filter-bar { 
  display: flex; 
  flex-direction: row;
  gap: var(--sp-sm); 
  margin-bottom: var(--sp-xl);
  align-items: center;
}
.search-input-field { 
  flex-grow: 1; 
}
.search-button { 
  flex-shrink: 0; 
  display: flex; 
  align-items: center;
  gap: var(--sp-xs);
}
.home-overview {
  padding: var(--sp-xl);
  margin-bottom: var(--sp-xl);
}
.welcome-section {
  text-align: center;
  margin-bottom: var(--sp-xl);
}
.welcome-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h1); 
  color: var(--color-text-primary);
  margin-bottom: var(--sp-xs);
}
.last-activity-text { 
  font-size: var(--fs-base);
  color: var(--color-text-muted); 
}
.last-activity-text strong {
    font-weight: var(--fw-medium);
    color: var(--color-text-secondary);
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
  gap: var(--sp-lg);
}
.stat-card {
  padding: var(--sp-lg);
  text-align: center;
  transition: var(--transition-base);
  cursor: pointer;
}
.stat-card:hover, .stat-card:focus-within { 
  border-color: var(--color-primary); 
}
.stat-icon {
    font-size: 2rem; 
    display: block;
    margin-bottom: var(--sp-sm);
    color: var(--color-primary);
}
.stat-value { 
  font-family: var(--font-body);
  font-size: var(--fs-h2); 
  font-weight: var(--fw-bold);
  color: var(--color-primary);
  margin-bottom: var(--sp-xs);
  line-height: 1;
}
.stat-label { 
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
  margin:0;
}
.dynamic-content-area {
    margin-top: var(--sp-xl); 
}
.sticky-action-button { 
  position: fixed;
  bottom: var(--sp-xl);
  right: var(--sp-xl);
  z-index: var(--zindex-sticky);
  box-shadow: var(--shadow-lg); 
  border-radius: var(--border-radius-pill); 
  width: auto; 
  padding: var(--sp-md); 
  display: flex;
  align-items: center;
  gap: var(--sp-xs);
}
.sticky-action-button:hover, .sticky-action-button:focus {
  transform: scale(1.05) translateY(-2px); 
}
.search-modal-content {
  max-width: 500px;
  text-align: left;
}
.modal-header { 
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: var(--sp-sm);
    margin-bottom: var(--sp-md);
    border-bottom: var(--border-width) solid var(--color-border);
}
.modal-title-text { 
    font-family: var(--font-heading);
    font-size: var(--fs-h4);
    color: var(--color-text-primary);
    margin: 0;
}
.button-close {
    background: none; border: none; font-size: var(--fs-large);
    color: var(--color-text-muted); cursor: pointer; padding: var(--sp-xs); line-height: 1;
}
.button-close:hover { color: var(--color-text-primary); }
.modal-body { 
    padding-top: var(--sp-sm);
}
.results-list-modal { 
  list-style: none;
  padding: 0;
  margin-bottom: var(--sp-lg);
  max-height: 350px; 
  overflow-y: auto;
}
.result-item-modal { 
  padding: var(--sp-sm) var(--sp-xs); 
  border-bottom: var(--border-width) solid var(--color-border-light);
  cursor: pointer;
  transition: var(--transition-base);
  border-radius: var(--border-radius-sm);
  color: var(--color-text-secondary);
}
.result-item-modal:last-child {
    border-bottom: none;
}
.result-item-modal:hover, .result-item-modal:focus {
  background-color: var(--color-bg-hover);
  color: var(--color-primary);
}
.result-item-modal strong {
    color: var(--color-text-primary);
    font-weight: var(--fw-medium);
}
.empty-state { 
    padding: var(--sp-lg);
    color: var(--color-text-muted);
}

/* NOVOS ESTILOS PARA A SEÇÃO DE CUSTOS */
.blockchain-costs-overview {
  /* .card já aplica estilos base */
  padding: var(--sp-xl);
  margin-top: var(--sp-xl); /* Espaçamento acima da seção de custos */
}

.section-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h3); /* Ou h4, dependendo da hierarquia */
  color: var(--color-text-primary);
  margin-bottom: var(--sp-lg); /* Espaço abaixo do título da seção */
  display: flex;
  align-items: center;
}

.costs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); /* Ajuste minmax se necessário */
  gap: var(--sp-lg);
  margin-bottom: var(--sp-xl);
}

.cost-card {
  /* Herda estilos do .card global e .card-interactive (se definido) */
  padding: var(--sp-lg); /* Padding maior para destaque */
  text-align: center;
  background-color: var(--color-bg-muted); /* Fundo sutilmente diferente */
}

.cost-value {
  font-family: var(--font-body); /* Usar fonte do corpo para números, ou manter heading */
  font-size: var(--fs-h6); /* Valor bem destacado */
  font-weight: var(--fw-bold);
  color: var(--color-accent); /* Usar a cor de destaque */
  margin-bottom: var(--sp-xs);
  line-height: 1.1;
}

.cost-currency {
  font-size: var(--fs-small); /* Menor que o valor */
  font-weight: var(--fw-normal);
  color: var(--color-text-muted);
  margin-left: var(--sp-xxs);
  text-transform: uppercase;
}
.cost-detail-wei {
    font-size: var(--fs-smaller);
    color: var(--color-text-muted);
    margin-top: var(--sp-xxs);
}

.cost-label {
  font-size: var(--fs-base); /* Tamanho base para o label */
  color: var(--color-text-secondary);
  margin: 0;
}

.cost-explanation {
  margin-top: var(--sp-lg);
  padding: var(--sp-md);
  background-color: var(--color-bg-body); /* Fundo igual ao da página para integrar */
  border-left: 4px solid var(--color-info); /* Uma borda de destaque sutil */
  border-radius: var(--border-radius-sm);
}
.cost-explanation p {
  font-size: var(--fs-small);
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: var(--sp-sm);
}
.cost-explanation strong {
  font-weight: var(--fw-semibold); /* Usar semibold para destaque em vez de bold */
  color: var(--color-text-primary);
}
.cost-explanation code {
    font-family: var(--font-monospace);
    background-color: var(--color-bg-muted);
    padding: var(--sp-xxs) var(--sp-xs);
    border-radius: var(--border-radius-sm);
    font-size: 0.9em;
}

.loading-state { /* Estilo genérico para estados de carregamento */
    text-align: center;
    padding: var(--sp-xl);
    color: var(--color-text-muted);
    font-size: var(--fs-large);
}
.text-danger { /* Utilitário para texto de erro */
    color: var(--color-danger);
}


@media (max-width: 992px) { 
    .sidebar nav ul { 
        display: flex;
        overflow-x: auto; 
        padding: 0 var(--sp-sm); 
        justify-content: flex-start; 
        -ms-overflow-style: none;  
        scrollbar-width: none;  
    }
    .sidebar nav ul::-webkit-scrollbar { 
        display: none;
    }
    .sidebar nav li {
        flex-shrink: 0; 
    }
    .sidebar nav a {
        padding: var(--sp-sm) var(--sp-md); 
        border-left: none; 
        border-bottom: 4px solid transparent; 
        white-space: nowrap; 
    }
    .sidebar nav li.active-link > a {
        border-left-color: transparent; 
        border-bottom-color: var(--color-primary); 
    }
    .dashboard-main-content {
        padding: var(--sp-md); 
    }
    .home-content {
        max-width: 100%; 
    }
}

@media (max-width: 576px) { 
  .search-filter-bar {
    flex-direction: column;
    gap: var(--sp-sm);
  }
  .search-input-field, .search-filter-bar > .button {
      width: 100%;
      max-width: none;
  }
  .stats-grid {
    grid-template-columns: 1fr; 
  }
  .sticky-action-button {
      bottom: var(--sp-md);
      right: var(--sp-md);
      padding: var(--sp-sm); 
  }
  .sticky-action-button .button-text {
      display: none; 
  }
    .sticky-action-button svg {
      margin: 0; 
  }
  .welcome-title {
      font-size: var(--fs-h2);
  }
  .search-modal-content {
      max-width: 95%; 
  }
  .costs-grid { /* Ajusta grid de custos para uma coluna em telas pequenas */
    grid-template-columns: 1fr;
  }
}
</style>