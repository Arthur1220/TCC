<!-- src/components/AppHeader.vue -->
<template>
  <div>
    <header class="header" role="banner">
      <div class="header-container">
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
            <li tabindex="0" @click="openUserModal('profile')">Perfil</li>
            <li tabindex="0" @click="openUserModal('settings')">Configurações</li>
            <li tabindex="0" @click="onLogout">Sair</li>
          </ul>
        </div>
      </div>
    </header>

    <!-- Modal de Perfil/Configurações -->
    <div v-if="showUserModal" class="modal-overlay" @click.self="closeUserModal">
      <div class="modal-content">
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
          <h3 class="modal-title">Meu Perfil</h3>

          <!-- Modo leitura -->
          <div v-if="!editMode" class="profile-view">
            <p><strong>Usuário:</strong> {{ userProfile.username }}</p>
            <p><strong>Nome:</strong> {{ userProfile.first_name }} {{ userProfile.last_name }}</p>
            <p><strong>E-mail:</strong> {{ userProfile.email }}</p>
            <p><strong>Telefone:</strong> {{ userProfile.phone || '–' }}</p>
            <div class="modal-actions">
              <button class="button-primary" @click="editMode = true">Editar</button>
              <button class="button-secondary" @click="closeUserModal">Fechar</button>
            </div>
          </div>

          <!-- Modo edição -->
          <form v-else @submit.prevent="submitProfile" class="modal-form">
            <div class="form-group">
              <label for="username">Usuário</label>
              <input id="username" v-model="profileForm.username" type="text" required />
            </div>
            <div class="form-group">
              <label for="first_name">Nome</label>
              <input id="first_name" v-model="profileForm.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label for="last_name">Sobrenome</label>
              <input id="last_name" v-model="profileForm.last_name" type="text" required />
            </div>
            <div class="form-group">
              <label for="email">E-mail</label>
              <input id="email" v-model="profileForm.email" type="email" required />
            </div>
            <div class="form-group">
              <label for="phone">Telefone</label>
              <input id="phone" v-model="profileForm.phone" type="text" />
            </div>
            <div class="modal-actions">
              <button type="submit" class="button-primary">Salvar</button>
              <button type="button" class="button-secondary" @click="cancelEdit">Cancelar</button>
            </div>
          </form>
        </div>

        <div v-if="activeModalTab === 'settings'" class="modal-body">
          <h3 class="modal-title">Configurações</h3>
          <p>Aqui você pode ajustar suas preferências do sistema.</p>
          <div class="modal-actions">
            <button class="button-secondary" @click="closeUserModal">Fechar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserProfile, updateUserProfile } from '@/services/userService';
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
      userProfile: {},
      showUserModal: false,
      activeModalTab: 'profile',
      editMode: false,
      profileForm: { username: '', first_name: '', last_name: '', email: '', phone: '' },
      observer: null
    };
  },
  methods: {
    goHome() { this.$router.push('/'); this.activeSection = ''; },
    goDashboard() { this.showMenu = false; this.$router.push('/dashboard'); },
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
      if (!this.isAuthenticated) this.$router.push('/login');
      else this.showMenu = !this.showMenu;
    },
    handleDocumentClick(e) {
      if (this.showMenu && this.$refs.userMenuWrapper && !this.$refs.userMenuWrapper.contains(e.target)) {
        this.showMenu = false;
      }
    },
    openUserModal(tab) {
      this.showMenu = false;
      this.showUserModal = true;
      this.activeModalTab = tab;
      this.editMode = false;
      this.profileForm = { ...this.userProfile };
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
      this.profileForm = { ...this.userProfile };
    },
    async submitProfile() {
      try {
        const updated = await updateUserProfile(this.profileForm);
        this.userProfile = { ...updated };
        this.editMode = false;
        alert('Perfil atualizado com sucesso!');
      } catch {
        alert('Erro ao salvar perfil.');
      }
    },
    async onLogout() {
      await userLogout().catch(() => {});
      this.isAuthenticated = false;
      this.userProfile = {};
      this.showMenu = false;
      this.closeUserModal();
      this.$router.push('/login');
    },
    scrollToSection(id) {
      this.$nextTick(() => {
        const el = document.getElementById(id);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      });
    },
    initObserver() {
      if (this.observer) this.observer.disconnect();
      if (this.$route.path !== '/') return;
      const ids = this.navLinks.filter(l => l.href.startsWith('#')).map(l => l.id);
      const secs = ids.map(i => document.getElementById(i)).filter(x=>x);
      this.observer = new IntersectionObserver(entries => {
        entries.forEach(e => { if(e.isIntersecting) this.activeSection = e.target.id; });
      }, { threshold: 0.5 });
      secs.forEach(s=>this.observer.observe(s));
    }
  },
  mounted() {
    getUserProfile()
      .then(p => { this.userProfile = p; this.isAuthenticated = true; })
      .catch(() => { this.isAuthenticated = false; });
    document.addEventListener('click', this.handleDocumentClick);
    this.initObserver();
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleDocumentClick);
    if (this.observer) this.observer.disconnect();
  }
};
</script>

<style scoped>
.header {
  position: sticky; top: 0;
  background: rgba(255,255,255,0.8); backdrop-filter: blur(10px);
  border-bottom:1px solid var(--color-border); z-index:1000;
}
.header-container {
  max-width:1200px; margin:0 auto;
  display:flex; align-items:center; justify-content:space-between;
  padding:var(--sp-sm) var(--sp-md);
}
.logo {
  font-family:var(--font-heading); font-size:1.75rem;
  color:var(--color-text); cursor:pointer;
  transition:.2s;
}
.logo:hover { color:var(--color-accent); }
.nav-list { display:flex; list-style:none; gap:var(--sp-lg); }
.nav-list a { color:var(--color-text); text-decoration:none; transition:.2s; }
.nav-list a:hover, .nav-list a.active { color:var(--color-accent); }
.dashboard-link a { color:var(--color-accent)!important; font-weight:bold; }

/* dropdown */
.user-icon-wrapper { position:relative; }
.user-icon-wrapper img { width:var(--sp-lg); height:var(--sp-lg); cursor:pointer; }
.user-menu {
  position:absolute; top:calc(100%+var(--sp-sm)); right:0;
  background:#fff; border:1px solid var(--color-border);
  border-radius:var(--sp-sm); box-shadow:0 4px 16px rgba(0,0,0,0.1);
  list-style:none; padding:var(--sp-sm) 0; margin:0; min-width:160px; z-index:1001;
}
.user-menu li {
  padding:var(--sp-sm) var(--sp-md); cursor:pointer;
  transition:background 0.2s, color 0.2s;
}
.user-menu li:hover {
  transition: background 0.3s, transform 0.2s;
  background-color: var(--color-accent);
  color: var(--color-bg);
}

/* Modal */
.modal-overlay {
  position:fixed; top:0; left:0; right:0; bottom:0;
  background:rgba(0,0,0,0.4); display:flex;
  align-items:center; justify-content:center; z-index:2000;
}
.modal-content {
  background:#fff; border-radius:var(--sp-sm);
  padding:var(--sp-lg); width:90%; max-width:500px;
  box-shadow:0 4px 16px rgba(0,0,0,0.2);
}
.modal-tabs { display:flex; border-bottom:1px solid var(--color-border); }
.modal-tab {
  flex:1; padding:var(--sp-sm); text-align:center;
  cursor:pointer; background:none; border:none;
  font-family:var(--font-heading); transition:color .2s, border-color .2s;
}
.modal-tab.active {
  border-bottom:3px solid var(--color-primary);
  color:var(--color-primary);
}
.modal-tab:not(.active):hover {
  color:var(--color-accent);
}
.modal-title {
  text-align:center; font-family:var(--font-heading);
  color:var(--color-primary); margin:var(--sp-md) 0;
}
.modal-body { max-height:70vh; overflow-y:auto; }
.modal-form .form-group {
  margin-bottom:var(--sp-md); display:flex; flex-direction:column;
}
.modal-form label { margin-bottom:var(--sp-sm); color:var(--color-dark-gray); }
.modal-form input, .modal-form textarea {
  padding:var(--sp-sm); border:1px solid var(--color-border);
  border-radius:var(--sp-sm);
}
.profile-view p { margin-bottom:var(--sp-md); }

.modal-actions {
  display:flex; justify-content:flex-end; margin-top:var(--sp-lg);
}
.button-primary {
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  padding: var(--sp-sm) var(--sp-lg);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  margin-right: 1rem;
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
.button-secondary {
  background-color: var(--color-bg);
  color: #e74c3c;
  border: 2px solid #e74c3c;
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-secondary:hover,
.button-secondary:focus {
  background-color: #e74c3c;
  color: var(--color-bg);
  outline: none;
}
</style>
