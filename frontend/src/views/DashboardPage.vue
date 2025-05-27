<template>
  <div class="dashboard-page">
    <AppHeader />

    <div class="dashboard-body">
      <aside class="sidebar">
        <nav aria-label="Main navigation">
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
            <li :class="{ 'active-link': activeContent === 'userBlockchain' }">
              <a href="#" @click.prevent="selectContent('userBlockchain')">Meus Registros Blockchain</a>
            </li>
          </ul>
        </nav>
      </aside>

      <main class="dashboard-content">
        <div v-if="activeContent === 'home'" class="search-filter-group">
          <input
            v-model="searchQuery"
            @keyup.enter="onSearch"
            type="text"
            class="search-input"
            placeholder="Buscar animais (identificação)..."
          />
          <button class="button-primary" @click="onSearch">Buscar</button>
        </div>

        <section v-if="activeContent === 'home'" class="home-overview">
          <div class="welcome-section">
            <h2 class="welcome-title">Bem-vindo, {{ user.username || 'Usuário' }}!</h2> <p class="last-event">
              Última atividade:
              <strong>{{ lastActivity.description || 'Nenhuma atividade recente.' }}</strong>
              <span v-if="lastActivity.date"> em {{ lastActivity.date }}</span>
            </p>
          </div>
          <div class="stats-grid">
            <div class="stat-card" tabindex="0" @click="selectContent('animals')" @keydown.enter="selectContent('animals')">
              <h4>{{ stats.animals }}</h4>
              <p>Animais</p>
            </div>
            <div class="stat-card" tabindex="0" @click="selectContent('home')" @keydown.enter="selectContent('home')"> <h4>{{ stats.lots }}</h4>
              <p>Lotes/Grupos</p>
            </div>
            <div class="stat-card" tabindex="0" @click="selectContent('properties')" @keydown.enter="selectContent('properties')">
              <h4>{{ stats.properties }}</h4>
              <p>Propriedades</p>
            </div>
          </div>
        </section>

        <AnimalContent
          v-if="activeContent === 'animals'"
          :key="'animals_' + selectedAnimalId" :search-query-prop="selectedAnimalId" />
        <PropertyContent
          v-if="activeContent === 'properties'"
          :key="'properties_' + searchQuery"
          :search-query-prop="searchQuery"
        />
        <EventContent
          v-if="activeContent === 'events'"
          ref="eventComp"
        />
        <UserBlockchainRecords
          v-if="activeContent === 'userBlockchain'"
          :key="'userBlockchainRecords_' + user.id" />
      </main>
    </div>

    <AppFooter />

    <button
      class="sticky-new-event button-primary"
      @click="goToNewEvent"
      aria-label="Registrar novo evento"
      v-if="activeContent !== 'events'" 
    > + Novo Evento
    </button>

    <div v-if="showSearchModal" class="modal-overlay" @click.self="closeSearchModal">
      <div class="modal-content search-modal-content">
        <h3 class="modal-title">Resultados da Busca por "{{ displayedSearchQuery }}"</h3>
        <ul v-if="searchResults.length" class="modal-list">
          <li
            v-for="a in searchResults"
            :key="a.id"
            class="modal-list-item"
            @click="selectSearchResult(a)"
            tabindex="0"
            @keydown.enter="selectSearchResult(a)"
          >
            ID: {{ a.identification }} (Raça: {{a.breed_name || 'N/D' }})
          </li>
        </ul>
        <p v-else class="empty-state">Nenhum animal encontrado para "{{ displayedSearchQuery }}".</p>
        <button class="button-secondary" @click="closeSearchModal">Fechar</button> </div>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import AnimalContent from '@/components/AnimalContent.vue';
import PropertyContent from '@/components/PropertyContent.vue';
import EventContent from '@/components/EventContent.vue';
import UserBlockchainRecords from '@/components/UserBlockchainRecords.vue'; // IMPORTAR O NOVO COMPONENTE

import { getUserProfile } from '@/services/userService';
import { getAnimals } from '@/services/animalService'; // Apenas para stats e busca
import { getAnimalGroups } from '@/services/lookupService'; // Apenas para stats
import { getUserProperties } from '@/services/propertyService'; // Apenas para stats
// import { getEvents } from '@/services/eventService'; // Para lastEvent, se necessário

export default {
  name: 'DashboardPage',
  components: {
    AppHeader,
    AppFooter,
    AnimalContent,
    PropertyContent,
    EventContent,
    UserBlockchainRecords, // REGISTRAR O NOVO COMPONENTE
  },
  data() {
    return {
      user: { username: '', id: null }, // Adicionado id do usuário
      stats: { animals: 0, lots: 0, properties: 0, events: 0 },
      lastActivity: { description: '', date: '' },
      searchQuery: '',
      displayedSearchQuery: '', // Para mostrar no modal o termo que foi buscado
      searchResults: [],
      showSearchModal: false,
      selectedAnimalId: null, // Para passar como prop para AnimalContent após busca
      activeContent: 'home', // Conteúdo ativo padrão
    };
  },
  async mounted() {
    try {
      const profile = await getUserProfile();
      this.user = profile;

      // Carregar estatísticas
      // Envolve múltiplas chamadas, pode ser otimizado no backend com um endpoint de resumo
      const [animalsData, groupsData, propsData] = await Promise.all([
        getAnimals({ owner: profile.id, limit: 1000 }), // Assumindo que owner é o filtro, limit para evitar sobrecarga se muitos animais
        getAnimalGroups(), // Estes são grupos do usuário? Se sim, o backend deve filtrar.
        getUserProperties() // Já deve ser do usuário
        // getEvents({ recorded_by: profile.id, ordering: '-date', limit: 1 }) // Para buscar último evento
      ]);

      this.stats.animals = animalsData.length;
      this.stats.lots = groupsData.filter(g => g.owner === profile.id).length; // Filtra grupos pelo owner no frontend se necessário
      this.stats.properties = propsData.length;
      // this.stats.events = ... (se você tiver um endpoint para contar eventos)

      // Lógica para a última atividade (exemplo, pode ser melhorada)
      // if (eventsData && eventsData.length > 0) {
      //   const lastEv = eventsData[0];
      //   const animalForEvent = animalsData.find(a => a.id === lastEv.animal);
      //   this.lastActivity = {
      //     description: `Evento '${lastEv.event_type_name || 'Desconhecido'}' em ${animalForEvent ? animalForEvent.identification : 'Animal ID ' + lastEv.animal}`,
      //     date: new Date(lastEv.date).toLocaleDateString('pt-BR'),
      //   };
      // } else 
      if (animalsData.length > 0) {
        this.lastActivity = {
          description: `Total de ${animalsData.length} animais registrados.`,
          // date: new Date().toLocaleDateString('pt-BR') // Data da última atualização, ou do último animal
        };
      }

    } catch (err) {
      console.error('Erro ao carregar dados do dashboard:', err);
      // Tratar erro, talvez redirecionar para login se for erro de autenticação
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        this.$router.push('/login');
      }
    }
  },
  methods: {
    selectContent(tab) {
      this.activeContent = tab;
      this.searchQuery = ''; // Limpa busca ao trocar de aba
      this.selectedAnimalId = null; // Limpa animal selecionado
      if (tab !== 'home') {
        this.searchResults = []; // Limpa resultados da busca se não for a home
      }
    },
    goToNewEvent() {
      this.selectContent('events'); // Muda para a aba de eventos
      this.$nextTick(() => {
        if (this.$refs.eventComp && typeof this.$refs.eventComp.openModal === 'function') {
          this.$refs.eventComp.openModal(); // Chama o método para abrir o modal de novo evento
        } else {
            console.warn("Referência para EventContent ou método openModal não encontrado.");
        }
      });
    },
    async onSearch() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        // this.showSearchModal = false; // Opcional: fechar modal se busca vazia
        return;
      }
      this.displayedSearchQuery = this.searchQuery; // Guarda o termo buscado
      try {
        // A busca é apenas por identificação do animal
        const list = await getAnimals({ owner: this.user.id, identification__icontains: this.searchQuery.trim() });
        this.searchResults = list.map(a => ({
            ...a,
            breed_name: a.breed_name || 'N/D' // Adiciona nome da raça se disponível
        }));
        this.showSearchModal = true;
      } catch (error) {
        console.error("Erro na busca de animais:", error);
        alert("Erro ao buscar animais. Tente novamente.");
        this.searchResults = [];
        this.showSearchModal = false;
      }
    },
    selectSearchResult(animal) {
      this.showSearchModal = false;
      this.selectedAnimalId = animal.id; // Guarda o ID do animal
      this.searchQuery = animal.identification; // Opcional: preenche a barra de busca
      this.activeContent = 'animals'; // Muda para a aba de animais
      // O AnimalContent agora usará :search-query-prop="selectedAnimalId"
      // e precisará de lógica interna para carregar/filtrar por esse ID.
    },
    closeSearchModal() {
        this.showSearchModal = false;
        // this.searchQuery = ''; // Opcional: limpar query ao fechar modal
        // this.searchResults = [];
    }
  }
};
</script>

<style scoped>
/* Seus estilos existentes para .dashboard-page, .sidebar, .dashboard-content, etc. */
/* Adicionar :key ao AnimalContent, PropertyContent para forçar recriação/atualização
   quando a query de busca mudar. */

.dashboard-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Alterado para min-height */
}
.dashboard-body {
  display: flex;
  flex: 1;
  background: var(--color-bg-muted, #f4f6f8); /* Cor de fundo mais suave para o corpo */
  /* align-items: center; Removido para permitir que o conteúdo cresça */
}
/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--color-white, #FFFFFF);
  border-right: 1px solid var(--color-border, #e0e0e0);
  padding: var(--sp-lg, 1.5rem) 0;
  display: flex;
  flex-direction: column;
  /* justify-content: center; Removido para alinhar no topo */
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar nav li {
  margin: 0; /* Removido margin y */
}
.sidebar nav a {
  display: block;
  padding: var(--sp-md, 1rem) var(--sp-lg, 1.5rem); /* Aumentado padding */
  color: var(--color-text-secondary, #555); /* Cor mais suave */
  text-decoration: none;
  transition: background 0.2s, color 0.2s, transform 0.1s, border-left-color 0.2s;
  border-left: 4px solid transparent; /* Para indicar link ativo */
  font-weight: 500; /* Peso da fonte */
}
.sidebar nav a:hover {
  background-color: var(--color-bg-hover, #e9ecef); /* Fundo sutil no hover */
  color: var(--color-accent-dark, #0056b3); /* Cor de destaque mais escura */
  /* transform: translateX(4px); Removido transform */
}
.sidebar nav li.active-link > a {
  background: var(--color-accent-light, #e7f1ff); /* Fundo de destaque suave */
  color: var(--color-accent, #1A73E8); /* Cor de destaque */
  font-weight: 600; /* Mais destaque para o ativo */
  border-left-color: var(--color-accent, #1A73E8);
}
/* Main Content */
.dashboard-content {
  flex: 1;
  padding: var(--sp-lg, 1.5rem) var(--sp-xl, 2rem); /* Mais padding lateral */
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  /* justify-content: center; Removido */
}
.search-filter-group {
  width: 100%;
  max-width: 700px; /* Limitar largura da busca */
  display: flex;
  gap: var(--sp-md, 1rem);
  margin-bottom: var(--sp-xl, 2rem);
  align-items: center;
}
.search-input,
.filter-select {
  flex: 1;
  padding: var(--sp-sm, 0.75rem); /* Mais padding interno */
  border: 1px solid var(--color-border, #ced4da);
  border-radius: var(--sp-sm, 0.25rem);
  font-size: var(--fs-base, 1rem);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.search-input:focus,
.filter-select:focus {
  border-color: var(--color-primary, #007bff);
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25); /* Sombra de foco Bootstrap-like */
}
.filter-select {
  max-width: 200px;
}
/* Botão de Buscar */
.button-primary { /* Estilo padrão para botões primários */
  padding: var(--sp-sm, 0.75rem) var(--sp-lg, 1.5rem);
  background-color: var(--color-accent, #007bff);
  color: var(--color-white, #FFFFFF);
  border: 1px solid var(--color-accent, #007bff);
  border-radius: var(--sp-sm, 0.25rem);
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s, transform 0.1s;
  font-weight: 500;
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent-dark, #0056b3); /* Mais escuro no hover */
  border-color: var(--color-accent-dark, #0056b3);
  outline: none;
  transform: translateY(-1px); /* Leve elevação */
}
.button-secondary { /* Estilo para botões secundários */
    background-color: var(--color-bg-secondary, #6c757d);
    color: var(--color-white, #FFFFFF);
    border: 1px solid var(--color-bg-secondary, #6c757d);
}
.button-secondary:hover, .button-secondary:focus {
    background-color: #5a6268;
    border-color: #545b62;
}


/* Home Overview */
.home-overview {
  background: var(--color-white, #FFFFFF);
  padding: var(--sp-xl, 2rem); /* Mais padding */
  border-radius: var(--sp-md, 0.5rem); /* Borda mais arredondada */
  box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Sombra mais suave e difundida */
  margin-bottom: var(--sp-xl, 2rem);
}
.welcome-section {
  text-align: center;
  margin-bottom: var(--sp-xl, 2rem);
}
.welcome-title {
  font-family: var(--font-heading, serif);
  font-size: 2.25rem; /* Maior */
  color: var(--color-text-primary, #333);
  margin-bottom: var(--sp-sm, 0.5rem);
}
.last-event, .last-activity {
  font-size: var(--fs-base, 1rem);
  color: var(--color-text-secondary, #666);
  margin-bottom: var(--sp-lg, 1.5rem);
}
.stats-grid {
  display: grid; /* Usar grid para melhor responsividade */
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* Colunas responsivas */
  gap: var(--sp-lg, 1.5rem);
}
.stat-card {
  background: var(--color-white, #FFFFFF);
  border: 1px solid var(--color-border, #e0e0e0);
  border-radius: var(--sp-md, 0.5rem);
  padding: var(--sp-lg, 1.5rem); /* Mais padding interno */
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.stat-card:hover,
.stat-card:focus {
  box-shadow: 0 6px 20px rgba(0,0,0,0.1); /* Sombra maior no hover */
  transform: translateY(-6px); /* Elevação maior */
  outline: none;
}
.stat-card h4 {
  font-family: var(--font-body, sans-serif); /* Fonte do corpo para números */
  font-size: 2rem; /* Números maiores */
  font-weight: 600; /* Mais peso */
  margin-bottom: var(--sp-xs, 0.25rem);
  color: var(--color-accent, #1A73E8); /* Cor de destaque para números */
}
.stat-card p {
  font-size: var(--fs-base, 1rem); /* Texto maior */
  color: var(--color-text-secondary, #555);
  margin:0;
}
/* Sticky Button */
.sticky-new-event {
  position: fixed;
  bottom: var(--sp-xl, 2rem);
  right: var(--sp-xl, 2rem); /* Ajustado para sp-xl */
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0,123,255,0.3); /* Sombra mais pronunciada */
  width: auto; /* Permitir que o padding defina a largura */
  /* padding já definido em .button-primary */
}
.sticky-new-event:hover,
.sticky-new-event:focus {
  transform: scale(1.05); /* Um pouco menos de scale */
  box-shadow: 0 6px 16px rgba(0,123,255,0.4);
}
/* Modal Overlay & Content (para busca) */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6); /* Overlay mais escuro */
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.search-modal-content { /* Classe específica para o modal de busca */
  background-color: var(--color-white, #ffffff);
  padding: var(--sp-lg, 1.5rem);
  border-radius: var(--sp-md, 0.5rem);
  width: 90%;
  max-width: 500px; /* Aumentado um pouco */
  text-align: left; /* Alinhar à esquerda */
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.modal-title { /* Estilo compartilhado de título de modal */
  font-family: var(--font-heading, serif);
  color: var(--color-text-primary, #333);
  margin-bottom: var(--sp-lg, 1.5rem);
  font-size: 1.5rem; /* Tamanho de título */
  text-align: center;
}
.modal-list {
  list-style: none;
  padding: 0;
  margin-bottom: var(--sp-lg, 1.5rem);
  max-height: 300px; /* Mais altura para a lista */
  overflow-y: auto;
}
.modal-list-item {
  padding: var(--sp-sm, 0.75rem); /* Mais padding */
  border-bottom: 1px solid var(--color-border-light, #f0f0f0);
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: var(--sp-xs, 0.25rem);
}
.modal-list-item:last-child {
    border-bottom: none;
}
.modal-list-item:hover {
  background: var(--color-bg-hover, #e9ecef);
}
@media (max-width: 768px) {
  .dashboard-body {
    flex-direction: column;
    align-items: stretch;
  }
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--color-border, #e0e0e0);
    padding: var(--sp-md, 1rem) 0; /* Menos padding no mobile */
  }
  .sidebar nav a {
      padding: var(--sp-sm, 0.75rem) var(--sp-md, 1rem);
  }
  .dashboard-content {
      padding: var(--sp-md, 1rem);
  }
  .search-filter-group {
    flex-direction: column;
    gap: var(--sp-sm, 0.5rem); /* Menor gap */
  }
  .search-input, .filter-select, .search-filter-group > .button-primary {
      width: 100%; /* Ocupar largura total */
      max-width: none;
  }
  .stats-grid {
    grid-template-columns: 1fr; /* Uma coluna no mobile */
  }
  .sticky-new-event {
      bottom: var(--sp-md, 1rem);
      right: var(--sp-md, 1rem);
  }
  .search-modal-content {
      max-width: 90%;
  }
}
</style>