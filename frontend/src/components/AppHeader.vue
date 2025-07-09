<template>
  <div>
    <header class="header" role="banner">
      <div class="header-container container">
        <h1 class="logo" tabindex="0" @click="goHome" @keydown.enter="goHome">AnimalTracking</h1>

        <button
          class="hamburger-menu-button"
          @click="toggleMobileMenu"
          :aria-expanded="isMobileMenuOpen.toString()"
          aria-label="Abrir menu de navegação"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28">
            <path d="M3 4h18v2H3V4zm0 7h18v2H3v-2zm0 7h18v2H3v-2z"/>
          </svg>
        </button>

        <nav class="nav" :class="{ 'is-open': isMobileMenuOpen }" aria-label="Main navigation">
          <button
            class="close-menu-button"
            @click="toggleMobileMenu"
            aria-label="Fechar menu de navegação"
          >
             &times;
          </button>

          <ul class="nav-list">
            <li v-for="link in navLinks" :key="link.id">
              <a @click.prevent="handleLink(link)" :class="{ active: activeSection === link.id }" tabindex="0">
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
                <button type="button" class="button button-secondary" @click="cancelEdit">Cancelar</button>
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
      isMobileMenuOpen: false,
      navLinks: [
        { id: 'benefits', label: 'Benefícios', href: '#benefits' },
        { id: 'details', label: 'Como Funciona', href: '#details' },
        { id: 'plans', label: 'Cobrança', href: '#plans' },
        { id: 'faq', label: 'FAQ', href: '#faq' },
        { id: 'auditoria', label: 'Auditoria', href: '/search-blockchain' }
      ],
      activeSection: '',
      showMenu: false,
      isAuthenticated: false,
      userProfile: {},
      showUserModal: false,
      activeModalTab: 'profile',
      editMode: false,
      profileForm: {},
      observer: null,
      notification: { show: false, message: '', type: 'success' }
    };
  },
  computed: {
    userRoles() {
      if (!this.isAuthenticated || !this.userProfile.roles) return [];
      return this.userProfile.roles.map(r => ROLE_ID_MAP[r.role]).filter(Boolean);
    },
    currentUserRoleNames() {
      if (!this.userRoles.length) return [];
      return this.userRoles.map(name => name.charAt(0).toUpperCase() + name.slice(1));
    },
    showUserDashboardLink() {
      return this.isAuthenticated && this.userRoles.includes('Usuário');
    },
    showAdminPageLink() {
      return this.isAuthenticated && (this.userRoles.includes('Administrador') || this.userRoles.includes('Gerente'));
    }
  },
  methods: {
    toggleMobileMenu() {
        this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    goHome() {
      this.$router.push('/');
      this.isMobileMenuOpen = false;
    },
    navigateTo(path) {
      this.isMobileMenuOpen = false;
      this.closeUserModal();
      if (this.$route.path !== path) {
        this.$router.push(path).catch(err => {
            if (err.name !== 'NavigationDuplicated') console.error('Erro de navegação:', err);
        });
      }
    },
    handleLink(link) {
      this.isMobileMenuOpen = false;
      if (link.href.startsWith('#')) {
        if (this.$route.path === '/') {
            this.scrollToSection(link.id);
        } else {
            this.$router.push({ path: '/', hash: link.href });
        }
      } else {
        this.navigateTo(link.href);
      }
    },
    showAppNotification(message, type = 'success') { this.notification = { show: true, message, type }; },
    closeNotification() { this.notification.show = false; },
    onUserIconClick() { if (!this.isAuthenticated) { this.navigateTo('/login'); } else { this.showMenu = !this.showMenu; } },
    handleDocumentClick(e) { if (this.showMenu && this.$refs.userMenuWrapper && !this.$refs.userMenuWrapper.contains(e.target)) { this.showMenu = false; } },
    async fetchUserProfile() { try { const profile = await getUserProfile(); this.userProfile = profile; this.isAuthenticated = true; this.profileForm = { ...profile }; } catch (error) { this.isAuthenticated = false; this.userProfile = {}; } },
    triggerOpenUserModal(tab = 'profile') { this.showMenu = false; this.openUserModal(tab); },
    triggerLogout() { this.showMenu = false; this.onLogout(); },
    openUserModal(tab = 'profile') { if (!this.isAuthenticated) return; this.activeModalTab = tab; this.editMode = false; this.profileForm = { ...this.userProfile }; this.showUserModal = true; },
    closeUserModal() { this.showUserModal = false; this.editMode = false; },
    switchTab(tab) { this.activeModalTab = tab; this.editMode = false; },
    cancelEdit() { this.editMode = false; this.profileForm = { ...this.userProfile }; },
    async submitProfile() { try { const updated = await updateUserProfile(this.userProfile.id, this.profileForm); this.userProfile = { ...this.userProfile, ...updated }; this.editMode = false; this.showAppNotification('Perfil atualizado com sucesso!', 'success'); } catch (error) { console.error('Erro ao salvar perfil:', error); this.showAppNotification('Erro ao salvar perfil.', 'error'); } },
    async onLogout() { try { await userLogout(); } catch (error) { console.error('Erro no logout do servidor:', error); } finally { this.isAuthenticated = false; this.userProfile = {}; this.closeUserModal(); if (this.$route.path !== '/') { this.navigateTo('/'); } else { window.location.reload(); } } },
    scrollToSection(id) { this.$nextTick(() => { const el = document.getElementById(id); if (el) el.scrollIntoView({ behavior: 'smooth' }); }); },
    initObserver() { /* Sua lógica de observer permanece aqui */ }
  },
  watch: {
    '$route'() {
      this.isMobileMenuOpen = false;
      this.closeUserModal();
    }
  },
  mounted() {
    this.fetchUserProfile();
    document.addEventListener('click', this.handleDocumentClick);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleDocumentClick);
  }
};
</script>

<style scoped>
.header {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: var(--border-width) solid var(--color-border-light);
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
  gap: var(--sp-md);
}

.logo {
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  color: var(--color-primary);
  font-weight: var(--fw-bold);
  cursor: pointer;
  text-decoration: none;
  flex-shrink: 0;
}

.nav-list {
  display: flex;
  list-style: none;
  gap: var(--sp-sm);
  align-items: center;
  margin: 0;
  padding: 0;
}
.nav-list a {
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: var(--transition-fast);
  padding: var(--sp-xs) var(--sp-sm);
  border-radius: var(--border-radius-sm);
  font-weight: var(--fw-medium);
  cursor: pointer;
  white-space: nowrap;
}
.nav-list a:hover,
.nav-list a.active {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}
.nav-dashboard-link {
  margin-left: var(--sp-sm);
}

.user-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.user-avatar-icon {
  width: 36px;
  height: 36px;
  cursor: pointer;
  border-radius: var(--border-radius-pill);
  transition: var(--transition-fast);
}
.user-avatar-icon:hover, .user-avatar-icon:focus-visible {
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
.user-menu {
  position: absolute;
  top: calc(100% + var(--sp-sm));
  right: 0;
  list-style: none;
  padding: var(--sp-xs) 0;
  min-width: 220px;
  z-index: var(--zindex-dropdown);
}
.user-menu-greeting {
  padding: var(--sp-sm) var(--sp-md);
  font-weight: var(--fw-semibold);
  color: var(--color-text-muted);
  border-bottom: var(--border-width) solid var(--color-border-light);
  margin-bottom: var(--sp-xs);
}
.user-menu li:not(.user-menu-greeting) {
  padding: var(--sp-sm) var(--sp-md);
  cursor: pointer;
  transition: var(--transition-fast);
}
.user-menu li:not(.user-menu-greeting):hover {
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
}

/* Esconde o botão hambúrguer e o botão de fechar em telas grandes */
.hamburger-menu-button, .close-menu-button {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
}

/* Responsividade */
@media (max-width: 992px) {
  .nav {
    display: block;
    position: fixed;
    top: 0;
    right: 0;
    width: 300px;
    height: 100vh;
    background-color: var(--color-bg-component);
    box-shadow: -4px 0px 15px rgba(0,0,0,0.1);
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
    z-index: calc(var(--zindex-sticky) + 1);
    padding-top: var(--sp-xxl);
  }

  .nav.is-open {
    transform: translateX(0);
  }
  
  .nav-list {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--sp-sm);
    padding: var(--sp-lg);
  }
  
  .nav-list a {
    font-size: var(--fs-large);
    width: 100%;
    display: block;
  }
  
  .nav-dashboard-link {
    margin-left: 0;
    margin-top: var(--sp-md);
    text-align: center;
  }

  .hamburger-menu-button {
    display: block;
    z-index: calc(var(--zindex-sticky) + 2);
  }

  .close-menu-button {
    display: block;
    position: absolute;
    top: var(--sp-md);
    right: var(--sp-md);
    font-size: 2.5rem;
    color: var(--color-text-secondary);
  }
  
  /* Esconde a navegação desktop tradicional */
  .header-container > .nav .nav-list {
      display: none;
  }

  /* Mostra a lista dentro do painel mobile */
  .nav.is-open .nav-list {
      display: flex;
  }
}

/* Estilos de Modal e Notificação... */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.65);
  display: flex; align-items: center; justify-content: center;
  z-index: var(--zindex-modal-backdrop);
}
.modal-content {
  background-color: var(--color-bg-component);
  padding: var(--sp-lg);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 650px;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding-bottom: var(--sp-md); margin-bottom: var(--sp-md);
  border-bottom: var(--border-width) solid var(--color-border);
}
.modal-title-text { font-size: var(--fs-h4); margin: 0; }
.button-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.modal-tabs { display: flex; border-bottom: 1px solid var(--color-border); margin-bottom: var(--sp-lg); }
.modal-tab { flex: 1; padding: var(--sp-sm) 0; border: none; background: none; cursor: pointer; border-bottom: 3px solid transparent; color: var(--color-text-muted); }
.modal-tab.active { border-bottom-color: var(--color-primary); color: var(--color-text-primary); font-weight: var(--fw-semibold); }
.modal-actions { display: flex; justify-content: flex-end; gap: var(--sp-sm); margin-top: var(--sp-lg); }
</style>