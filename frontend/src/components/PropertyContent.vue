<template>
  <section class="content-panel">
    <h2>Minhas Propriedades</h2>

    <!-- Lista de propriedades -->
    <div v-if="properties.length" class="list-group">
      <ul>
        <li v-for="prop in properties" :key="prop.id" class="list-item">
          <div class="item-info">
            <strong>{{ prop.name }}</strong><br />
            {{ prop.address }}, {{ prop.city }} - {{ prop.state }} • CEP: {{ prop.zip_code }}
          </div>
          <div class="item-actions">
            <button class="button button-secondary" @click="editProperty(prop)">Editar</button>
            <button class="button button-primary" @click="removeProperty(prop.id)">Deletar</button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="empty-state">
      <p>Você ainda não possui nenhuma propriedade cadastrada.</p>
    </div>

    <!-- Formulário para cadastro/edição -->
    <div class="form-panel">
      <h3>{{ editing ? 'Editar Propriedade' : 'Adicionar Propriedade' }}</h3>
      <form @submit.prevent="submitForm" class="form-group">
        <label for="name">Nome</label>
        <input id="name" type="text" v-model="formData.name" required />

        <label for="address">Endereço</label>
        <input id="address" type="text" v-model="formData.address" required />

        <label for="city">Cidade</label>
        <input id="city" type="text" v-model="formData.city" required />

        <label for="state">Estado</label>
        <input id="state" type="text" v-model="formData.state" required />

        <label for="zip_code">CEP</label>
        <input id="zip_code" type="text" v-model="formData.zip_code" required />

        <div class="form-actions">
          <button type="submit" class="button button-primary">
            {{ editing ? 'Atualizar' : 'Cadastrar' }}
          </button>
          <button
            type="button"
            v-if="editing"
            class="button button-secondary"
            @click="cancelEdit"
          >
            Cancelar
          </button>
        </div>
      </form>
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
      editingId: null
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
    async submitForm() {
      try {
        if (this.editing) {
          const updated = await updateProperty(this.editingId, this.formData);
          const idx = this.properties.findIndex(p => p.id === this.editingId);
          this.$set(this.properties, idx, updated);
          alert('Propriedade atualizada com sucesso.');
        } else {
          const created = await registerProperty(this.formData);
          this.properties.push(created);
          alert('Propriedade cadastrada com sucesso.');
        }
        this.resetForm();
      } catch (err) {
        console.error('Erro ao salvar propriedade:', err);
        alert('Erro ao salvar propriedade.');
      }
    },
    editProperty(prop) {
      this.editing = true;
      this.editingId = prop.id;
      this.formData = { ...prop };
    },
    cancelEdit() {
      this.resetForm();
      this.editing = false;
      this.editingId = null;
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
.form-panel {
  margin-top: var(--sp-xl);
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
  gap: var(--sp-sm);
}
</style>
