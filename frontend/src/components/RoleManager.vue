<template>
  <div class="role-manager">
    <h2 class="panel-title">Gerenciar Usuários</h2>

    <div v-if="loading" class="loading-state">
      <p>Carregando usuários e roles...</p>
    </div>
    <div v-else-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
    <ul v-else class="user-list">
      <li
        v-for="user in users"
        :key="user.id"
        class="user-item"
        @click="openModal(user)"
      >
        <span class="user-name">{{ user.username }}</span>
        <div class="user-roles-display">
          Roles:
          <span v-if="user.roles && user.roles.length">
            <span v-for="userRole in user.roles" :key="userRole.id" class="role-tag">
              {{ userRole.role_details ? userRole.role_details.name : 'Role Desconhecida' }}
            </span>
          </span>
          <span v-else class="no-role">Nenhuma</span>
        </div>
      </li>
    </ul>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-button" @click="closeModal">&times;</button>
        <h3 class="modal-title">Gerenciar Roles de {{ selectedUser.username }}</h3>
        
        <div class="current-roles">
          <h4>Roles Atuais:</h4>
          <p v-if="selectedUserRoles.length === 0">Nenhuma role atribuída.</p>
          <ul v-else class="current-roles-list">
            <li v-for="userRole in selectedUserRoles" :key="userRole.id">
              <span>{{ userRole.role_details.name }}</span>
              <button class="remove-role-btn" @click="handleRemoveRole(userRole.role_details.id)">Remover</button>
            </li>
          </ul>
        </div>

        <div class="assign-new-role">
          <h4>Atribuir Role:</h4>
          <ul class="current-roles-list"> <li>
              <select v-model="selectedRoleIdToAdd">
                <option :value="null" disabled>Selecione uma role</option>
                <option v-for="role in availableRoles" :key="role.id" :value="role.id">
                  {{ role.name }}
                </option>
              </select>
              <button 
                class="button-primary assign-btn" 
                @click="handleAssignRole" 
                :disabled="!selectedRoleIdToAdd || isRoleAlreadyAssigned(selectedRoleIdToAdd)">
                Atribuir
              </button>
            </li>
          </ul>
        </div>

        <div v-if="modalMessage" :class="['modal-feedback', modalMessageType]">
          {{ modalMessage }}
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { getAllUsers } from '@/services/userService';
import { getRoles, assignUserRole, removeUserRole } from '@/services/userRoleService';

export default {
  name: 'RoleManager',
  data() {
    return {
      users: [],
      availableRoles: [], // Todas as roles disponíveis (Admin, Manager, User, etc.)
      showModal: false,
      selectedUser: null, // Usuário atualmente selecionado no modal
      selectedUserRoles: [], // Roles do usuário selecionado para exibir no modal
      selectedRoleIdToAdd: null, // ID da role a ser adicionada
      loading: true,
      errorMessage: '',
      modalMessage: '',
      modalMessageType: '' // 'success' or 'error'
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.errorMessage = '';
      try {
        const [usersData, rolesData] = await Promise.all([
          getAllUsers(), // Busca todos os usuários, que agora já vêm com suas roles
          getRoles() // Busca todas as roles disponíveis
        ]);
        this.users = usersData;
        this.availableRoles = rolesData;
        this.loading = false;
      } catch (error) {
        this.errorMessage = 'Erro ao carregar dados de usuários ou roles. Verifique as permissões ou a conexão.';
        console.error('Erro ao carregar dados:', error);
        this.loading = false;
      }
    },
    openModal(user) {
      this.selectedUser = { ...user };
      // As roles já estão no objeto user retornado pelo backend
      this.selectedUserRoles = user.roles || []; 
      this.selectedRoleIdToAdd = null; // Resetar seleção para nova atribuição
      this.modalMessage = ''; // Limpar mensagens antigas
      this.modalMessageType = '';
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedUser = null;
      this.selectedUserRoles = [];
      this.selectedRoleIdToAdd = null;
    },
    isRoleAlreadyAssigned(roleId) {
      // Verifica se a role já está atribuída ao usuário selecionado
      return this.selectedUserRoles.some(userRole => userRole.role === roleId);
    },
    async handleAssignRole() {
      if (!this.selectedUser || !this.selectedRoleIdToAdd) {
        this.showModalMessage('Selecione um usuário e uma role.', 'error');
        return;
      }
      if (this.isRoleAlreadyAssigned(this.selectedRoleIdToAdd)) {
        this.showModalMessage('Este usuário já possui esta role.', 'error');
        return;
      }

      try {
        const response = await assignUserRole(this.selectedUser.id, this.selectedRoleIdToAdd);
        this.showModalMessage(response.status, 'success');
        // Atualiza as roles do usuário no modal e na lista principal
        const assignedRole = this.availableRoles.find(r => r.id === this.selectedRoleIdToAdd);
        if (assignedRole) {
            this.selectedUserRoles.push({
                id: response.user_role.id, // O ID da nova UserRole criada
                user: this.selectedUser.id,
                role: assignedRole.id,
                role_details: assignedRole // Inclui os detalhes da role
            });
        }
        // Atualiza o objeto user na lista principal para refletir a mudança
        const userInList = this.users.find(u => u.id === this.selectedUser.id);
        if (userInList) {
            userInList.roles = [...this.selectedUserRoles]; // Garante reatividade
        }
        this.selectedRoleIdToAdd = null; // Limpar a seleção do select
      } catch (error) {
        const msg = error.error || 'Erro ao atribuir role.';
        this.showModalMessage(`Erro: ${msg}`, 'error');
      }
    },
    async handleRemoveRole(roleId) {
      if (!this.selectedUser || !roleId) {
        this.showModalMessage('Erro: ID de usuário ou role ausente.', 'error');
        return;
      }
      if (!confirm('Tem certeza que deseja remover esta role do usuário?')) {
        return;
      }
      try {
        await removeUserRole(this.selectedUser.id, roleId);
        this.showModalMessage('Role removida com sucesso!', 'success');
        // Remove a role da lista do modal
        this.selectedUserRoles = this.selectedUserRoles.filter(ur => ur.role !== roleId);
        // Atualiza o objeto user na lista principal para refletir a mudança
        const userInList = this.users.find(u => u.id === this.selectedUser.id);
        if (userInList) {
            userInList.roles = [...this.selectedUserRoles]; // Garante reatividade
        }
      } catch (error) {
        const msg = error.error || 'Erro ao remover role.';
        this.showModalMessage(`Erro: ${msg}`, 'error');
      }
    },
    showModalMessage(msg, type) {
      this.modalMessage = msg;
      this.modalMessageType = type;
      setTimeout(() => {
        this.modalMessage = '';
        this.modalMessageType = '';
      }, 3000);
    }
  }
};
</script>

<style scoped>
.role-manager {
  width: 100%;
}
.panel-title {
  text-align: center;
  margin-bottom: var(--sp-md);
  font-family: var(--font-heading);
  color: var(--color-primary);
}
.loading-state, .error-message {
  text-align: center;
  padding: var(--sp-md);
  color: var(--color-dark-gray);
}
.error-message {
  color: #e74c3c;
}
.user-list {
  list-style: none;
  padding: 0;
}
.user-item {
  display: flex;
  flex-direction: column; /* Para empilhar nome e roles */
  align-items: flex-start;
  padding: var(--sp-md);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.user-item:hover {
  background: var(--color-muted);
}
.user-name {
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--sp-sm);
}
.user-roles-display {
  font-size: var(--fs-small);
  color: var(--color-dark-gray);
}
.role-tag {
  display: inline-block;
  background-color: var(--color-accent);
  color: var(--color-bg);
  padding: 0.2em 0.6em;
  border-radius: var(--sp-sm);
  margin-left: 0.5em;
  font-weight: normal;
  font-size: 0.9em;
}
.no-role {
  font-style: italic;
  color: var(--color-dark-gray);
  margin-left: 0.5em;
}


/* Modal Styles */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%; max-width: 500px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  position: relative;
}
.close-button {
  position: absolute;
  top: var(--sp-sm);
  right: var(--sp-sm);
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-dark-gray);
}
.close-button:hover {
  color: var(--color-text);
}
.modal-title {
  margin-bottom: var(--sp-lg);
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
}

.current-roles, .assign-new-role {
  margin-bottom: var(--sp-lg);
  padding: var(--sp-md);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
}

.current-roles h4, .assign-new-role h4 {
  margin-bottom: var(--sp-md);
  color: var(--color-text);
}

.current-roles-list {
  list-style: none;
  padding: 0;
}

.current-roles-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-muted);
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  margin-bottom: var(--sp-sm);
  font-size: var(--fs-base);
}

/* Estilos base para todos os botões */
button {
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  cursor: pointer;
  font-size: var(--fs-base);
  font-weight: 500;
  transition: background 0.3s ease, color 0.3s ease, border-color 0.3s ease, transform 0.2s ease;
  white-space: nowrap;
}

/* Estilo para botões de remoção */
.remove-role-btn {
  background-color: #e74c3c;
  color: #fff;
  border: 2px solid #e74c3c;
}
.remove-role-btn:hover,
.remove-role-btn:focus {
  background-color: #c0392b;
  border-color: #c0392b;
  transform: translateY(-1px);
  outline: none;
}

/* Estilo para botões primários (geral, aplicado ao 'Atribuir') */
.button-primary {
  background-color: var(--color-accent); /* Usar o azul para primário */
  color: var(--color-bg);
  border: 2px solid var(--color-accent);
}
.button-primary:hover,
.button-primary:focus {
  background-color: var(--color-accent-dark);
  border-color: var(--color-accent-dark);
  transform: translateY(-1px);
  outline: none;
}
.button-primary:disabled {
  background-color: #cccccc;
  border-color: #cccccc;
  color: #888888;
  cursor: not-allowed;
  transform: none;
}

/* Ajustes específicos para o select dentro da nova estrutura de atribuição */
.assign-new-role .current-roles-list li select {
  flex-grow: 1; /* Permite que o select ocupe o espaço disponível */
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  margin-right: var(--sp-sm); /* Espaço entre o select e o botão */
}


.modal-feedback {
  padding: var(--sp-sm);
  border-radius: var(--sp-sm);
  margin-top: var(--sp-md);
  text-align: center;
  font-weight: 500;
}

.modal-feedback.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.modal-feedback.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>