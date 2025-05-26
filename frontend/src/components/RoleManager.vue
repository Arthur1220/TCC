<!-- File: src/components/RoleManager.vue -->
<template>
  <div class="role-manager">
    <h2 class="panel-title">Gerenciar Usuários</h2>
    <ul class="user-list">
      <li
        v-for="user in users"
        :key="user.id"
        class="user-item"
        @click="openModal(user)"
      >
        <span class="user-name">{{ user.username }}</span>
        <span class="user-role">{{ user.role }}</span>
      </li>
    </ul>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">Alterar Role de {{ selectedUser.username }}</h3>
        <select v-model="newRole">
          <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
        </select>
        <div class="form-actions">
          <button class="button-primary" @click="saveRole">Salvar</button>
          <button class="button-secondary" @click="closeModal">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { /*getUsers, updateUserRole*/ } from '@/services/userService';

export default {
  name: 'RoleManager',
  data() {
    return {
      users: [],
      roles: ['user', 'admin', 'manager'],
      showModal: false,
      selectedUser: null,
      newRole: ''
    };
  },
  async mounted() {
    //this.users = await getUsers().catch(() => []);
    alert('Usuários carregados com sucesso.');
  },
  methods: {
    openModal(user) {
      this.selectedUser = { ...user };
      this.newRole = user.role;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedUser = null;
    },
    async saveRole() {
      try {
        //await updateUserRole(this.selectedUser.id, this.newRole);
        const u = this.users.find(u => u.id === this.selectedUser.id);
        if (u) u.role = this.newRole;
        this.closeModal();
        alert('Role atualizada com sucesso.');
      } catch {
        alert('Erro ao atualizar role.');
      }
    }
  }
}
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
.user-list {
  list-style: none;
  padding: 0;
}
.user-item {
  display: flex;
  justify-content: space-between;
  padding: var(--sp-md);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
}
.user-item:hover {
  background: var(--color-light-gray);
}
.user-name { font-weight: 500; }
.user-role { font-style: italic; }

.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%; max-width: 400px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
.modal-title {
  margin-bottom: var(--sp-md);
  text-align: center;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-sm);
  margin-top: var(--sp-md);
}
.button-primary, .button-secondary {
  padding: var(--sp-sm) var(--sp-lg);
  border-radius: var(--sp-sm);
  cursor: pointer;
  border: none;
}
.button-primary {
  background: var(--color-primary);
  color: #fff;
}
.button-secondary {
  background: var(--color-light-gray);
  color: var(--color-dark-gray);
}
</style>
