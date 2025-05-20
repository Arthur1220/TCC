<!-- src/components/AppHeader.vue -->
<template>
  <header class="header" role="banner">
    <div class="header-container">
      <h1 class="logo" tabindex="0" @click="goHome" @keydown.enter="goHome">AnimalTracking</h1>
      <nav class="nav" role="navigation" aria-label="Main navigation">
        <ul class="nav-list">
          <li v-for="link in navLinks" :key="link.id">
            <a
              @click.prevent="handleLink(link)"
              :class="{ active: activeSection === link.id }"
              tabindex="0"
            >
              {{ link.label }}
            </a>
          </li>
          <li v-if="isAuthenticated" class="dashboard-link">
            <a @click.prevent="goDashboard" tabindex="0">Dashboard</a>
          </li>
        </ul>
      </nav>

      <div class="user-icon-wrapper" ref="userMenuWrapper">
        <img
          src="https://img.icons8.com/ios-glyphs/30/000000/user--v1.png"
          alt="Menu de usuário"
          tabindex="0"
          @click.stop="onUserIconClick"
          @keydown.enter.prevent="onUserIconClick"
        />
        <ul v-if="showMenu" class="user-menu" @click.stop>
          <li tabindex="0" @click="goProfile">Perfil</li>
          <li tabindex="0" @click="goSettings">Configurações</li>
          <li tabindex="0" @click="onLogout">Sair</li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
import { getUserProfile } from '@/services/userService';
import { logout as userLogout } from '@/services/authService';

export default {
  name: 'AppHeader',
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
      showMenu: false,
      isAuthenticated: false,
      userProfile: null,
      observer: null
    };
  },
  methods: {
    goHome() {
      this.$router.push('/');
      this.activeSection = '';
    },
    goDashboard() {
      this.showMenu = false;
      this.$router.push('/dashboard');
    },
    handleLink(link) {
      this.showMenu = false;
      if (link.href.startsWith('#')) {
        this.$router.push({ path: '/', hash: link.href })
          .then(() => this.scrollToSection(link.id));
      } else {
        this.$router.push(link.href);
      }
    },
    onUserIconClick() {
      if (!this.isAuthenticated) {
        this.$router.push('/login');
      } else {
        this.showMenu = !this.showMenu;
      }
    },
    handleDocumentClick(event) {
      if (this.showMenu && this.$refs.userMenuWrapper && !this.$refs.userMenuWrapper.contains(event.target)) {
        this.showMenu = false;
      }
    },
    scrollToSection(id) {
      this.$nextTick(() => {
        const el = document.getElementById(id);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      });
    },
    goProfile() {
      this.showMenu = false;
      this.$router.push('/profile');
    },
    goSettings() {
      this.showMenu = false;
      this.$router.push('/settings');
    },
    async onLogout() {
      try {
        await userLogout();
      } catch (e) {
        console.error('Erro no logout', e);
      }
      this.isAuthenticated = false;
      this.userProfile = null;
      this.showMenu = false;
      this.$router.push('/login');
    },
    initObserver() {
      if (this.observer) {
        this.observer.disconnect();
        this.observer = null;
      }
      if (this.$route.path !== '/') return;
      const sectionIds = this.navLinks.filter(l => l.href.startsWith('#')).map(l => l.id);
      const sections = sectionIds.map(id => document.getElementById(id)).filter(el => el);
      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.activeSection = entry.target.id;
          }
        });
      }, { threshold: 0.5 });
      sections.forEach(sec => this.observer.observe(sec));
    }
  },
  watch: {
    '$route'(to) {
      this.initObserver();
      if (to.hash && to.path === '/') {
        this.activeSection = to.hash.replace('#','');
      } else if (to.path !== '/') {
        const match = this.navLinks.find(l => l.href === to.path);
        this.activeSection = match ? match.id : '';
      }
    }
  },
  mounted() {
    getUserProfile()
      .then(profile => {
        this.userProfile = profile;
        this.isAuthenticated = true;
      })
      .catch(() => {
        this.isAuthenticated = false;
        this.userProfile = null;
      });
    document.addEventListener('click', this.handleDocumentClick);
    this.initObserver();
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleDocumentClick);
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
  }
};
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  background: rgba(255,255,255,0.8);
  backdrop-filter: saturate(180%) blur(10px);
  border-bottom: 1px solid var(--color-border);
  z-index: 1000;
}
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--sp-sm) var(--sp-md);
}
.logo {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  color: var(--color-text);
  cursor: pointer;
  transition: color 0.2s, transform 0.2s;
}
.logo:hover,
.logo:focus {
  color: var(--color-accent);
  transform: scale(1.1);
  outline: none;
}
.nav-list {
  list-style: none;
  display: flex;
  gap: var(--sp-lg);
}
.nav-list a {
  font-family: var(--font-body);
  color: var(--color-text);
  text-decoration: none;
  transition: color 0.2s;
  cursor: pointer;
}
.nav-list a:hover,
.nav-list a:focus {
  color: var(--color-accent);
  outline: none;
}
.nav-list a.active {
  color: var(--color-accent);
}
.dashboard-link a {
  color: var(--color-accent) !important;
  font-weight: bold;
}
.user-icon-wrapper {
  position: relative;
}
.user-icon-wrapper img {
  width: var(--sp-lg);
  height: var(--sp-lg);
  cursor: pointer;
  transition: transform 0.3s;
}
.user-icon-wrapper img:hover,
.user-icon-wrapper img:focus {
  transform: scale(1.5);
  outline: none;
}
.user-menu {
  position: absolute;
  top: calc(100% + var(--sp-sm));
  right: 0;
  background-color: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  list-style: none;
  padding: var(--sp-sm) 0;
  margin: 0;
  min-width: 160px;
  z-index: 1001;
}
.user-menu li {
  padding: var(--sp-sm) var(--sp-md);
  font-family: var(--font-body);
  color: var(--color-text);
  cursor: pointer;
  transition: background 0.2s;
}
.user-menu li:hover,
.user-menu li:focus {
  background: var(--color-primary-light);
  color: var(--color-white);
  outline: none;
}
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    padding: var(--sp-md);
  }
  .nav-list {
    flex-direction: column;
    gap: var(--sp-sm);
    margin-top: var(--sp-sm);
  }
}
</style>
