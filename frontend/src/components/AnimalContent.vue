<!-- File: src/components/AnimalContent.vue -->
<template>
  <section class="content-panel">
    <h2 class="panel-title">Gerenciar Animais</h2>
    <p class="panel-description">
      Nesta tela você pode cadastrar novos animais, editar dados existentes ou removê-los.
    </p>

    <!-- Botão para abrir modal de adicionar -->
    <div class="add-button-wrapper">
      <button class="button-primary" @click="openModalForAdd">
        + Cadastrar Animal
      </button>
    </div>

    <!-- Lista de animais -->
    <div v-if="animals.length" class="list-group">
      <ul>
        <li v-for="animal in animals" :key="animal.id" class="list-item">
          <div class="item-info">
            <strong>{{ animal.identification }}</strong><br />
            Espécie: {{ animal.specie_name }} • Raça: {{ animal.breed_name }} • Grupo: {{ animal.group_name }}
          </div>
          <div class="item-actions">
            <button class="button-secondary" @click="openModalForEdit(animal)">
              Editar
            </button>
            <button class="button-danger" @click="handleDelete(animal.id)">
              Deletar
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="empty-state">
      <p>Nenhum animal cadastrado.</p>
    </div>

    <!-- Modal de Cadastrar/Editar Animal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">{{ editing ? 'Editar Animal' : 'Cadastrar Animal' }}</h3>
        <form @submit.prevent="handleSubmit" class="form-group">
          <label for="identification">Identificação</label>
          <input id="identification" v-model="form.identification" type="text" required />

          <label for="specie">Espécie</label>
          <select id="specie" v-model="form.specie" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in species" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>

          <label for="breed">Raça</label>
          <select id="breed" v-model="form.breed" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in breeds" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>

          <label for="group">Grupo / Lote</label>
          <select id="group" v-model="form.group" @change="handleGroupChange" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in animalGroups" :key="o.id" :value="o.id">{{ o.name }}</option>
            <option value="new">+ Novo Grupo</option>
          </select>

          <label for="gender">Gênero</label>
          <select id="gender" v-model="form.gender" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in genders" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>

          <label for="status">Status</label>
          <select id="status" v-model="form.status" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in statuses" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>

          <label for="identification_type">Tipo de Identificação</label>
          <select id="identification_type" v-model="form.identification_type" required>
            <option disabled value="">Selecione</option>
            <option v-for="o in identificationTypes" :key="o.id" :value="o.id">{{ o.name }}</option>
          </select>

          <label for="birth_date">Data de Nascimento</label>
          <input id="birth_date" v-model="form.birth_date" type="date" required />

          <label for="observations">Observações</label>
          <textarea id="observations" v-model="form.observations"></textarea>

          <div class="form-actions">
            <button type="submit" class="button-primary">
              {{ editing ? 'Atualizar' : 'Cadastrar' }}
            </button>
            <button type="button" class="button-secondary" @click="closeModal">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Novo Grupo -->
    <div v-if="showGroupModal" class="modal-overlay" @click.self="closeGroupModal">
      <div class="modal-content">
        <h3 class="modal-title">Cadastrar Novo Grupo</h3>
        <form @submit.prevent="saveNewGroup" class="form-group">
          <label for="new-group-name">Nome do Grupo</label>
          <input id="new-group-name" v-model="newGroup.name" type="text" required />

          <label for="new-group-desc">Descrição</label>
          <input id="new-group-desc" v-model="newGroup.description" type="text" />

          <div class="form-actions">
            <button type="submit" class="button-primary">Salvar Grupo</button>
            <button type="button" class="button-secondary" @click="closeGroupModal">
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
  registerAnimal,
  getAnimals,
  updateAnimal,
  deleteAnimal
} from '@/services/animalService';
import {
  getSpecies,
  getBreeds,
  getAnimalGroups,
  getGenders,
  getStatuses,
  getIdentificationTypes,
  registerAnimalGroup
} from '@/services/lookupService';

export default {
  name: 'AnimalContent',
  data() {
    return {
      animals: [],
      form: {
        identification: '',
        specie: '',
        breed: '',
        group: '',
        gender: '',
        status: '',
        identification_type: '',
        birth_date: '',
        observations: ''
      },
      species: [],
      breeds: [],
      animalGroups: [],
      genders: [],
      statuses: [],
      identificationTypes: [],
      editing: false,
      editingId: null,
      showModal: false,
      newGroup: { name: '', description: '' },
      showGroupModal: false
    };
  },
  async created() {
    await this.loadAnimals();
    await this.loadLookups();
  },
  methods: {
    async loadAnimals() {
      try {
        this.animals = await getAnimals();
      } catch (e) {
        console.error(e);
      }
    },
    async loadLookups() {
      try {
        this.species = await getSpecies();
        this.breeds = await getBreeds();
        this.animalGroups = await getAnimalGroups();
        this.genders = await getGenders();
        this.statuses = await getStatuses();
        this.identificationTypes = await getIdentificationTypes();
      } catch (e) {
        console.error(e);
      }
    },
    openModalForAdd() {
      this.editing = false;
      this.editingId = null;
      this.resetForm();
      this.showModal = true;
    },
    openModalForEdit(animal) {
      this.editing = true;
      this.editingId = animal.id;
      this.form = { ...animal };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async handleSubmit() {
      try {
        if (this.editing) {
          const updated = await updateAnimal(this.editingId, this.form);
          const idx = this.animals.findIndex(a => a.id === this.editingId);
          this.animals.splice(idx, 1, updated);
          alert('Animal atualizado com sucesso.');
        } else {
          const created = await registerAnimal(this.form);
          this.animals.push(created);
          alert('Animal cadastrado com sucesso.');
        }
        this.closeModal();
      } catch (e) {
        console.error(e);
        alert('Erro ao salvar animal.');
      }
    },
    handleDelete(id) {
      if (confirm('Deseja realmente deletar este animal?')) {
        deleteAnimal(id)
          .then(() => {
            this.animals = this.animals.filter(a => a.id !== id);
            alert('Animal deletado com sucesso.');
          })
          .catch(e => {
            console.error(e);
            alert('Erro ao deletar animal.');
          });
      }
    },
    handleGroupChange(e) {
      if (e.target.value === 'new') {
        this.showGroupModal = true;
        this.newGroup = { name: '', description: '' };
      }
    },
    async saveNewGroup() {
      try {
        const created = await registerAnimalGroup(this.newGroup);
        this.animalGroups.push(created);
        this.form.group = created.id;
        this.closeGroupModal();
        alert('Grupo cadastrado com sucesso.');
      } catch (e) {
        console.error(e);
        alert('Erro ao cadastrar grupo.');
      }
    },
    closeGroupModal() {
      this.showGroupModal = false;
      if (!this.editing) this.form.group = '';
    },
    resetForm() {
      this.form = {
        identification: '',
        specie: '',
        breed: '',
        group: '',
        gender: '',
        status: '',
        identification_type: '',
        birth_date: '',
        observations: ''
      };
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
  margin-bottom: var(--sp-xs);
}
.panel-description {
  text-align: center;
  color: var(--color-dark-gray);
  margin-bottom: var(--sp-md);
  font-size: var(--font-size-base);
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
.empty-state {
  text-align: center;
  color: var(--color-dark-gray);
  padding: var(--sp-lg) 0;
}
/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%;
  max-width: 700px;
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
.form-group input,
.form-group select,
.form-group textarea {
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-sm);
  margin-top: var(--sp-md);
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
</style>
