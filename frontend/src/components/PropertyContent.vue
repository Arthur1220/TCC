<template>
  <div class="property-content-panel content-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Minhas Propriedades</h2>
      <div class="panel-actions">
        <button class="button button-primary" @click="openModalForAdd">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
          Adicionar Propriedade
        </button>
      </div>
    </div>
    <p class="panel-description">
      Gerencie suas propriedades rurais, adicione novas ou edite as existentes. As propriedades são usadas para rastrear a localização dos seus animais e eventos.
    </p>

    <div v-if="isLoadingProperties" class="loading-state">
      <p>Carregando propriedades...</p>
    </div>
    <div v-else-if="properties.length" class="property-list styled-list-group">
      <ul>
        <li
          v-for="prop in properties"
          :key="prop.id"
          class="list-item card-hover"
          @click="openModalForEdit(prop)"
          tabindex="0"
          @keydown.enter="openModalForEdit(prop)"
          role="button"
          :aria-label="`Ver detalhes da propriedade ${prop.name}`"
        >
          <div class="item-info">
            <strong class="property-name">{{ prop.name }}</strong>
            <span class="property-detail">{{ prop.address }}, {{ prop.city }} - {{ prop.state }}</span>
            <span class="property-detail">CEP: {{ prop.zip_code }}</span>
            <span class="property-detail" v-if="prop.country">País: {{ prop.country }}</span>
          </div>
          <div class="item-actions">
            <button class="button button-outline-primary button-sm" @click.stop="openModalForEdit(prop)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
              Editar
            </button>
            <button class="button button-danger button-sm" @click.stop="confirmRemoveProperty(prop.id)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
              Deletar
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="empty-state">
      <p>Você ainda não cadastrou nenhuma propriedade. <a href="#" @click.prevent="openModalForAdd" class="link">Adicionar propriedade</a>.</p>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content card">
        <div class="modal-header">
          <h3 class="modal-title-text">{{ editing ? 'Editar Propriedade' : 'Adicionar Nova Propriedade' }}</h3>
          <button @click="closeModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <form @submit.prevent="submitForm" class="modal-form form-grid">
          <div class="form-group full-width">
            <label for="prop-name" class="form-label">Nome da Propriedade*</label>
            <input id="prop-name" type="text" v-model="formData.name" class="input" required />
          </div>

          <div class="form-group">
            <label for="prop-address" class="form-label">Endereço*</label>
            <input id="prop-address" type="text" v-model="formData.address" class="input" required />
          </div>

          <div class="form-group">
            <label for="prop-city" class="form-label">Cidade*</label>
            <input id="prop-city" type="text" v-model="formData.city" class="input" required />
          </div>

          <div class="form-group">
            <label for="prop-state" class="form-label">Estado (UF)*</label>
            <input id="prop-state" type="text" v-model="formData.state" class="input" required maxlength="2" placeholder="Ex: BA" />
          </div>

          <div class="form-group">
            <label for="prop-zip_code" class="form-label">CEP*</label>
            <input id="prop-zip_code" type="text" v-model="formData.zip_code" class="input" required placeholder="Ex: 00000-000" />
          </div>
          
          <div class="form-group full-width">
            <label for="prop-country" class="form-label">País</label>
            <input id="prop-country" type="text" v-model="formData.country" class="input" placeholder="Brasil" />
          </div>

          <div class="form-actions full-width">
            <button type="submit" class="button button-primary">
              {{ editing ? 'Salvar Alterações' : 'Cadastrar Propriedade' }}
            </button>
            <button type="button" class="button button-secondary" @click="closeModal">
              Cancelar
            </button>
          </div>
        </form>
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
import {
  getUserProperties,
  registerProperty,
  updateProperty,
  deleteProperty
} from '@/services/propertyService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'PropertyContent',
  components: {
      NotificationModal
  },
  props: {
    searchQueryProp: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      properties: [],
      isLoadingProperties: true,
      formData: {
        name: '',
        address: '',
        city: '',
        state: '',
        zip_code: '',
        country: 'Brasil'
      },
      editing: false,
      editingId: null,
      showModal: false,
      notification: { show: false, message: '', type: 'success' },
    };
  },
  async created() {
    await this.loadProperties();
  },
  methods: {
    showAppNotification(message, type = 'success', duration = 3000) {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      if (duration) {
        setTimeout(() => { this.notification.show = false; }, duration);
      }
    },
    closeNotification() { this.notification.show = false; },
    formatDate(dateString) {
        if (!dateString) return 'N/D';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('pt-BR');
        } catch (e) { return dateString; }
    },
    async loadProperties() {
      this.isLoadingProperties = true;
      try {
        this.properties = await getUserProperties();
        this.properties.sort((a,b) => a.name.localeCompare(b.name));
      } catch (err) {
        console.error('Erro ao carregar propriedades:', err.response?.data || err);
        this.showAppNotification('Erro ao carregar suas propriedades.', 'error');
      } finally {
        this.isLoadingProperties = false;
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
      this.formData = { 
          name: prop.name || '',
          address: prop.address || '',
          city: prop.city || '',
          state: prop.state || '',
          zip_code: prop.zip_code || '',
          country: prop.country || 'Brasil'
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async submitForm() {
      if (!this.formData.name || !this.formData.address || !this.formData.city || !this.formData.state || !this.formData.zip_code) {
          this.showAppNotification('Preencha todos os campos obrigatórios (*).', 'warning');
          return;
      }
      try {
        if (this.editing) {
          const updated = await updateProperty(this.editingId, this.formData);
          const idx = this.properties.findIndex(p => p.id === this.editingId);
          if (idx !== -1) this.properties.splice(idx, 1, updated);
          this.showAppNotification('Propriedade atualizada com sucesso!', 'success');
        } else {
          const created = await registerProperty(this.formData);
          this.properties.push(created);
          this.properties.sort((a,b) => a.name.localeCompare(b.name));
          this.showAppNotification('Propriedade cadastrada com sucesso!', 'success');
        }
        this.closeModal();
      } catch (err) {
        console.error('Erro ao salvar propriedade:', err.response?.data || err);
        let errorMessage = 'Erro ao salvar propriedade.';
        if (err.response && err.response.data && typeof err.response.data === 'object') {
            errorMessage += ' Detalhes: ' + Object.entries(err.response.data)
                .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                .join('; ');
        } else if (err.response && err.response.data) {
            errorMessage += ' ' + err.response.data;
        }
        this.showAppNotification(errorMessage, 'error');
      }
    },
    resetForm() {
      this.formData = { name: '', address: '', city: '', state: '', zip_code: '', country: 'Brasil' };
    },
    confirmRemoveProperty(id) {
      if (confirm('Tem certeza que deseja remover esta propriedade? Esta ação não pode ser desfeita.')) {
        this.removeProperty(id);
      }
    },
    async removeProperty(id) {
      try {
        await deleteProperty(id);
        this.properties = this.properties.filter(p => p.id !== id);
        this.showAppNotification('Propriedade removida com sucesso.', 'success');
      } catch (err) {
        console.error('Erro ao remover propriedade:', err.response?.data || err);
        this.showAppNotification('Erro ao remover propriedade.', 'error');
      }
    }
  }
};
</script>

<style scoped>
/* Herda .content-panel da DashboardPage ou define localmente */

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
.panel-actions .button {
    font-size: var(--fs-small);
    padding: var(--sp-xs) var(--sp-sm);
    display: flex;
    align-items: center;
    gap: var(--sp-xs);
}

.panel-description {
  text-align: left;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
}

.property-list { /* Renomeado de .list-group */
  list-style: none;
  padding: 0;
  margin: 0;
}
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-md);
  border: var(--border-width) solid var(--color-border-light);
  border-radius: var(--border-radius);
  margin-bottom: var(--sp-sm);
  background-color: var(--color-bg-component);
  transition: var(--transition-base);
}
.list-item.card-hover:hover, .list-item.card-hover:focus-within {
    border-color: var(--color-primary-light);
    box-shadow: var(--shadow);
    transform: translateY(-2px);
}
.list-item strong.property-name {
    font-size: var(--fs-large);
    font-weight: var(--fw-semibold);
    color: var(--color-primary);
    margin-bottom: var(--sp-xs);
    display: block;
}
.property-detail {
    font-size: var(--fs-small);
    color: var(--color-text-secondary);
    display: block; 
    line-height: 1.4;
}

.item-info {
  flex-grow: 1;
  margin-right: var(--sp-md);
}

.item-actions {
  display: flex;
  gap: var(--sp-xs);
  flex-shrink: 0;
}
.item-actions .button {
    font-size: var(--fs-small);
    padding: var(--sp-xs) var(--sp-sm);
    display: flex; 
    align-items: center;
    gap: var(--sp-xs);
}
.item-actions .button svg {
    margin-right: 0;
}


.empty-state {
  padding: var(--sp-xl) var(--sp-md);
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
  text-align: center; /* Centraliza o texto do empty state */
}
.empty-state p .link {
    font-weight: var(--fw-medium);
}

/* Modal e Formulário usam classes globais definidas em style.css */
/* .modal-overlay, .modal-content, .card, .modal-header, */
/* .modal-title-text, .button-close, .modal-form, .form-grid, */
/* .form-group, .form-label, .input, .form-actions, */
/* .button, .button-primary, .button-secondary */

/* Este estilo específico para .form-group.full-width pode permanecer aqui */
/* ou ser movido para o global style.css se for um padrão recorrente. */
/* Por enquanto, deixo aqui pois é específico de como este formulário é estruturado. */
.form-group.full-width {
    grid-column: 1 / -1; /* Faz o campo ocupar todas as colunas do grid do formulário */
}

.loading-state {
    text-align: center;
    padding: var(--sp-xl);
    color: var(--color-text-muted);
    font-size: var(--fs-large);
}
</style>