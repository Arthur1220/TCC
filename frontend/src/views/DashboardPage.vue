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
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg> Animais
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
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm1-13h-2v6h2V7zm0 8h-2v2h2v-2z"/></svg>
                Transferir Animal
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <main class="dashboard-main-content"> <div v-if="activeContent === 'home'" class="home-content">
          <div class="search-filter-bar form-group"> <input
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

          <section class="home-overview card"> <div class="welcome-section">
              <h1 class="welcome-title">Bem-vindo, {{ user.username || 'Usuário' }}!</h1>
              <p class="last-activity-text"> Última atividade:
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
      <div class="modal-content card search-modal-content"> <div class="modal-header">
            <h3 class="modal-title-text">Resultados da Busca por "{{ displayedSearchQuery }}"</h3>
            <button @click="closeSearchModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <div class="modal-body">
            <ul v-if="searchResults.length" class="results-list-modal"> <li
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
      @close="closeNotification"
    />
  </div>
</template>

<script>
// ... (imports como antes)
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
import { getAnimalGroups } from '@/services/lookupService'; // Assumindo que esta filtra por usuário no backend ou retorna todos
import { getUserProperties } from '@/services/propertyService';
// import { getEvents } from '@/services/eventService'; // Para lastActivity real

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
      searchQuery: '', // Usado pela barra de busca
      displayedSearchQuery: '',
      searchResults: [],
      showSearchModal: false,
      selectedAnimalIdForContent: null, // Para AnimalContent após busca
      genericSearchQueryForContent: '', // Para PropertyContent, se a busca for genérica
      activeContent: 'home',
      notification: { show: false, message: '', type: 'success' },
    };
  },
  computed: {
      canShowStickyButton() {
          // Mostrar o botão se não estiver na tela de Eventos OU
          // se estiver na tela de Eventos mas o modal de novo evento não estiver aberto (lógica mais complexa, precisa de estado do EventContent)
          // Simplificando por agora: não mostrar na tela de eventos.
          return this.activeContent !== 'events';
      }
  },
  async mounted() {
    try {
      const profile = await getUserProfile();
      this.user = profile || { username: 'Usuário', id: null }; // Fallback para user

      const [animalsData, allGroupsData, propsData] = await Promise.allSettled([
        profile.id ? getAnimals({ owner: profile.id }) : Promise.resolve([]),
        getAnimalGroups(), // Idealmente, o backend filtra por owner ou é um lookup geral
        profile.id ? getUserProperties() : Promise.resolve([]),
        // profile.id ? getEvents({ recorded_by: profile.id, ordering: '-date', limit: 1 }) : Promise.resolve([]) // Exemplo
      ]);

      this.stats.animals = animalsData.status === 'fulfilled' ? animalsData.value.length : 0;
      
      // Filtra grupos pelo owner no frontend se getAnimalGroups retornar todos
      // Se getAnimalGroups já for filtrado pelo backend para o usuário logado, este filtro é redundante.
      const userGroups = allGroupsData.status === 'fulfilled' ? allGroupsData.value.filter(g => g.owner === profile.id) : [];
      this.stats.lots = userGroups.length;

      this.stats.properties = propsData.status === 'fulfilled' ? propsData.value.length : 0;
      
      // Exemplo de lógica para lastActivity (pode ser melhorado)
      const animals = animalsData.status === 'fulfilled' ? animalsData.value : [];
      if (animals.length > 0) {
        this.lastActivity = {
          description: `Você possui ${animals.length} animais registrados.`,
          date: new Date().toLocaleDateString('pt-BR'), // Data de hoje como exemplo
        };
      }

    } catch (err) {
      console.error('Erro ao carregar dados do dashboard:', err.response?.data || err);
      this.showAppNotification('Falha ao carregar dados do dashboard.', 'error');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        this.$router.push('/login');
      }
    }
  },
  methods: {
    showAppNotification(message, type = 'error') {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
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
          console.warn("Referência para EventContent ou método openModal não encontrado ao tentar criar novo evento.");
          this.showAppNotification("Não foi possível abrir o formulário de novo evento.", "error");
        }
      });
    },
    async onSearch() {
      if (!this.searchQuery.trim()) {
        this.showAppNotification('Digite um termo para buscar.', 'info');
        return;
      }
      this.displayedSearchQuery = this.searchQuery;
      this.selectedAnimalIdForContent = null; // Limpa seleção anterior
      this.genericSearchQueryForContent = this.searchQuery; // Para PropertyContent, se aplicável

      try {
        // Assumindo que a busca principal é por identificação de animal
        // O backend DEVE filtrar por `owner: this.user.id` implicitamente ou explicitamente
        const list = await getAnimals({ identification__icontains: this.searchQuery.trim() });
        this.searchResults = list.map(a => ({
            ...a,
            breed_name: a.breed_name || 'N/D'
        }));
        if (this.searchResults.length === 0) {
            this.showAppNotification(`Nenhum animal encontrado para "${this.displayedSearchQuery}".`, 'info');
        }
        this.showSearchModal = true;
      } catch (error) {
        console.error("Erro na busca de animais:", error.response?.data || error);
        this.showAppNotification("Erro ao buscar animais. Tente novamente.", 'error');
        this.searchResults = [];
      }
    },
    selectSearchResult(animal) {
      this.showSearchModal = false;
      this.selectedAnimalIdForContent = animal.id;
      this.searchQuery = animal.identification; // Preenche a barra de busca com o item selecionado
      this.activeContent = 'animals';
      // A prop :key em AnimalContent já deve forçar a atualização se selectedAnimalIdForContent mudar.
    },
    closeSearchModal() {
        this.showSearchModal = false;
    }
  }
};
</script>

<style scoped>
/* Estilos Globais e Variáveis CSS são aplicados */
.dashboard-page {
  display: flex;
  flex-direction: column;
  min-height: 130vh;
  background-color: var(--color-bg-body);
}

.dashboard-body {
  display: flex;
  flex: 1;
  overflow: hidden; /* Evita scroll duplo se sidebar/content tiverem seus próprios scrolls */
}

/* Sidebar */
.sidebar {
  width: 260px; /* Largura aumentada */
  background: var(--color-bg-component); /* Fundo branco */
  border-right: var(--border-width) solid var(--color-border);
  padding: var(--sp-lg) 0;
  flex-shrink: 0; /* Sidebar não encolhe */
  overflow-y: auto; /* Scroll se muitos itens */
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar nav li {
  margin: 0;
}
.sidebar nav a {
  display: flex; /* Para alinhar ícone e texto */
  align-items: center;
  gap: var(--sp-sm); /* Espaço entre ícone e texto */
  padding: var(--sp-md) var(--sp-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: var(--transition-base);
  border-left: 4px solid transparent;
  font-weight: var(--fw-medium);
}
.sidebar nav a svg { /* Estilo para os ícones SVG na sidebar */
    flex-shrink: 0;
    color: var(--color-text-muted); /* Cor padrão do ícone */
    transition: color var(--transition-fast);
}
.sidebar nav a:hover,
.sidebar nav a:focus {
  background-color: var(--color-bg-hover);
  color: var(--color-primary); /* Cor de destaque no hover */
  border-left-color: var(--color-primary-light); /* Borda de destaque suave */
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


/* Main Content Area */
.dashboard-main-content { /* Renomeado de .dashboard-content */
  flex: 1;
  padding: var(--sp-lg) var(--sp-xl);
  overflow-y: auto; /* Permite scroll apenas no conteúdo principal */
}
.home-content { /* Wrapper para o conteúdo da home */
    max-width: 900px; /* Limita a largura do conteúdo da home */
    margin: 0 auto; /* Centraliza */
}

.search-filter-bar { /* Renomeado de .search-filter-group */
  /* .form-group global já tem display:flex, flex-direction:column. Ajustar se necessário */
  display: flex; /* Sobrescreve para linha */
  flex-direction: row;
  gap: var(--sp-sm); /* Menor gap entre input e botão */
  margin-bottom: var(--sp-xl);
  align-items: center;
}
.search-input-field { /* .input global é aplicado */
  flex-grow: 1; /* Input ocupa espaço */
}
.search-button { /* .button .button-primary globais são aplicados */
  flex-shrink: 0; /* Botão não encolhe */
  display: flex; /* Para alinhar ícone e texto do botão */
  align-items: center;
  gap: var(--sp-xs);
}

/* Home Overview Section */
.home-overview {
  /* .card global já aplica background, padding, border-radius, box-shadow */
  padding: var(--sp-xl);
  margin-bottom: var(--sp-xl);
}
.welcome-section {
  text-align: center;
  margin-bottom: var(--sp-xl);
}
.welcome-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h1); /* Título de boas-vindas maior */
  color: var(--color-text-primary);
  margin-bottom: var(--sp-xs);
}
.last-activity-text { /* Renomeado de .last-event */
  font-size: var(--fs-base);
  color: var(--color-text-muted); /* Cor mais suave */
}
.last-activity-text strong {
    font-weight: var(--fw-medium);
    color: var(--color-text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); /* Cards de stats um pouco maiores */
  gap: var(--sp-lg);
}
.stat-card {
  /* .card global já aplica estilos base */
  padding: var(--sp-lg);
  text-align: center;
  transition: var(--transition-base);
  cursor: pointer;
}
.stat-card:hover, .stat-card:focus-within { /* Usar focus-within se houver elementos focáveis dentro */
  /* :hover e :focus do .card global já aplicam transform e shadow */
  border-color: var(--color-primary); /* Destaque extra na borda */
}
.stat-icon {
    font-size: 2rem; /* Tamanho para ícones emoji */
    display: block;
    margin-bottom: var(--sp-sm);
    color: var(--color-primary);
}
.stat-value { /* Era h4 */
  font-family: var(--font-body);
  font-size: var(--fs-h2); /* Números bem grandes */
  font-weight: var(--fw-bold);
  color: var(--color-primary);
  margin-bottom: var(--sp-xs);
  line-height: 1;
}
.stat-label { /* Era p */
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
  margin:0;
}

/* Dynamic Content Area (onde os componentes são carregados) */
.dynamic-content-area {
    margin-top: var(--sp-xl); /* Espaço acima da área de conteúdo dinâmico */
}

/* Sticky Action Button */
.sticky-action-button { /* Renomeado de .sticky-new-event */
  /* .button .button-primary .button-lg já aplicados no template */
  position: fixed;
  bottom: var(--sp-xl);
  right: var(--sp-xl);
  z-index: var(--zindex-sticky);
  box-shadow: var(--shadow-lg); /* Sombra mais pronunciada */
  border-radius: var(--border-radius-pill); /* Botão redondo */
  width: auto; /* Ajusta à largura do conteúdo */
  padding: var(--sp-md); /* Padding para botão redondo com ícone */
  display: flex;
  align-items: center;
  gap: var(--sp-xs);
}
.sticky-action-button:hover, .sticky-action-button:focus {
  /* Efeitos de hover do .button global já se aplicam */
  transform: scale(1.05) translateY(-2px); /* Ajuste no transform */
}


/* Search Results Modal */
/* .modal-overlay, .modal-content, .modal-title já usam estilos globais */
.search-modal-content {
  /* A classe .card global já foi aplicada ao modal-content no template */
  max-width: 500px;
  text-align: left;
}
.modal-header { /* Estilo para cabeçalho de modal */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: var(--sp-sm);
    margin-bottom: var(--sp-md);
    border-bottom: var(--border-width) solid var(--color-border);
}
.modal-title-text { /* Se precisar de um estilo específico para o texto do título */
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

.modal-body { /* Corpo do modal, se necessário */
    padding-top: var(--sp-sm);
}

.results-list-modal { /* Renomeado de .modal-list */
  list-style: none;
  padding: 0;
  margin-bottom: var(--sp-lg);
  max-height: 350px; /* Altura aumentada */
  overflow-y: auto;
}
.result-item-modal { /* Renomeado de .modal-list-item */
  padding: var(--sp-sm) var(--sp-xs); /* Padding ajustado */
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
.empty-state { /* Estilo global deve ser suficiente */
    padding: var(--sp-lg);
    color: var(--color-text-muted);
}


@media (max-width: 992px) { /* Breakpoint para tablet */
    .dashboard-body {
        flex-direction: column;
        align-items: stretch;
    }
    .sidebar {
        width: 100%;
        border-right: none;
        border-bottom: var(--border-width) solid var(--color-border);
        padding: var(--sp-sm) 0; /* Padding vertical menor */
        overflow-y: hidden; /* Evitar scroll na sidebar no mobile, se for horizontal */
    }
    .sidebar nav ul { /* Navegação horizontal no mobile */
        display: flex;
        overflow-x: auto; /* Permite scroll horizontal nos links */
        padding: 0 var(--sp-sm); /* Padding lateral para a lista */
        justify-content: flex-start; /* Alinha à esquerda, permitindo scroll */
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
    .sidebar nav ul::-webkit-scrollbar { /* Chrome, Safari, Opera */
        display: none;
    }
    .sidebar nav li {
        flex-shrink: 0; /* Impede que os itens encolham */
    }
    .sidebar nav a {
        padding: var(--sp-sm) var(--sp-md); /* Padding dos links ajustado */
        border-left: none; /* Remove borda esquerda */
        border-bottom: 4px solid transparent; /* Borda inferior para indicar ativo */
        white-space: nowrap; /* Impede quebra de linha nos textos dos links */
    }
    .sidebar nav li.active-link > a {
        border-left-color: transparent; /* Remove borda esquerda no ativo */
        border-bottom-color: var(--color-primary); /* Borda inferior ativa */
    }
    .dashboard-main-content {
        padding: var(--sp-md); /* Menos padding no mobile */
    }
    .home-content {
        max-width: 100%; /* Ocupa toda a largura */
    }
}

@media (max-width: 576px) { /* Breakpoint para mobile pequeno */
  .search-filter-bar {
    flex-direction: column;
    gap: var(--sp-sm);
  }
  .search-input-field, .search-filter-bar > .button {
      width: 100%;
      max-width: none;
  }
  .stats-grid {
    grid-template-columns: 1fr; /* Uma coluna sempre */
  }
  .sticky-action-button {
      bottom: var(--sp-md);
      right: var(--sp-md);
      padding: var(--sp-sm); /* Botão menor */
  }
  .sticky-action-button .button-text {
      display: none; /* Esconde o texto, mostrando só o ícone */
  }
   .sticky-action-button svg {
      margin: 0; /* Centraliza ícone se texto some */
  }
  .welcome-title {
      font-size: var(--fs-h2);
  }
  .search-modal-content {
      max-width: 95%; /* Modal de busca quase tela cheia */
  }
}
</style>