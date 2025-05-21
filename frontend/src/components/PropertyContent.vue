<!-- File: src/components/PropriedadeContent.vue -->
<template>
  <section class="content-panel">
    <h2 class="panel-title">Minhas Propriedades</h2>

    <!-- Botão para abrir modal de adicionar -->
    <div class="add-button-wrapper">
      <button class="button-primary" @click="openModalForAdd">
        + Adicionar Propriedade
      </button>
    </div>

    <!-- Lista de propriedades -->
    <div v-if="properties.length" class="list-group">
      <ul>
        <li v-for="prop in properties" :key="prop.id" class="list-item">
          <div class="item-info">
            <strong>{{ prop.name }}</strong><br />
            {{ prop.address }}, {{ prop.city }} - {{ prop.state }} • CEP: {{ prop.zip_code }}
          </div>
          <div class="item-actions">
            <button class="button-secondary" @click="openModalForEdit(prop)">
              Editar
            </button>
            <button class="button-danger" @click="removeProperty(prop.id)">
              Deletar
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="empty-state">
      <p>Você ainda não possui nenhuma propriedade cadastrada.</p>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">{{ editing ? 'Editar Propriedade' : 'Adicionar Propriedade' }}</h3>
        <form @submit.prevent="submitForm" class="form-group">
          <label for="name">Nome</label>
          <input
            id="name"
            type="text"
            v-model="formData.name"
            required
          />

          <label for="address">Endereço</label>
          <input
            id="address"
            type="text"
            v-model="formData.address"
            required
          />

          <label for="city">Cidade</label>
          <input
            id="city"
            type="text"
            v-model="formData.city"
            required
          />

          <label for="state">Estado</label>
          <input
            id="state"
            type="text"
            v-model="formData.state"
            required
          />

          <label for="zip_code">CEP</label>
          <input
            id="zip_code"
            type="text"
            v-model="formData.zip_code"
            required
          />

          <div class="form-actions">
            <button type="submit" class="button-primary">
              {{ editing ? 'Atualizar' : 'Cadastrar' }}
            </button>
            <button
              type="button"
              class="button-secondary"
              @click="closeModal"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import {
  getUserProperties,
  registerProperty,
  updateProperty,
  deleteProperty
} from '@/services/propertyService';

export default {
  name: 'PropriedadeContent',
  data() {
    return {
      properties: [],
      formData: { name: '', address: '', city: '', state: '', zip_code: '' },
      editing: false,
      editingId: null,
      showModal: false
    };
  },
  async created() {
    await this.loadProperties();
  },
  methods: {
    async loadProperties() {
      try {
        this.properties = await getUserProperties();
      } catch (err) {
        console.error('Erro ao carregar propriedades:', err);
      }
    },
    openModalForAdd() {
      this.editing = false;
      this.editingId = null;
      this.resetForm();
      this.showModal = true;
    },
    openModalForEdit(prop) {
      this.editing = true;
      this.editingId = prop.id;
      this.formData = { ...prop };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async submitForm() {
      try {
        if (this.editing) {
          const updated = await updateProperty(this.editingId, this.formData);
          const idx = this.properties.findIndex(p => p.id === this.editingId);
          this.properties.splice(idx, 1, updated);
          alert('Propriedade atualizada com sucesso.');
        } else {
          const created = await registerProperty(this.formData);
          this.properties.push(created);
          alert('Propriedade cadastrada com sucesso.');
        }
        this.closeModal();
      } catch (err) {
        console.error('Erro ao salvar propriedade:', err);
        alert('Erro ao salvar propriedade.');
      }
    },
    resetForm() {
      this.formData = { name: '', address: '', city: '', state: '', zip_code: '' };
    },
    async removeProperty(id) {
      if (confirm('Deseja realmente remover esta propriedade?')) {
        try {
          await deleteProperty(id);
          this.properties = this.properties.filter(p => p.id !== id);
          alert('Propriedade removida com sucesso.');
        } catch (err) {
          console.error('Erro ao remover propriedade:', err);
          alert('Erro ao remover propriedade.');
        }
      }
    }
  }
};
</script>

<style scoped>
.content-panel {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: var(--sp-xl);
}
.panel-title {
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.add-button-wrapper {
  text-align: right;
  margin-bottom: var(--sp-md);
}
.list-group ul {
  list-style: none;
  padding: 0;
}
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-md) 0;
  border-bottom: 1px solid var(--color-light-gray);
}
.item-info {
  flex: 1;
}
.item-actions button {
  margin-left: var(--sp-sm);
}
/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
.modal-title {
  text-align: center;
  font-family: var(--font-heading);
  margin-bottom: var(--sp-md);
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--sp-md);
}
.form-group label {
  font-weight: 500;
}
.form-group input {
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
}
.form-actions {
  margin-top: var(--sp-md);
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-sm);
}
/* Botões */
.button-primary {
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  padding: var(--sp-sm) var(--sp-lg);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
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
.button-danger {
  background: #e74c3c;
  color: #fff;
  border: 2px solid #e74c3c;
  padding: var(--sp-sm) var(--sp-md);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-danger:hover,
.button-danger:focus {
  background-color: var(--color-bg);
  color: #e74c3c;
  outline: none;
}
.empty-state {
  text-align: center;
  color: var(--color-dark-gray);
  padding: var(--sp-lg) 0;
}
</style>
