<template>
  <div>
    <header class="header" role="banner">
      <div class="header-container container">
        <div class="header-left">
          <h1 class="logo" @click="navigateTo('/')">AnimalTracking</h1>
        </div>

        <nav class="nav-desktop" aria-label="Navegação Principal">
          <ul class="nav-list">
            <li v-for="link in navLinks" :key="link.id">
              <a @click.prevent="handleLink(link)">{{ link.label }}</a>
            </li>
          </ul>
        </nav>

        <div class="header-right">
          <div class="user-icon-wrapper" ref="userMenuWrapper">
            <button @click.stop="onUserIconClick" class="user-avatar-button" aria-label="Menu de utilizador">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            </button>
            <transition name="fade">
              <ul v-if="showMenu" class="user-menu card" @click.stop>
                <template v-if="auth.isAuthenticated">
                  <li class="user-menu-greeting">Olá, {{ auth.user.username }}</li>
                  <li v-if="showUserDashboardLink" @click="navigateTo('/dashboard')">Meu Dashboard</li>
                  <li v-if="showAdminPageLink" @click="navigateTo('/admin')">Painel Admin</li>
                  <li class="user-menu-divider"></li>
                  <li @click="triggerOpenUserModal('profile')">Gerir Perfil</li>
                  <li @click="triggerLogout">Sair</li>
                </template>
                <template v-else>
                    <li @click="navigateTo('/login')">Login</li>
                    <li @click="navigateTo('/register')">Cadastre-se</li>
                </template>
              </ul>
            </transition>
          </div>

          <button class="hamburger-button" @click="toggleMobileMenu" aria-label="Abrir menu">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
          </button>
        </div>
      </div>
    </header>
    
    <nav class="nav-mobile" :class="{ 'is-open': isMobileMenuOpen }">
        <button class="close-button" @click="toggleMobileMenu" aria-label="Fechar menu">&times;</button>
        <ul class="nav-mobile-list">
            <li v-for="link in navLinks" :key="link.id"><a @click.prevent="handleLink(link)">{{ link.label }}</a></li>
        </ul>
    </nav>
    <div class="nav-mobile-overlay" v-if="isMobileMenuOpen" @click="toggleMobileMenu"></div>

    </div>
</template>

<script>
import { auth, logout } from '@/stores/authStore';
import { ROLE_ID_MAP } from '@/utils/constants';

export default {
  name: 'AppHeader',
  data() {
    return {
      auth,
      isMobileMenuOpen: false,
      navLinks: [
        { id: 'benefits', label: 'Benefícios', href: '#benefits' },
        { id: 'details', label: 'Como Funciona', href: '#details' },
        { id: 'plans', label: 'Cobrança', href: '#plans' },
        { id: 'faq', label: 'FAQ', href: '#faq' },
        { id: 'auditoria', label: 'Auditoria', href: '/search-blockchain' },
      ],
      showMenu: false,
    };
  },
  computed: {
    userRoles() {
      if (!this.auth.isAuthenticated || !this.auth.user?.roles) return [];
      return this.auth.user.roles.map(r => ROLE_ID_MAP[r.role]).filter(Boolean);
    },
    showUserDashboardLink() { return this.auth.isAuthenticated && this.userRoles.includes('Usuário'); },
    showAdminPageLink() { return this.auth.isAuthenticated && this.userRoles.includes('Administrador'); }
  },
  methods: {
    toggleMobileMenu() { this.isMobileMenuOpen = !this.isMobileMenuOpen; },
    navigateTo(path) {
      this.showMenu = false;
      this.isMobileMenuOpen = false;
      if (this.$route.path !== path) this.$router.push(path);
    },
    handleLink(link) {
      this.isMobileMenuOpen = false;
      if (link.href.startsWith('#')) {
        if (this.$route.path === '/') this.scrollToSection(link.id);
        else this.$router.push({ path: '/', hash: link.href });
      } else {
        this.navigateTo(link.href);
      }
    },
    onUserIconClick() { this.showMenu = !this.showMenu; },
    handleDocumentClick(e) {
      if (this.showMenu && this.$refs.userMenuWrapper && !this.$refs.userMenuWrapper.contains(e.target)) {
        this.showMenu = false;
      }
    },
    async triggerLogout() {
      this.showMenu = false;
      await logout();
      if (this.$route.meta.requiresAuth) this.$router.push('/');
    },
    scrollToSection(id) {
      this.$nextTick(() => {
        const el = document.getElementById(id);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      });
    },
    triggerOpenUserModal(tab) {
        this.showMenu = false;
        // Aqui você pode emitir um evento para a App.vue ou usar uma store para abrir o modal de perfil
        console.log(`Abrir modal de perfil na aba: ${tab}`);
    },
  },
  watch: {
    '$route'() { this.isMobileMenuOpen = false; }
  },
  mounted() {
    document.addEventListener('click', this.handleDocumentClick);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleDocumentClick);
  }
};
</script>

<style scoped>
/* Estilos Base do Header */
.header {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--gray-300);
  position: sticky;
  top: 0;
  z-index: var(--zindex-sticky);
}
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--sp-md);
  padding-bottom: var(--sp-md);
}
.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: var(--sp-md);
}
.logo {
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  color: var(--color-primary);
  font-weight: var(--fw-bold);
  cursor: pointer;
}

/* Navegação Desktop */
.nav-desktop {
  margin: 0 auto;
  padding: 0 var(--sp-lg);
}
.nav-list {
  display: flex;
  list-style: none;
  gap: var(--sp-lg);
  margin: 0;
  padding: 0;
}
.nav-list a {
  color: var(--color-text-secondary);
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-decoration: none;
}
.nav-list a:hover {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.user-avatar-button {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  color: var(--gray-700);
  border-radius: 50%;
}
.user-avatar-button:hover, .user-avatar-button:focus-visible {
  color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.user-icon-wrapper { position: relative; }
.user-menu {
  position: absolute;
  top: calc(100% + var(--sp-md));
  right: 0;
  width: 240px;
  z-index: var(--zindex-dropdown);
  padding: var(--sp-xs) 0;
}
.user-menu li {
  padding: var(--sp-sm) var(--sp-md);
  cursor: pointer;
  font-weight: var(--fw-medium);
  list-style: none;
}
.user-menu li:not(.user-menu-greeting):not(.user-menu-divider):hover {
  background-color: var(--color-primary);
  color: var(--color-white);
}
.user-menu-greeting {
  font-weight: var(--fw-semibold);
  color: var(--color-text-muted);
  cursor: default;
}
.user-menu-divider {
  height: 1px;
  background-color: var(--color-border);
  margin: var(--sp-xs) 0;
  padding: 0 !important;
  cursor: default;
}
.user-menu-divider:hover {
    background-color: var(--color-border) !important;
}

/* --- Mobile --- */
.hamburger-button, .nav-mobile, .mobile-menu-overlay, .close-button {
  display: none;
}

@media (max-width: 992px) {
  .nav-desktop { display: none; }
  .hamburger-button {
    display: block;
  }
  .nav-mobile {
    display: flex; flex-direction: column;
    position: fixed; top: 0; right: 0;
    width: 300px; max-width: 80vw; height: 100%;
    background: var(--color-white);
    box-shadow: -4px 0 15px rgba(0,0,0,0.1);
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
    z-index: calc(var(--zindex-sticky) + 10);
    padding: var(--sp-xl);
  }
  .nav-mobile.is-open { transform: translateX(0); }
  .mobile-menu-overlay {
    display: block; position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: calc(var(--zindex-sticky) + 5);
  }
  .close-button {
    display: block; position: absolute;
    top: var(--sp-md); right: var(--sp-md);
    font-size: 2.5rem; color: var(--color-text-secondary);
  }
  .nav-mobile-list {
    list-style: none; padding: 0;
    margin-top: var(--sp-xl);
  }
  .nav-mobile-list li a {
    display: block; padding: var(--sp-md) 0;
    font-size: var(--fs-large); color: var(--color-text-primary);
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>