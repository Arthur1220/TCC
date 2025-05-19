<template>
  <section class="content-panel">
    <h2>Gerenciar Animais</h2>

    <div v-if="animals.length" class="list-group">
      <ul>
        <li v-for="animal in animals" :key="animal.id" class="list-item">
          <div class="item-info">
            <strong>{{ animal.identification }}</strong><br />
            Espécie: {{ animal.specie_name }} • Raça: {{ animal.breed_name }} • Lote: {{ animal.group_name }}
          </div>
          <div class="item-actions">
            <button class="button button-secondary" @click="loadAnimalForEdit(animal)">Editar</button>
            <button class="button button-primary" @click="handleDelete(animal.id)">Deletar</button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="empty-state">
      <p>Nenhum animal cadastrado.</p>
    </div>

    <div class="form-panel">
      <h3>{{ editing ? 'Editar Animal' : 'Cadastrar Animal' }}</h3>
      <form @submit.prevent="handleSubmit" class="form-group">
        <label for="identification">Identificação</label>
        <input id="identification" v-model="form.identification" type="text" required />

        <label for="specie">Espécie</label>
        <select id="specie" v-model="form.specie" required>
          <option disabled value="">Selecione</option>
          <option v-for="option in species" :key="option.id" :value="option.id">{{ option.name }}</option>
        </select>

        <label for="breed">Raça</label>
        <select id="breed" v-model="form.breed" required>
          <option disabled value="">Selecione</option>
          <option v-for="option in breeds" :key="option.id" :value="option.id">{{ option.name }}</option>
        </select>

        <label for="group">Lote / Grupo</label>
        <select id="group" v-model="form.group" @change="handleGroupChange" required>
          <option disabled value="">Selecione</option>
          <option v-for="option in animalGroups" :key="option.id" :value="option.id">{{ option.name }}</option>
          <option value="new">-- Novo Grupo --</option>
        </select>

        <label for="gender">Gênero</label>
        <select id="gender" v-model="form.gender" required>
          <option disabled value="">Selecione</option>
          <option v-for="option in genders" :key="option.id" :value="option.id">{{ option.name }}</option>
        </select>

        <label for="status">Status</label>
        <select id="status" v-model="form.status" required>
          <option disabled value="">Selecione</option>
          <option v-for="option in statuses" :key="option.id" :value="option.id">{{ option.name }}</option>
        </select>

        <label for="identification_type">Tipo de Identificação</label>
        <select id="identification_type" v-model="form.identification_type" required>
          <option disabled value="">Selecione</option>
          <option v-for="option in identificationTypes" :key="option.id" :value="option.id">{{ option.name }}</option>
        </select>

        <label for="birth_date">Data de Nascimento</label>
        <input id="birth_date" v-model="form.birth_date" type="date" required />

        <label for="observations">Observações</label>
        <textarea id="observations" v-model="form.observations"></textarea>

        <div class="form-actions">
          <button type="submit" class="button button-primary">{{ editing ? 'Atualizar' : 'Cadastrar' }}</button>
          <button type="button" v-if="editing" class="button button-secondary" @click="cancelEdit">Cancelar</button>
        </div>
      </form>
    </div>

    <div v-if="showGroupModal" class="modal-overlay" @click.self="closeGroupModal">
      <div class="modal">
        <h4>Cadastrar Novo Grupo</h4>
        <form @submit.prevent="saveNewGroup" class="form-group">
          <label for="new-group-name">Nome do Grupo</label>
          <input id="new-group-name" v-model="newGroup.name" type="text" required />

          <label for="new-group-desc">Descrição</label>
          <input id="new-group-desc" v-model="newGroup.description" type="text" />

          <div class="form-actions">
            <button type="submit" class="button button-primary">Salvar Grupo</button>
            <button type="button" class="button button-secondary" @click="closeGroupModal">Cancelar</button>
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
      newGroup: { name: '', description: '' },
      showGroupModal: false
    };
  },
  async created() {
    await this.loadAnimals();
    await this.loadLookups();
  },
  methods: {
    async loadAnimals() { try { this.animals = await getAnimals(); } catch (e) { console.error(e); } },
    async loadLookups() {
      try {
        this.species = await getSpecies();
        this.breeds = await getBreeds();
        this.animalGroups = await getAnimalGroups();
        this.genders = await getGenders();
        this.statuses = await getStatuses();
        this.identificationTypes = await getIdentificationTypes();
      } catch (e) { console.error(e); }
    },
    handleSubmit() { /* placeholder */ },
    loadAnimalForEdit() { /* placeholder */ },
    cancelEdit() { /* placeholder */ },
    resetForm() { /* placeholder */ },
    handleDelete() { /* placeholder */ },
    handleGroupChange(event) {
      if (event.target.value === 'new') {
        this.showGroupModal = true;
        this.newGroup = { name: '', description: '' };
      }
    },
    async saveNewGroup() {
      try {
        const created = await registerAnimalGroup(this.newGroup);
        this.animalGroups.push(created);
        this.form.group = created.id;
        this.showGroupModal = false;
        alert('Grupo cadastrado com sucesso.');
      } catch (e) { console.error(e); alert('Erro ao cadastrar grupo'); }
    },
    closeGroupModal() {
      this.showGroupModal = false;
      this.form.group = '';
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
.form-group input,
.form-group select,
.form-group textarea {
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
}
.new-group-form {
  margin-top: var(--sp-md);
  padding: var(--sp-md);
  background: var(--color-light-gray);
  border-radius: var(--sp-sm);
}
.form-actions {
  margin-top: var(--sp-md);
  display: flex;
  gap: var(--sp-sm);
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background-color: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
</style>
