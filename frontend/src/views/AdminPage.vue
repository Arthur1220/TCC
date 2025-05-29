<template>
  <div class="admin-page-wrapper">
    <AppHeader />

    <div class="admin-body">
      <aside class="sidebar admin-sidebar">
        <nav aria-label="Admin Navigation">
          <ul>
            <li :class="{ 'active-link': activeSection === 'overview' }">
              <a href="#" @click.prevent="selectSection('overview')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                Visão Geral
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'carteira' }">
              <a href="#" @click.prevent="selectSection('carteira')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
                Gerenciar Carteiras
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'pause' }">
              <a href="#" @click.prevent="selectSection('pause')">
                <svg v-if="contractActive" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M8 5v14l11-7z"/></svg>
                {{ contractActive ? 'Pausar Contrato' : 'Ativar Contrato' }}
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'events' }">
              <a href="#" @click.prevent="selectSection('events')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7v-5z"/></svg>
                Visualizar Eventos
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'blockchain' }">
              <a href="#" @click.prevent="selectSection('blockchain')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M16.53 11.06L15.47 10l-4.88 4.88-2.12-2.12-1.06 1.06L10.59 17l5.94-5.94zM19 3h-4.18C14.4 1.84 13.3 1 12 1s-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7-.25c.41 0 .75.34.75.75s-.34.75-.75.75-.75-.34-.75-.75.34-.75.75-.75zM19 19H5V5h14v14z"/></svg>
                Auditoria Blockchain
              </a>
            </li>
            <li :class="{ 'active-link': activeSection === 'users' }">
              <a href="#" @click.prevent="selectSection('users')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
                Gerenciar Usuários
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <main class="admin-main-content">
        <div v-if="isLoadingAdminData" class="loading-state admin-loading">
            <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
            <p>Carregando dados da administração...</p>
        </div>
        <div v-else>
            <section v-if="activeSection === 'overview'" class="content-panel admin-overview-panel">
            <div class="welcome-admin-section">
                <h1 class="welcome-title">Bem-vindo(a) à Área Administrativa, {{ user.username || 'Admin' }}!</h1>
                <p class="page-subtitle">Aqui você tem o controle total sobre a plataforma AnimalTracking.</p>
            </div>

            <h2 class="section-title-global admin-section-title">Visão Geral do Sistema</h2>
            <div class="stats-grid admin-stats-grid">
                <div class="stat-card card">
                <span class="stat-icon">🐾</span>
                <h3 class="stat-value">{{ stats.animals }}</h3>
                <p class="stat-label">Total de Animais</p>
                </div>
                <div class="stat-card card">
                <span class="stat-icon">📄</span>
                <h3 class="stat-value">{{ stats.events === 'Calculando...' ? stats.events : (stats.events || 0) }}</h3>
                <p class="stat-label">Total de Eventos Registrados</p>
                </div>
                <div class="stat-card card">
                <span class="stat-icon">{{ contractActive ? '✅' : '⏸️' }}</span>
                <h3 :class="['stat-value', contractActive ? 'status-active-text' : 'status-paused-text']">
                    {{ contractActive ? 'Ativo' : 'Pausado' }}
                </h3>
                <p class="stat-label">Status do Contrato</p>
                </div>
            </div>
            </section>

            <section v-else-if="activeSection === 'carteira'" class="content-panel form-section-panel">
            <h2 class="section-title-global admin-section-title">Gerenciar Carteiras da Plataforma</h2>
            <div class="wallet-controls">
                <AddWallet class="wallet-control-item"/>
                <RemoveWallet class="wallet-control-item"/>
            </div>
            </section>

            <section v-else-if="activeSection === 'pause'" class="content-panel form-section-panel">
            <PauseContract
                :isActive="contractActive"
                @update:active="handleContractStatusUpdate"
            />
            </section>

            <VisualizacaoContent v-else-if="activeSection === 'events'" />
            <BlockchainViewer v-else-if="activeSection === 'blockchain'" mode="admin" />
            <RoleManager v-else-if="activeSection === 'users'" />
        </div>
      </main>
    </div>

    <AppFooter />
    <NotificationModal
      :show="notification.show"
      :title="notification.title"
      :message="notification.message"
      :type="notification.type"
      @close="closeNotification"
    />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';
import NotificationModal from '@/components/NotificationModal.vue';

// Presumindo que os componentes admin estão em uma subpasta para organização
import AddWallet from '@/components/AddWallet.vue';
import RemoveWallet from '@/components/RemoveWallet.vue';
import VisualizacaoContent from '@/components/VisualizacaoContent.vue'; // Este deve ser o Visualizador GERAL de Eventos
import PauseContract from '@/components/PauseContract.vue';
import RoleManager from '@/components/RoleManager.vue';
import BlockchainViewer from '@/components/BlockchainViewer.vue'; // Este deve ser o Visualizador GERAL da Blockchain

import { getUserProfile } from '@/services/userService';
import { getAnimals } from '@/services/animalService'; // Usar um método que busca TODOS os animais para admin
import { getEvents } from '@/services/eventService'; // Usar um método que busca TODOS os eventos para admin
import { checkContractStatus } from '@/services/contractService';

export default {
  name: 'AdminPage',
  components: {
    AppHeader,
    AppFooter,
    NotificationModal,
    AddWallet,
    RemoveWallet,
    VisualizacaoContent,
    PauseContract,
    RoleManager,
    BlockchainViewer
  },
  data() {
    return {
      user: { username: '' },
      stats: { animals: 0, events: 'Carregando...' }, // Inicia events como string
      contractActive: false,
      activeSection: 'overview',
      isLoadingAdminData: true, // Novo estado de carregamento para dados da página
      notification: { show: false, title: '', message: '', type: 'success' },
    };
  },
  async mounted() {
    await this.loadAdminData();
  },
  methods: {
    showAppNotification(title, message, type = 'success', duration = 4000) {
      this.notification.title = title;
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      if (duration) {
        setTimeout(() => { this.notification.show = false; }, duration);
      }
    },
    closeNotification() {
        this.notification.show = false;
    },
    async loadAdminData() {
        this.isLoadingAdminData = true;
        this.showAppNotification("Admin", "Carregando dados administrativos...", "info", null);
        try {
            const profilePromise = getUserProfile();
            // Para admin, assumimos que o backend tem endpoints que retornam TODOS os dados
            // ou que o serviço pode ser chamado com um parâmetro especial.
            const animalsPromise = getAnimals({ all: true }); // Exemplo: buscar todos os animais
            const eventsPromise = getEvents({ all: true });   // Exemplo: buscar todos os eventos
            const contractStatusPromise = checkContractStatus();

            const [profileResponse, animalsResponse, eventsResponse, contractStatusResponse] = await Promise.allSettled([
                profilePromise,
                animalsPromise,
                eventsPromise,
                contractStatusPromise
            ]);

            if (profileResponse.status === 'fulfilled') {
                this.user = profileResponse.value || { username: 'Admin' };
            } else {
                this.user = { username: 'Admin (Perfil N/A)' };
                this.showAppNotification('Perfil Admin', 'Não foi possível carregar o perfil do administrador.', 'warning');
            }

            if (animalsResponse.status === 'fulfilled') {
                this.stats.animals = animalsResponse.value.length;
            } else {
                this.showAppNotification('Animais', 'Erro ao carregar total de animais.', 'error');
            }

            if (eventsResponse.status === 'fulfilled') {
                this.stats.events = eventsResponse.value.length;
            } else {
                this.stats.events = 'Erro';
                this.showAppNotification('Eventos', 'Erro ao carregar total de eventos.', 'error');
            }

            if (contractStatusResponse.status === 'fulfilled') {
                this.contractActive = contractStatusResponse.value.active;
            } else {
                this.showAppNotification('Contrato', 'Erro ao verificar status do contrato.', 'error');
            }
            
        } catch (err) {
            console.error('Erro geral ao carregar dados do admin:', err);
            this.showAppNotification('Erro Crítico', 'Erro geral ao carregar dados administrativos.', 'error');
        } finally {
            this.isLoadingAdminData = false;
            this.closeNotification(); // Esconde a notificação de "Carregando..."
        }
    },
    selectSection(section) {
      this.activeSection = section;
      if (section === 'pause' || section === 'overview') {
          this.refreshContractStatus();
      }
    },
    async refreshContractStatus() {
        try {
            const { active = false } = await checkContractStatus();
            this.contractActive = active;
        } catch (e) {
             console.warn('Falha ao atualizar status do contrato em refreshContractStatus:', e);
        }
    },
    async handleContractStatusUpdate(newStatus) {
        this.contractActive = newStatus;
        this.showAppNotification('Status do Contrato', `Contrato ${newStatus ? 'ATIVADO' : 'PAUSADO'} com sucesso.`, 'success');
    }
  }
};
</script>

<style scoped>
/* Estilos Globais e Variáveis CSS são aplicados */
.admin-page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 130vh;
  background-color: var(--color-bg-body);
}

.admin-body {
  display: flex;
  flex: 1;
  overflow: hidden; /* Para scroll individual de sidebar e content */
}

/* Sidebar Admin (Estilos da DashboardPage aplicados aqui com ajustes) */
.admin-sidebar {
  width: 260px;
  background: var(--color-bg-component);
  border-right: var(--border-width) solid var(--color-border);
  padding: var(--sp-lg) 0;
  flex-shrink: 0;
  overflow-y: auto;
}
.admin-sidebar nav ul { list-style: none; padding: 0; margin: 0; }
.admin-sidebar nav li { margin: 0; }
.admin-sidebar nav a {
  display: flex;
  align-items: center;
  gap: var(--sp-md);
  padding: var(--sp-md) var(--sp-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: var(--transition-base);
  border-left: 4px solid transparent;
  font-weight: var(--fw-medium);
}
.admin-sidebar nav a svg {
    flex-shrink: 0;
    color: var(--color-text-muted);
    transition: color var(--transition-fast);
    width: 20px; height: 20px;
}
.admin-sidebar nav a:hover, .admin-sidebar nav a:focus {
  background-color: var(--color-bg-hover);
  color: var(--color-primary);
  border-left-color: var(--color-primary-light);
}
.admin-sidebar nav a:hover svg, .admin-sidebar nav a:focus svg { color: var(--color-primary); }
.admin-sidebar nav li.active-link > a {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: var(--fw-semibold);
  border-left-color: var(--color-primary);
}
.admin-sidebar nav li.active-link > a svg { color: var(--color-primary); }


/* Conteúdo Principal Admin */
.admin-main-content {
  flex: 1;
  padding: var(--sp-lg) var(--sp-xl);
  overflow-y: auto;
}

/* Seção de Boas-vindas */
.welcome-admin-section {
  text-align: center;
  margin-bottom: var(--sp-xl); /* Espaço antes do título "Visão Geral" */
  padding: var(--sp-lg) var(--sp-md);
  background-color: var(--color-bg-component);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
}
.welcome-admin-section .welcome-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h1);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-xs);
}
.welcome-admin-section .page-subtitle {
  font-size: var(--fs-large);
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

/* Título de Seção Global */
.section-title-global.admin-section-title { /* Classe específica para admin se precisar de variação */
  font-family: var(--font-heading);
  font-size: var(--fs-h3); /* Títulos de seção H3 para admin */
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--sp-lg);
  padding-bottom: var(--sp-sm);
  border-bottom: 2px solid var(--color-primary); /* Linha de destaque abaixo do título */
  display: inline-block; /* Para que a borda não ocupe toda a largura */
}
/* Remover o ::after se o border-bottom já cumpre a função visual */
/* .section-title-global.admin-section-title::after { display: none; } */


/* Grid de Estatísticas */
.stats-grid.admin-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--sp-lg);
}
.stat-card.card { /* Herda de .card global */
  text-align: center;
  padding: var(--sp-lg);
}
.stat-icon {
  font-size: 2.8rem; /* Ícones emoji/SVG maiores */
  display: block;
  margin-bottom: var(--sp-md); /* Mais espaço */
  color: var(--color-primary);
}
.stat-card .stat-value {
  font-family: var(--font-body);
  font-size: var(--fs-h2); /* Números grandes */
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-xs);
  line-height: 1.1;
}
.stat-card .stat-label {
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
  margin: 0;
}
.stat-card .status-active-text { color: var(--color-success); }
.stat-card .status-paused-text { color: var(--color-warning); color: var(--color-text-primary); /* Texto escuro para fundo amarelo */ }

/* Seções de Conteúdo/Formulário */
.form-section-panel .section-title-global,
.content-section .section-title-global {
  text-align: left; /* Títulos de seção à esquerda dentro dos cards */
  border-bottom: none; /* Remove borda inferior do section-title-global aqui */
  padding-bottom: 0;
  margin-bottom: var(--sp-md); /* Ajuste de margem */
}
.form-section-panel .section-title-global::after {
    display: none; /* Remove sublinhado decorativo para títulos à esquerda */
}


.wallet-controls {
  display: grid; /* Usar grid para melhor controle */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Colunas responsivas */
  gap: var(--sp-lg);
}

/* Estado de Carregamento da Página Admin */
.loading-state.admin-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px; /* Altura mínima para o loader */
    color: var(--color-text-muted);
}
.loading-state.admin-loading .spinner {
    width: 60px;
    height: 60px;
    margin-bottom: var(--sp-md);
}
.loading-state.admin-loading p {
    font-size: var(--fs-large);
}


/* Responsividade */
@media (max-width: 992px) {
    .admin-body { flex-direction: column; }
    .admin-sidebar {
        width: 100%; border-right: none; border-bottom: var(--border-width) solid var(--color-border);
        padding: var(--sp-sm) 0; overflow-y: hidden;
    }
    .admin-sidebar nav ul {
        display: flex; overflow-x: auto; padding: 0 var(--sp-sm); justify-content: flex-start;
        -ms-overflow-style: none; scrollbar-width: none;
    }
    .admin-sidebar nav ul::-webkit-scrollbar { display: none; }
    .admin-sidebar nav li { flex-shrink: 0; }
    .admin-sidebar nav a {
        padding: var(--sp-sm) var(--sp-md); border-left: none; border-bottom: 4px solid transparent; white-space: nowrap;
    }
    .admin-sidebar nav li.active-link > a { border-left-color: transparent; border-bottom-color: var(--color-primary); }
    .admin-main-content { padding: var(--sp-md); }
    .welcome-admin-section .welcome-title { font-size: var(--fs-h2); }
}

@media (max-width: 576px) {
    .stats-grid.admin-stats-grid { grid-template-columns: 1fr; }
    .wallet-controls { grid-template-columns: 1fr; } /* Empilha os controles de carteira */
    .section-title-global.admin-section-title { font-size: var(--fs-h4); }
}
</style>