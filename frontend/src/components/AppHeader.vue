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
            <template v-if="isAuthenticated">
              <li v-if="showUserDashboardLink" class="dashboard-link">
                <a @click.prevent="navigateTo('/dashboard')" tabindex="0">Dashboard</a>
              </li>
              <li v-if="showAdminPageLink" class="dashboard-link admin-page-link">
                <a @click.prevent="navigateTo('/admin')" tabindex="0">Admin Page</a>
              </li>
            </template>
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
            <li v-if="isAuthenticated && userProfile.username">
                <span class="user-menu-greeting">Olá, {{ userProfile.username }}</span>
            </li>
            <li v-if="isAuthenticated" tabindex="0" @click="openUserModal('profile')">Perfil</li>
            <li v-if="isAuthenticated" tabindex="0" @click="openUserModal('settings')">Configurações</li>
            <li v-if="isAuthenticated" tabindex="0" @click="onLogout">Sair</li>
            <li v-if="!isAuthenticated" tabindex="0" @click="navigateTo('/login')">Login</li>
          </ul>
        </div>
      </div>
    </header>

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
          <div v-if="!editMode" class="profile-view">
            <p><strong>Usuário:</strong> {{ userProfile.username }}</p>
            <p><strong>Nome:</strong> {{ userProfile.first_name }} {{ userProfile.last_name }}</p>
            <p><strong>E-mail:</strong> {{ userProfile.email }}</p>
            <p><strong>Telefone:</strong> {{ userProfile.phone || '–' }}</p>
            <p v-if="currentUserRoleNames.length"> <strong>Função(ões):</strong> {{ currentUserRoleNames.join(', ') }}
            </p>
            <div class="modal-actions">
              <button class="button-primary" @click="editMode = true">Editar</button>
              <button class="button-secondary" @click="closeUserModal">Fechar</button>
            </div>
          </div>
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

// !!! IMPORTANTE: Confirme estes IDs e nomes com seu backend !!!
const ROLE_ID_MAP = {
  1: 'administrador',
  2: 'gerente',
  3: 'usuario',
  // Adicione outros mappings se necessário
};

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
      showMenu: false,
      isAuthenticated: false,
      userProfile: {}, // `roles` será um array aqui
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
      // allRoles: [], // Descomente e popule se for buscar roles dinamicamente
    };
  },
  computed: {
    currentUserRoleNames() {
      if (!this.isAuthenticated || !this.userProfile.roles || !Array.isArray(this.userProfile.roles)) {
        return [];
      }
      return this.userProfile.roles.map(userRoleObject => {
        // userRoleObject é como {id: 1, user: 3, role: 3, ...}
        // userRoleObject.role é o ID da função
        const roleName = ROLE_ID_MAP[userRoleObject.role];
        return roleName ? roleName.charAt(0).toUpperCase() + roleName.slice(1) : null; // Capitaliza
      }).filter(name => name !== null);
    },
    // As computed properties abaixo usam os nomes das roles em minúsculas para a lógica interna
    _currentUserRoleNamesLower() {
        if (!this.isAuthenticated || !this.userProfile.roles || !Array.isArray(this.userProfile.roles)) {
            return [];
        }
        return this.userProfile.roles.map(userRoleObject => ROLE_ID_MAP[userRoleObject.role])
                                  .filter(name => name !== undefined); // Retorna array de nomes em minúsculo
    },
    showUserDashboardLink() {
      if (!this.isAuthenticated) return false;
      return this._currentUserRoleNamesLower.includes('usuario') || this._currentUserRoleNamesLower.includes('administrador');
    },
    showAdminPageLink() {
      if (!this.isAuthenticated) return false;
      return this._currentUserRoleNamesLower.includes('gerente') || this._currentUserRoleNamesLower.includes('administrador');
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
      this.showMenu = false;
    },
    navigateTo(path) {
      this.showMenu = false;
      this.closeUserModal();
      if (this.$route.path !== path) { // Evita navegação para a mesma rota
        this.$router.push(path).catch(err => {
            if (err.name !== 'NavigationDuplicated' && err.name !== ' selben Navigations-Guard mehrmals') {
                console.error('Erro de navegação:', err);
            }
        });
      }
    },
    handleLink(link) {
      this.showMenu = false;
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
    onUserIconClick() {
      if (!this.isAuthenticated) {
        this.navigateTo('/login');
      } else {
        this.showMenu = !this.showMenu;
      }
    },
    handleDocumentClick(e) {
      if (this.showMenu && this.$refs.userMenuWrapper && !this.$refs.userMenuWrapper.contains(e.target)) {
        this.showMenu = false;
      }
    },
    async fetchUserProfile() {
        try {
            const profile = await getUserProfile();
            this.userProfile = profile; // Agora userProfile contém o array 'roles'

            this.isAuthenticated = true;
            if (!this.editMode) {
                this.profileForm = { ...this.userProfile };
            }
        } catch (error) {
            console.warn('Usuário não autenticado ou erro ao buscar perfil:', error.response?.data || error);
            this.isAuthenticated = false;
            this.userProfile = {};
        }
    },
    openUserModal(tab) {
      if (!this.isAuthenticated) return;
      this.showMenu = false;
      this.showUserModal = true;
      this.activeModalTab = tab;
      this.editMode = false;
      this.profileForm = { 
        username: this.userProfile.username || '',
        first_name: this.userProfile.first_name || '',
        last_name: this.userProfile.last_name || '',
        email: this.userProfile.email || '',
        phone: this.userProfile.phone || ''
      };
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
        const updatedProfileData = { ...this.profileForm };
        const updated = await updateUserProfile(updatedProfileData);
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
                    .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                    .join('; ');
            } else if (typeof errors === 'string') {
                errorMessage += ' ' + errors;
            }
        }
        this.showAppNotification(errorMessage, 'error');
      }
    },
    async onLogout() {
      try {
        await userLogout();
      } catch (error) {
        console.error('Erro no logout no servidor, limpando localmente:', error);
      } finally {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userProfile');
        this.isAuthenticated = false;
        this.userProfile = {};
        this.showMenu = false;
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
      this.showMenu = false;
      this.closeUserModal();
    },
    isAuthenticated(newVal, oldVal) { // Modificado para reagir à mudança de autenticação
        if (newVal && (!this.userProfile || Object.keys(this.userProfile).length === 0)) {
            this.fetchUserProfile();
        } else if (!newVal && oldVal) { // Se desautenticado
            this.userProfile = {}; // Limpa perfil
        }
    }
  },
  mounted() {
    // Tenta buscar o perfil. Se o token não existir ou for inválido,
    // o catch em fetchUserProfile e o estado de isAuthenticated cuidarão disso.
    this.fetchUserProfile();
    document.addEventListener('click', this.handleDocumentClick);
    this.initObserver();
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleDocumentClick);
    if (this.observer) {
      this.observer.disconnect();
    }
  }
};
</script>

<style scoped>
/* Seus estilos CSS (.header, .nav-list, .user-menu, .modal-overlay, etc.) permanecem os mesmos */
.header {
  position: sticky; top: 0;
  background: rgba(255,255,255,0.8); backdrop-filter: blur(10px);
  border-bottom:1px solid var(--color-border, #E0E0E0); z-index:1000;
}
.header-container {
  max-width:1200px; margin:0 auto;
  display:flex; align-items:center; justify-content:space-between;
  padding:var(--sp-sm, 0.5rem) var(--sp-md, 1rem);
}
.logo {
  font-family:var(--font-heading, serif); font-size:1.75rem;
  color:var(--color-text, #000); cursor:pointer;
  transition: color 0.2s;
}
.logo:hover { color:var(--color-accent, #1A73E8); }

.nav-list { display:flex; list-style:none; gap:var(--sp-lg, 1.5rem); align-items: center;}
.nav-list li { margin: 0; padding: 0; }
.nav-list a {
    color:var(--color-text, #000);
    text-decoration:none;
    transition: color 0.2s;
    padding: var(--sp-xs, 0.25rem) var(--sp-sm, 0.5rem);
    border-radius: var(--sp-xs, 0.25rem);
    cursor: pointer;
}
.nav-list a:hover, .nav-list a.active {
    color:var(--color-accent, #1A73E8);
    background-color: rgba(0,0,0,0.05);
}
.dashboard-link a, .admin-page-link a { /* Estilo específico para links de dashboard */
  color:var(--color-accent, #1A73E8)!important;
  font-weight:bold;
  border: 1px solid var(--color-accent, #1A73E8);
}
.dashboard-link a:hover, .admin-page-link a:hover {
    background-color: var(--color-accent, #1A73E8) !important;
    color: var(--color-bg, #FFFFFF) !important;
}


/* dropdown */
.user-icon-wrapper { position:relative; }
.user-icon-wrapper img {
    width:calc(var(--sp-lg, 1.5rem) + 4px); /* Aumentado um pouco */
    height:calc(var(--sp-lg, 1.5rem) + 4px);
    cursor:pointer;
    border-radius: 50%;
    padding: 2px;
    transition: box-shadow 0.2s;
}
.user-icon-wrapper img:hover {
    box-shadow: 0 0 5px rgba(0,0,0,0.2);
}
.user-menu {
  position:absolute; top:calc(100% + var(--sp-sm, 0.5rem) + 5px); right:0; /* Mais espaço */
  background:var(--color-bg, #fff); border:1px solid var(--color-border, #E0E0E0);
  border-radius:var(--sp-sm, 0.5rem); box-shadow:0 4px 16px rgba(0,0,0,0.1);
  list-style:none; padding:var(--sp-sm, 0.5rem) 0; margin:0; min-width:180px; /* Aumentado min-width */
  z-index:1001;
}
.user-menu-greeting {
    padding: var(--sp-sm, 0.5rem) var(--sp-md, 1rem);
    font-weight: bold;
    color: var(--color-text-muted, #555); /* Cor mais suave */
    display: block; /* Para ocupar a largura total */
    border-bottom: 1px solid var(--color-border, #eee); /* Separador */
    margin-bottom: var(--sp-xs, 0.25rem); /* Pequeno espaço abaixo */
    cursor: default;
}
.user-menu li {
  padding:var(--sp-sm, 0.5rem) var(--sp-md, 1rem); cursor:pointer;
  transition:background 0.2s, color 0.2s;
  font-size: var(--fs-base, 14px);
}
.user-menu li:not(.user-menu-greeting):hover { /* Não aplicar hover na saudação */
  background-color: var(--color-accent, #1A73E8);
  color: var(--color-bg, #FFFFFF);
}

/* Modal Styles (reutilizando e ajustando os existentes) */
.modal-overlay {
  position:fixed; top:0; left:0; right:0; bottom:0;
  background:rgba(0,0,0,0.5); display:flex; /* Aumentada opacidade do overlay */
  align-items:center; justify-content:center; z-index:2000;
}
.modal-content {
  background:var(--color-bg, #fff); border-radius:var(--sp-sm, 0.5rem);
  padding:var(--sp-lg, 1.5rem); width:90%; max-width:500px;
  box-shadow:0 8px 24px rgba(0,0,0,0.15); /* Sombra mais pronunciada */
}
.modal-tabs {
    display:flex;
    border-bottom:2px solid var(--color-border, #E0E0E0); /* Borda mais grossa */
    margin-bottom: var(--sp-md, 1rem);
}
.modal-tab {
  flex:1; padding:var(--sp-md, 1rem); /* Mais padding */
  text-align:center; cursor:pointer; background:none; border:none;
  font-family:var(--font-body, sans-serif); /* Usar font-body */
  font-weight: 600; /* Mais peso */
  color: var(--color-text-muted, #555);
  border-bottom: 3px solid transparent; /* Para animação da borda */
  transition:color .2s, border-color .2s;
  margin-bottom: -2px; /* Para alinhar com a borda principal */
}
.modal-tab.active {
  border-bottom-color: var(--color-accent, #1A73E8); /* Usar accent color */
  color:var(--color-accent, #1A73E8);
}
.modal-tab:not(.active):hover {
  color:var(--color-text, #000);
  border-bottom-color: var(--color-border-hover, #ccc); /* Borda sutil no hover */
}
.modal-title {
  text-align:center; font-family:var(--font-heading, serif);
  color:var(--color-text, #000); /* Cor de texto padrão */
  margin-top: 0; /* Removido margin-top se já houver espaço das tabs */
  margin-bottom:var(--sp-lg, 1.5rem); /* Mais espaço abaixo do título */
  font-size: var(--fs-large, 1.25rem); /* Tamanho de fonte um pouco maior */
}
.modal-body { max-height:65vh; overflow-y:auto; padding-right: var(--sp-sm); } /* Padding para scrollbar */

.modal-form .form-group {
  margin-bottom:var(--sp-md, 1rem); display:flex; flex-direction:column;
}
.modal-form label {
    margin-bottom:var(--sp-xs, 0.25rem); /* Menor espaço abaixo do label */
    color:var(--color-text, #333);
    font-weight: 600;
}
.modal-form input, .modal-form textarea {
  padding:var(--sp-sm, 0.65rem); border:1px solid var(--color-border, #ccc); /* Borda um pouco mais escura */
  border-radius:var(--sp-xs, 0.25rem); /* Bordas menos arredondadas */
  font-size: var(--fs-base, 14px);
}
.modal-form input:focus, .modal-form textarea:focus {
    border-color: var(--color-accent, #1A73E8);
    box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2); /* Sombra no foco */
}

.profile-view p { margin-bottom:var(--sp-sm, 0.5rem); line-height: 1.6; } /* Menor margem e line-height */
.profile-view p strong { color: var(--color-text, #000); }

.modal-actions {
  display:flex; justify-content:flex-end; gap: var(--sp-sm, 0.5rem);
  margin-top:var(--sp-lg, 1.5rem);
  padding-top: var(--sp-md, 1rem);
  border-top: 1px solid var(--color-border, #E0E0E0);
}

/* Estilos de botões já fornecidos parecem ok, mas vamos garantir consistência */
.button-primary {
  background-color: var(--color-accent, #1A73E8); /* Cor de destaque */
  color: var(--color-bg, #FFFFFF);
  border: 2px solid var(--color-accent, #1A73E8);
  padding: var(--sp-sm, 0.65rem) var(--sp-lg, 1.2rem); /* Padding ajustado */
  border-radius: var(--sp-sm, 0.5rem);
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
  /* Removido margin-right, usar gap no container .modal-actions */
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-bg, #FFFFFF);
  color: var(--color-accent, #1A73E8);
  border-color: var(--color-accent, #1A73E8);
  outline: none;
}

.button-secondary { /* Geralmente usado para ações de cancelamento ou menos importantes */
  background-color: var(--color-muted, #f5f5f5); /* Fundo mais neutro */
  color: var(--color-text, #333);
  border: 2px solid var(--color-border, #ccc);
  padding: var(--sp-sm, 0.65rem) var(--sp-md, 1rem); /* Padding um pouco menor */
  border-radius: var(--sp-sm, 0.5rem);
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}
.button-secondary:hover,
.button-secondary:focus {
  background-color: var(--color-dark-gray, #555); /* Escurece no hover */
  color: var(--color-bg, #FFFFFF);
  border-color: var(--color-dark-gray, #555);
  outline: none;
}
/* Botão de perigo (Sair, Deletar) - pode herdar do global ou definir aqui se necessário */
/* .button-danger ... */
</style>