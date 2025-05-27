<template>
  <div class="role-manager-panel content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Gerenciamento de Usuários e Funções</h2>
    </div>
    <p class="panel-description">
      Visualize todos os usuários do sistema, atribua ou remova suas funções administrativas e de acesso.
    </p>

    <div v-if="loading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>
      <p>Carregando usuários e funções...</p>
    </div>
    <div v-else-if="errorMessage" class="empty-state card alert alert-danger">
      <h4 class="alert-heading">Erro ao Carregar Dados</h4>
      <p>{{ errorMessage }}</p>
      <button @click="fetchData" class="button button-primary button-sm">Tentar Novamente</button>
    </div>
    <div v-else-if="sortedUsers.length === 0" class="empty-state card">
      <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" viewBox="0 0 24 24" fill="currentColor" width="64" height="64"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
      <h4 class="empty-state-title">Nenhum Usuário Encontrado</h4>
      <p>Não há usuários cadastrados no sistema ou ocorreu um problema ao listá-los.</p>
    </div>
    <div v-else class="user-list-container">
      <ul class="styled-list-group">
        <li
          v-for="user in sortedUsers"
          :key="user.id"
          class="list-item card-hover user-list-item" @click="openModal(user)"
          tabindex="0"
          @keydown.enter="openModal(user)"
          role="button"
          :aria-label="`Gerenciar funções do usuário ${user.username}`"
        >
          <div class="user-item-main-info">
            <span class="user-avatar-placeholder">{{ user.username ? user.username.charAt(0).toUpperCase() : 'U' }}</span>
            <div class="user-details">
              <span class="user-name-text">{{ user.username }}</span>
              <span class="user-email-text">{{ user.email }}</span>
            </div>
          </div>
          <div class="user-roles-tags">
            <span v-if="user.roles && user.roles.length">
              <span v-for="userRole in user.roles" :key="userRole.id" :class="getRoleClass(userRole.role_details?.name)" class="role-badge">
                {{ userRole.role_details ? userRole.role_details.name : 'Role Desconhecida' }}
              </span>
            </span>
            <span v-else class="role-badge status-default">Nenhuma Função</span>
          </div>
          <span class="chevron-icon" aria-hidden="true">&rsaquo;</span>
        </li>
      </ul>
    </div>

    <div v-if="showModal && selectedUser" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content card large-modal">
        <div class="modal-header">
          <h3 class="modal-title-text">Gerenciar Funções de: {{ selectedUser.username }}</h3>
          <button @click="closeModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="roles-management-grid">
            <div class="current-roles-section card"> <h4 class="subsection-title">Funções Atuais</h4>
              <div v-if="selectedUserRoles.length === 0" class="empty-state-small">
                <p>Nenhuma função atribuída a este usuário.</p>
              </div>
              <ul v-else class="roles-list-display">
                <li v-for="userRole in selectedUserRoles" :key="userRole.id" class="role-display-item">
                  <span :class="getRoleClass(userRole.role_details?.name)" class="role-badge">
                      {{ userRole.role_details ? userRole.role_details.name : 'Role Desconhecida' }}
                  </span>
                  <button class="button button-danger button-icon button-sm" @click="handleRemoveRole(userRole.role_details.id)" title="Remover Função">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
                  </button>
                </li>
              </ul>
            </div>

            <div class="assign-new-role-section card"> <h4 class="subsection-title">Atribuir Nova Função</h4>
              <div class="form-group">
                <label for="role-select" class="form-label">Selecione uma função para atribuir:</label>
                <div class="assign-role-controls">
                    <select id="role-select" v-model="selectedRoleIdToAdd" class="select">
                    <option :value="null" disabled>-- Selecione uma função --</option>
                    <option v-for="role in unassignedRolesForSelectedUser" :key="role.id" :value="role.id">
                        {{ role.name }}
                    </option>
                    </select>
                    <button
                    class="button button-primary button-sm assign-button"
                    @click="handleAssignRole"
                    :disabled="!selectedRoleIdToAdd || isSubmittingRoleAction"
                    >
                    <span v-if="isSubmittingRoleAction">Atribuindo...</span>
                    <span v-else>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                        Atribuir
                    </span>
                    </button>
                </div>
                <p v-if="unassignedRolesForSelectedUser.length === 0 && availableRoles.length > 0" class="form-text">
                    Este usuário já possui todas as funções disponíveis.
                </p>
                <p v-if="availableRoles.length === 0" class="form-text">
                    Nenhuma função disponível para atribuição.
                </p>
              </div>
            </div>
          </div>
        </div>
         <div class="modal-actions form-actions">
            <button class="button button-secondary" @click="closeModal">Fechar</button>
        </div>
      </div>
    </div>
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
// O script permanece o mesmo da sua última versão, pois a lógica de dados e métodos já está correta.
// Certifique-se de que as importações e o `ROLE_ID_MAP` (se usado para getRoleClass) estejam corretos.
import { getAllUsers } from '@/services/userService';
import { getRoles, assignUserRole, removeUserRole } from '@/services/userRoleService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'RoleManager',
  components: { NotificationModal },
  data() {
    return {
      users: [],
      availableRoles: [],
      showModal: false,
      selectedUser: null,
      selectedUserRoles: [],
      selectedRoleIdToAdd: null,
      loading: true,
      errorMessage: '',
      isSubmittingRoleAction: false,
      notification: { show: false, title: '', message: '', type: 'success' },
    };
  },
  computed: {
    sortedUsers() {
        return [...this.users].sort((a,b) => (a.username || '').localeCompare(b.username || ''));
    },
    unassignedRolesForSelectedUser() {
      if (!this.selectedUser || !this.availableRoles.length) return [];
      const assignedRoleIds = new Set(this.selectedUserRoles.map(ur => ur.role_details.id));
      return this.availableRoles.filter(role => !assignedRoleIds.has(role.id));
    }
  },
  async mounted() {
    await this.fetchData();
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
    closeNotification() { this.notification.show = false; },
    async fetchData() {
      this.loading = true;
      this.errorMessage = '';
      try {
        const [usersData, rolesData] = await Promise.all([
          getAllUsers(),
          getRoles()
        ]);
        this.users = usersData.map(user => ({
          ...user,
          roles: user.roles || [] 
        }));
        this.availableRoles = rolesData.sort((a,b) => a.name.localeCompare(b.name));
      } catch (error) {
        this.errorMessage = 'Erro ao carregar dados de usuários ou funções.';
        console.error('Erro ao carregar dados (RoleManager):', error.response?.data || error);
        this.showAppNotification('Erro de Carregamento', this.errorMessage, 'error');
      } finally {
        this.loading = false;
      }
    },
    openModal(user) {
      this.selectedUser = { ...user };
      this.selectedUserRoles = user.roles ? [...user.roles] : [];
      this.selectedUserRoles.sort((a,b) => {
          const nameA = a.role_details?.name || '';
          const nameB = b.role_details?.name || '';
          return nameA.localeCompare(nameB);
      });
      this.selectedRoleIdToAdd = null;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedUser = null;
      this.selectedUserRoles = [];
      this.selectedRoleIdToAdd = null;
    },
    getRoleClass(roleName) {
        if (!roleName) return 'status-badge status-default';
        const nameLower = roleName.toLowerCase();
        // Mantenha seu mapeamento de cores para roles aqui
        if (nameLower.includes('administrador')) return 'status-badge status-danger';
        if (nameLower.includes('gerente')) return 'status-badge status-warning';
        if (nameLower.includes('usuario')) return 'status-badge status-success';
        return 'status-badge status-info';
    },
    isRoleAlreadyAssigned(roleId) {
      return this.selectedUserRoles.some(userRole => userRole.role_details && userRole.role_details.id === roleId);
    },
    async handleAssignRole() {
      if (!this.selectedUser || this.selectedRoleIdToAdd === null) {
        this.showAppNotification('Aviso', 'Selecione um usuário e uma função para atribuir.', 'warning');
        return;
      }
      if (this.isRoleAlreadyAssigned(this.selectedRoleIdToAdd)) {
        this.showAppNotification('Aviso', 'Este usuário já possui esta função.', 'warning');
        return;
      }
      this.isSubmittingRoleAction = true;
      try {
        const assignedUserRole = await assignUserRole(this.selectedUser.id, this.selectedRoleIdToAdd);
        if (assignedUserRole && assignedUserRole.role_details) {
            this.selectedUserRoles.push(assignedUserRole);
        } else { // Fallback se a API não retornar o objeto completo
            const roleDetails = this.availableRoles.find(r => r.id === this.selectedRoleIdToAdd);
            if (roleDetails) {
                 this.selectedUserRoles.push({
                    id: Date.now(), // Idealmente a API retorna o ID da UserRole
                    user: this.selectedUser.id,
                    role: roleDetails.id,
                    role_details: roleDetails
                });
            }
        }
        this.selectedUserRoles.sort((a,b) => a.role_details.name.localeCompare(b.role_details.name));
        const userInList = this.users.find(u => u.id === this.selectedUser.id);
        if (userInList) { userInList.roles = [...this.selectedUserRoles]; }
        this.showAppNotification('Sucesso', 'Função atribuída com sucesso!', 'success');
        this.selectedRoleIdToAdd = null;
      } catch (error) {
        console.error('Erro ao atribuir função:', error.response?.data || error);
        this.showAppNotification('Erro', error.response?.data?.error || 'Não foi possível atribuir a função.', 'error');
      } finally {
        this.isSubmittingRoleAction = false;
      }
    },
    async handleRemoveRole(roleIdToRemove) {
      if (!this.selectedUser || !roleIdToRemove) return;
      const roleBeingRemoved = this.availableRoles.find(r => r.id === roleIdToRemove);
      if (!confirm(`Tem certeza que deseja remover a função "${roleBeingRemoved?.name || 'desconhecida'}" do usuário ${this.selectedUser.username}?`)) {
        return;
      }
      this.isSubmittingRoleAction = true;
      try {
        await removeUserRole(this.selectedUser.id, roleIdToRemove);
        this.selectedUserRoles = this.selectedUserRoles.filter(ur => ur.role_details.id !== roleIdToRemove);
        const userInList = this.users.find(u => u.id === this.selectedUser.id);
        if (userInList) { userInList.roles = [...this.selectedUserRoles]; }
        this.showAppNotification('Sucesso', 'Função removida com sucesso!', 'success');
      } catch (error) {
        console.error('Erro ao remover função:', error.response?.data || error);
        this.showAppNotification('Erro', error.response?.data?.error || 'Não foi possível remover a função.', 'error');
      } finally {
        this.isSubmittingRoleAction = false;
      }
    }
  }
};
</script>

<style scoped>
/* Estilos Globais e Variáveis CSS são primários */
.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--sp-md);
    padding-bottom: var(--sp-md);
    border-bottom: var(--border-width) solid var(--color-border-light);
}
.panel-title-text {
  font-family: var(--font-heading);
  color: var(--color-text-primary);
  font-size: var(--fs-h3);
  margin: 0;
  text-align: left;
}
.panel-description {
  text-align: left;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
}

/* Estados de Carregamento e Vazio */
.loading-state, .empty-state { /* .empty-state global já tem estilos */
  padding: var(--sp-xl) var(--sp-md);
  text-align: center;
}
.empty-state.card { background-color: var(--color-bg-muted); }
.loading-state .spinner { margin-bottom: var(--sp-sm); }
.empty-state-icon { color: var(--color-text-muted); width: var(--sp-xxl); height: var(--sp-xxl); margin-bottom: var(--sp-md); }
.empty-state-title { font-family: var(--font-heading); font-size: var(--fs-h5); color: var(--color-text-secondary); margin-bottom: var(--sp-xs); }
.alert.alert-danger { text-align: center; } /* Herda de global */
.alert-heading { font-size: var(--fs-large); font-weight: var(--fw-semibold); margin-bottom: var(--sp-sm); }


/* Lista de Usuários */
.user-list-container {
    margin-top: var(--sp-lg);
}
.styled-list-group {
    list-style: none;
    padding: 0;
    margin: 0;
}
.user-list-item { /* Herda de .list-item e .card-hover globais */
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--sp-md);
  cursor: pointer; /* ADICIONADO: Cursor pointer para indicar clicabilidade */
  /* padding, border, etc. virão de .list-item e .card, e card-hover do global */
}
/* Efeito de hover já é fornecido pela classe .card-hover global */
/* Se precisar de um destaque adicional específico para esta lista: */
/*
.user-list-item:hover, .user-list-item:focus-within {
   background-color: var(--color-bg-hover);
   border-left: 4px solid var(--color-primary);
   padding-left: calc(var(--sp-md) - 4px); // Ajusta padding para compensar a borda
}
*/

.user-item-main-info {
    display: flex;
    align-items: center;
    gap: var(--sp-md);
    flex-grow: 1;
    overflow: hidden; /* Para evitar que o texto comprima os ícones/tags */
}
.user-avatar-placeholder {
    width: 40px;
    height: 40px;
    border-radius: var(--border-radius-pill);
    background-color: var(--color-primary-light);
    color: var(--color-primary-dark);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: var(--fw-bold);
    font-size: var(--fs-large);
    flex-shrink: 0;
}
.user-details {
    display: flex;
    flex-direction: column;
    overflow: hidden; /* Para text-overflow funcionar */
}
.user-name-text {
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
  font-size: var(--fs-base);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-email-text {
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.user-roles-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-xs); /* MODIFICADO: Gap entre os badges de role */
  align-items: center;
  margin-left: var(--sp-sm); /* Espaço entre detalhes do usuário e tags */
  flex-shrink: 0; /* Evita que as tags encolham demais */
}
.role-badge {
  font-size: var(--fs-smaller);
  padding: var(--sp-xxs) var(--sp-xs);
  border-radius: var(--border-radius-sm);
  font-weight: var(--fw-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-inverted);
  /* margin-right: var(--sp-xs);  Removido, pois o gap no container .user-roles-tags já faz isso */
}

/* Cores específicas para as roles (já definidas antes) */
.status-danger { background-color: var(--color-danger); }
.status-warning { background-color: var(--color-warning); color: var(--color-text-primary); }
.status-success { background-color: var(--color-success); }
.status-info { background-color: var(--color-info); }
.status-default { background-color: var(--color-text-muted); }

.chevron-icon {
    color: var(--color-text-muted);
    font-size: var(--fs-large);
    flex-shrink: 0;
}


/* Modal de Gerenciamento de Roles */
.modal-content.large-modal { max-width: 700px; }

.roles-management-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--sp-lg);
}
@media (min-width: 768px) {
    .roles-management-grid {
        grid-template-columns: 1fr 1fr;
    }
}

.current-roles-section, .assign-new-role-section {
    padding: var(--sp-lg); /* Mais padding interno */
    /* .card global já define background, border, border-radius */
}
.subsection-title {
  font-family: var(--font-heading);
  font-size: var(--fs-large);
  color: var(--color-text-primary);
  margin-top: 0;
  margin-bottom: var(--sp-md);
  padding-bottom: var(--sp-sm); /* Aumentado padding */
  border-bottom: var(--border-width) solid var(--color-border);
}

.roles-list-display {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 200px; /* Limita altura e adiciona scroll se necessário */
  overflow-y: auto;
}
.role-display-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-bg-component);
  padding: var(--sp-sm);
  border-radius: var(--border-radius-sm);
  margin-bottom: var(--sp-xs);
  border: var(--border-width) solid var(--color-border-light);
}
.role-display-item .role-badge {
    margin-right: auto;
}
.role-display-item .button.button-icon {
    padding: var(--sp-xxs);
}

.assign-new-role-section .form-group { /* Herda de .form-group global */
    margin-bottom: 0; 
}
.assign-role-controls {
    display: flex;
    gap: var(--sp-sm);
    align-items: center;
}
.assign-role-controls .select { /* Herda de .select global */
    flex-grow: 1;
}
.assign-role-controls .button.assign-button { /* Usa .button .button-primary .button-sm globais */
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    gap: var(--sp-xs);
}
.assign-role-controls .button svg { margin-right: 0; } /* Se o gap no botão já faz isso */

.empty-state-small p {
    font-size: var(--fs-base);
    color: var(--color-text-muted);
    margin: var(--sp-md) 0 0; /* Adiciona margem se for o único conteúdo */
    text-align: center;
    padding: var(--sp-sm);
    background-color: var(--color-bg-component);
    border-radius: var(--border-radius-sm);
}
.form-text { /* Estilo para textos de ajuda em formulários */
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    margin-top: var(--sp-xs);
}


/* Spinner (reutilizado) */
.spinner { animation: rotate 2s linear infinite; width: 40px; height: 40px; margin: var(--sp-md) auto var(--sp-sm); }
.spinner .path { stroke: var(--color-primary); stroke-linecap: round; animation: dash 1.5s ease-in-out infinite; }
@keyframes rotate { 100% { transform: rotate(360deg); } }
@keyframes dash { 0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; } 50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35;} 100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124;} }
</style>