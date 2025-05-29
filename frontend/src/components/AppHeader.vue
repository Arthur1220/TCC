<template>
  <div>
    <header class="header" role="banner">
      <div class="header-container container">
        <h1 class="logo" tabindex="0" @click="goHome" @keydown.enter="goHome">AnimalTracking</h1>
        <nav class="nav" aria-label="Main navigation">
          <ul class="nav-list">
            <li v-for="link in navLinks" :key="link.id">
              <a @click.prevent="handleLink(link)"
                 :class="{ active: activeSection === link.id }"
                 tabindex="0">
                {{ link.label }}
              </a>
            </li>
            <template v-if="isAuthenticated">
              <li v-if="showUserDashboardLink">
                <a @click.prevent="navigateTo('/dashboard')" class="button button-outline-primary button-sm nav-dashboard-link" tabindex="0">Dashboard</a>
              </li>
              <li v-if="showAdminPageLink">
                <a @click.prevent="navigateTo('/admin')" class="button button-outline-primary button-sm nav-dashboard-link admin-page-link" tabindex="0">Admin Page</a>
              </li>
            </template>
          </ul>
        </nav>

        <div class="user-icon-wrapper" ref="userMenuWrapper">
          <img
            src="https://img.icons8.com/ios-glyphs/30/000000/user--v1.png"
            alt="Menu de usuário"
            tabindex="0"
            @click.stop="onUserIconClick" @keydown.enter.prevent="onUserIconClick"
            class="user-avatar-icon"
          />
          <ul v-if="showMenu" class="user-menu card" @click.stop>
            <li v-if="isAuthenticated && userProfile.username" class="user-menu-greeting">
                Olá, {{ userProfile.username }}
            </li>
            <li v-if="isAuthenticated" tabindex="0" @click="triggerOpenUserModal('profile')">Perfil</li>
            <li v-if="isAuthenticated" tabindex="0" @click="triggerOpenUserModal('settings')">Configurações</li>
            <li v-if="isAuthenticated" tabindex="0" @click="triggerLogout">Sair</li>
            </ul>
        </div>
      </div>
    </header>

    <div v-if="showUserModal" class="modal-overlay" @click.self="closeUserModal">
      <div class="modal-content card">
        <div class="modal-header">
            <h3 class="modal-title-text">Minha Conta</h3>
            <button @click="closeUserModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <div class="modal-tabs">
          <button
            class="modal-tab"
            :class="{ active: activeModalTab === 'profile' }"
            @click="switchTab('profile')"
          >Perfil</button>
          <button
            class="modal-tab"
            :class="{ active: activeModalTab === 'settings' }"
            @click="switchTab('settings')"
          >Configurações</button>
        </div>

        <div v-if="activeModalTab === 'profile'" class="modal-body">
          <div v-if="!editMode" class="profile-view">
            <p><strong>Usuário:</strong> {{ userProfile.username }}</p>
            <p><strong>Nome:</strong> {{ userProfile.first_name }} {{ userProfile.last_name }}</p>
            <p><strong>E-mail:</strong> {{ userProfile.email }}</p>
            <p><strong>Telefone:</strong> {{ userProfile.phone || 'Não informado' }}</p>
            <p v-if="currentUserRoleNames.length"> <strong>Função(ões):</strong> {{ currentUserRoleNames.join(', ') }}</p>
            <div class="modal-actions form-actions">
              <button class="button button-primary" @click="editMode = true">Editar Perfil</button>
              <button class="button button-secondary" @click="closeUserModal" style="margin-left: auto;">Fechar</button>
            </div>
          </div>
          <form v-else @submit.prevent="submitProfile" class="modal-form">
            <div class="form-group">
              <label for="username" class="form-label">Usuário</label>
              <input id="username" v-model="profileForm.username" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="first_name" class="form-label">Nome</label>
              <input id="first_name" v-model="profileForm.first_name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="last_name" class="form-label">Sobrenome</label>
              <input id="last_name" v-model="profileForm.last_name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="email" class="form-label">E-mail</label>
              <input id="email" v-model="profileForm.email" type="email" class="input" required />
            </div>
            <div class="form-group">
              <label for="phone" class="form-label">Telefone</label>
              <input id="phone" v-model="profileForm.phone" type="text" class="input" />
            </div>
            <div class="modal-actions form-actions">
              <button type="submit" class="button button-primary">Salvar Alterações</button>
              <button type="button" class="button button-secondary" @click="cancelEdit">Cancelar Edição</button>
            </div>
          </form>
        </div>

        <div v-if="activeModalTab === 'settings'" class="modal-body">
          <p>Preferências do sistema e outras configurações estarão disponíveis aqui.</p>
           <div class="modal-actions form-actions">
              <button class="button button-secondary" @click="closeUserModal" style="margin-left: auto;">Fechar</button>
            </div>
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
import { getUserProfile, updateUserProfile } from '@/services/userService';
import { logout as userLogout } from '@/services/authService';
import NotificationModal from '@/components/NotificationModal.vue';
import { ROLE_ID_MAP } from '@/utils/constants';

export default {
  name: 'AppHeader',
  components: {
    NotificationModal
  },
  data() {
    return {
      navLinks: [
        { id: 'benefits', label: 'Benefícios', href: '#benefits' },
        { id: 'details', label: 'Como Funciona', href: '#details' },
        { id: 'plans', label: 'Cobrança', href: '#plans' },
        { id: 'faq', label: 'FAQ', href: '#faq' },
        { id: 'auditoria', label: 'Auditoria', href: '/search-blockchain' }
      ],
      activeSection: '',
      showMenu: false, // RESTAURADO: Controla a visibilidade do menu dropdown
      isAuthenticated: false,
      userProfile: {},
      showUserModal: false,
      activeModalTab: 'profile',
      editMode: false,
      profileForm: { username: '', first_name: '', last_name: '', email: '', phone: '' },
      observer: null,
      notification: {
        show: false,
        message: '',
        type: 'success'
      }
    };
  },
  computed: {
    userRoles() {
      if (!this.isAuthenticated || !this.userProfile.roles || !Array.isArray(this.userProfile.roles)) {
        return [];
      }
      return this.userProfile.roles
        .map(userRoleObject => ROLE_ID_MAP[userRoleObject.role])
        .filter(name => name); // Filtra quaisquer nomes undefined
    },
    currentUserRoleNames() {
      // Esta propriedade computada é usada apenas para exibir os nomes no perfil, pode continuar
      if (!this.userRoles.length) return [];
      return this.userRoles.map(name => name.charAt(0).toUpperCase() + name.slice(1));
    },
    showUserDashboardLink() {
      if (!this.isAuthenticated) return false;
      // Mostra o botão do Dashboard APENAS se o perfil for 'Usuário'
      return this.userRoles.includes('Usuário');
    },
    showAdminPageLink() {
      if (!this.isAuthenticated) return false;
      // Mostra o botão da Admin Page se o perfil for 'Administrador' OU 'Gerente'
      return this.userRoles.includes('Administrador') || this.userRoles.includes('Gerente');
    }
  },
  methods: {
    showAppNotification(message, type = 'success') {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
    },
    closeNotification() {
        this.notification.show = false;
    },
    goHome() {
      this.$router.push('/');
      this.activeSection = '';
      this.showMenu = false; // Fecha o menu ao ir para home
    },
    navigateTo(path) {
      this.showMenu = false; // Fecha o menu ao navegar
      this.closeUserModal();
      if (this.$route.path !== path) {
        this.$router.push(path).catch(err => {
            if (err.name !== 'NavigationDuplicated' && err.name !== ' selben Navigations-Guard mehrmals') {
                console.error('Erro de navegação:', err);
            }
        });
      }
    },
    handleLink(link) {
      this.showMenu = false; // Fecha o menu
      if (link.href.startsWith('#')) {
        if (this.$route.path === '/') {
            this.scrollToSection(link.id);
        } else {
            this.$router.push({ path: '/', hash: link.href })
              .then(() => this.scrollToSection(link.id));
        }
      } else {
        this.navigateTo(link.href);
      }
    },
    onUserIconClick() { // RESTAURADO: Alterna o menu dropdown
      if (!this.isAuthenticated) {
        this.navigateTo('/login');
      } else {
        this.showMenu = !this.showMenu; // Alterna a visibilidade do menu dropdown
      }
    },
    handleDocumentClick(e) { // RESTAURADO: Fecha o menu se clicar fora
      if (this.showMenu && this.$refs.userMenuWrapper && !this.$refs.userMenuWrapper.contains(e.target)) {
        this.showMenu = false;
      }
    },
    async fetchUserProfile() {
        try {
            const profile = await getUserProfile();
            this.userProfile = profile;
            this.isAuthenticated = true;
            if (!this.editMode) {
                this.profileForm = { 
                    username: profile.username || '',
                    first_name: profile.first_name || '',
                    last_name: profile.last_name || '',
                    email: profile.email || '',
                    phone: profile.phone || ''
                };
            }
        } catch (error) {
            console.warn('Usuário não autenticado ou erro ao buscar perfil:', error.response?.data || error);
            this.isAuthenticated = false;
            this.userProfile = {};
        }
    },
    triggerOpenUserModal(tab = 'profile') { // NOVO: Chamado pelos itens do menu
        this.showMenu = false; // Fecha o menu dropdown
        this.openUserModal(tab);
    },
    triggerLogout() { // NOVO: Chamado pelo item "Sair" do menu
        this.showMenu = false; // Fecha o menu dropdown
        this.onLogout();
    },
    openUserModal(tab = 'profile') {
      if (!this.isAuthenticated) return;
      // this.showMenu = false; // Já tratado em triggerOpenUserModal
      this.activeModalTab = tab;
      this.editMode = false;
      this.profileForm = { 
        username: this.userProfile.username || '',
        first_name: this.userProfile.first_name || '',
        last_name: this.userProfile.last_name || '',
        email: this.userProfile.email || '',
        phone: this.userProfile.phone || ''
      };
      this.showUserModal = true;
    },
    closeUserModal() {
      this.showUserModal = false;
      this.editMode = false;
    },
    switchTab(tab) {
      this.activeModalTab = tab;
      this.editMode = false; 
    },
    cancelEdit() {
      this.editMode = false;
      this.profileForm = { 
        username: this.userProfile.username || '',
        first_name: this.userProfile.first_name || '',
        last_name: this.userProfile.last_name || '',
        email: this.userProfile.email || '',
        phone: this.userProfile.phone || ''
      };
    },
    async submitProfile() {
      try {
        const updatedProfileData = { ...this.profileForm };
        if (this.userProfile.username === updatedProfileData.username) {
            delete updatedProfileData.username;
        }
        const updated = await updateUserProfile(this.userProfile.id, updatedProfileData);
        this.userProfile = { ...this.userProfile, ...updated }; 
        this.profileForm = { ...this.userProfile };
        this.editMode = false;
        this.showAppNotification('Perfil atualizado com sucesso!', 'success');
      } catch (error) {
        console.error('Erro ao salvar perfil:', error.response?.data || error);
        let errorMessage = 'Erro ao salvar perfil.';
        if (error.response && error.response.data) {
            const errors = error.response.data;
             if (typeof errors === 'object' && errors !== null) {
                 errorMessage += ' Detalhes: ' + Object.entries(errors)
                    .map(([key, value]) => `${key}: ${typeof value === 'object' ? JSON.stringify(value) : (Array.isArray(value) ? value.join(', ') : value)}`)
                    .join('; ');
            } else if (typeof errors === 'string') {
                errorMessage += ' ' + errors;
            }
        }
        this.showAppNotification(errorMessage, 'error');
      }
    },
    async onLogout() { // Este método agora é chamado por triggerLogout
      try {
        await userLogout();
      } catch (error) {
        console.error('Erro no logout no servidor, limpando localmente:', error);
      } finally {
        this.isAuthenticated = false;
        this.userProfile = {};
        this.closeUserModal();
        if (this.$route.path !== '/') {
            this.navigateTo('/');
        } else {
            window.location.reload();
        }
      }
    },
    scrollToSection(id) {
      this.$nextTick(() => {
        const el = document.getElementById(id);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
          console.warn(`Elemento com ID '${id}' não encontrado para scroll.`);
        }
      });
    },
    initObserver() {
      if (this.observer) {
        this.observer.disconnect();
      }
      if (this.$route.path !== '/') {
        this.activeSection = '';
        return;
      }
      const ids = this.navLinks.filter(link => typeof link.href === 'string' && link.href.startsWith('#')).map(link => link.id);
      const sections = ids.map(id => document.getElementById(id)).filter(el => el !== null);

      if (sections.length === 0) return;

      this.observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.activeSection = entry.target.id;
          }
        });
      }, { threshold: 0.5, rootMargin: "-50% 0px -50% 0px" });

      sections.forEach(section => this.observer.observe(section));
    }
  },
  watch: {
    '$route'() {
      this.initObserver();
      this.showMenu = false; // RESTAURADO: Fecha o menu ao mudar de rota
      this.closeUserModal();
    },
    isAuthenticated(newVal, oldVal) {
        if (newVal && (!this.userProfile || Object.keys(this.userProfile).length === 0)) {
            this.fetchUserProfile();
        } else if (!newVal && oldVal) {
            this.userProfile = {};
        }
    }
  },
  mounted() {
    this.fetchUserProfile();
    document.addEventListener('click', this.handleDocumentClick); // RESTAURADO
    this.initObserver();
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleDocumentClick); // RESTAURADO
    if (this.observer) {
      this.observer.disconnect();
    }
  }
};
</script>

<style scoped>
/* ... (Estilos anteriores, incluindo os do header, logo, nav-list, user-avatar-icon, modal, etc.) ... */
/* Certifique-se que os estilos para .user-menu (o dropdown) e o cursor dos links de navegação estejam corretos. */

.header {
  background: var(--color-bg-component);
  backdrop-filter: blur(10px);
  border-bottom: var(--border-width) solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: var(--zindex-sticky);
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--sp-sm);
  padding-bottom: var(--sp-sm);
}

.logo {
  font-family: var(--font-heading);
  font-size: var(--fs-h2); /* Destaque do logo */
  color: var(--color-primary); /* Destaque do logo */
  font-weight: var(--fw-bold); /* Destaque do logo */
  cursor: pointer;
  transition: var(--transition-fast);
  text-decoration: none;
}
.logo:hover, .logo:focus {
  color: var(--color-primary-dark);
  text-decoration: none;
}

.nav-list {
  display: flex;
  list-style: none;
  gap: var(--sp-md);
  align-items: center;
}
.nav-list a {
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: var(--transition-fast);
  padding: var(--sp-xs) var(--sp-sm);
  border-radius: var(--border-radius-sm);
  font-weight: var(--fw-medium);
  cursor: pointer; /* CORREÇÃO: Cursor pointer para os links de navegação */
}
.nav-list a:hover,
.nav-list a:focus,
.nav-list a.active {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.nav-dashboard-link {
  padding-top: calc(var(--sp-xs) * 0.8);
  padding-bottom: calc(var(--sp-xs) * 0.8);
  font-size: var(--fs-small);
  margin-left: var(--sp-sm);
}

.user-icon-wrapper {
  position: relative;
}
.user-avatar-icon {
  width: calc(var(--sp-lg) + var(--sp-xs));
  height: calc(var(--sp-lg) + var(--sp-xs));
  cursor: pointer;
  border-radius: var(--border-radius-pill);
  padding: var(--sp-xxs);
  transition: var(--transition-fast);
  background-color: var(--color-bg-muted);
}
.user-avatar-icon:hover, .user-avatar-icon:focus {
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

/* Estilos para .user-menu (o dropdown) RESTAURADOS e usando variáveis globais */
.user-menu {
  /* A classe .card global já define background, border, border-radius, box-shadow */
  position: absolute;
  top: calc(100% + var(--sp-xs)); 
  right: 0;
  list-style: none;
  padding: var(--sp-xs) 0; 
  margin: 0;
  min-width: 200px; 
  z-index: var(--zindex-dropdown);
  /* Os estilos de .card do style.css global serão aplicados aqui se .card estiver no elemento <ul> */
}
.user-menu-greeting {
  padding: var(--sp-sm) var(--sp-md);
  font-weight: var(--fw-semibold);
  color: var(--color-text-muted);
  display: block;
  border-bottom: var(--border-width) solid var(--color-border-light);
  margin-bottom: var(--sp-xs);
  cursor: default;
}
.user-menu li {
  padding: var(--sp-sm) var(--sp-md);
  cursor: pointer;
  transition: var(--transition-fast);
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
}
.user-menu li:not(.user-menu-greeting):hover,
.user-menu li:not(.user-menu-greeting):focus {
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
}

/* Modal */
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
    background: none;
    border: none;
    font-size: var(--fs-large);
    color: var(--color-text-muted);
    cursor: pointer;
    padding: var(--sp-xs);
    line-height: 1;
}
.button-close:hover, .button-close:focus {
    color: var(--color-text-primary);
}

.modal-tabs {
  display: flex;
  border-bottom: var(--border-width) solid var(--color-border);
  margin-bottom: var(--sp-md);
}
.modal-tab {
  flex: 1;
  padding: var(--sp-sm) var(--sp-xs);
  text-align: center;
  cursor: pointer;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  font-family: var(--font-body);
  font-weight: var(--fw-medium);
  color: var(--color-text-muted);
  transition: var(--transition-fast);
  margin-bottom: -1px; /* Ajuste para borda ativa */
}
.modal-tab.active {
  border-bottom-color: var(--color-primary);
  color: var(--color-primary);
  font-weight: var(--fw-semibold);
}
.modal-tab:not(.active):hover, .modal-tab:not(.active):focus {
  color: var(--color-text-primary);
  border-bottom-color: var(--color-border);
}

.modal-body {
  max-height: 70vh;
  overflow-y: auto;
  padding: var(--sp-xs);
}

.profile-view p {
  margin-bottom: var(--sp-sm);
  line-height: var(--lh-base);
}
.profile-view p strong {
  color: var(--color-text-primary);
  font-weight: var(--fw-medium);
}

</style>