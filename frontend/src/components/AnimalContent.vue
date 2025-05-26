<!-- File: src/components/AnimalContent.vue -->
<template>
  <div>
    <section v-if="!showGroupManager" class="content-panel">
      <h2 class="panel-title">Gerenciar Animais</h2>
      <p class="panel-description">
        Nesta tela você pode cadastrar novos animais, editar dados existentes ou removê-los.
      </p>

      <div class="add-button-wrapper">
        <button class="button-primary" @click="openModalForAdd">
          + Cadastrar Animal
        </button>
        <button class="button-primary" @click="openGroupManager">
          Gerenciar Lotes
        </button>
      </div>

      <div v-if="animals.length" class="list-group">
        <ul>
          <li
            v-for="animal in animals"
            :key="animal.id"
            class="list-item"
          >
            <div class="item-info">
              <strong>{{ animal.identification }}</strong><br />
              Espécie: {{ animal.specie_name }} •
              Raça: {{ animal.breed_name }} •
              Grupo: {{ animal.group_name }} •
              Nascimento: {{ animal.birth_date }}<br />
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
          <h3 class="modal-title">
            {{ editing ? 'Editar Animal' : 'Cadastrar Animal' }}
          </h3>
          <form @submit.prevent="handleSubmit" class="form-group">
            <label for="identification">Identificação</label>
            <input id="identification" v-model="form.identification" type="text" required />

            <label for="specie">Espécie</label>
            <select
              id="specie"
              v-model="form.specie"
              @change="onSpecieChange"
              required
            >
              <option disabled value="">Selecione</option>
              <option v-for="s in species" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>

            <label for="breed">Raça</label>
            <select id="breed" v-model="form.breed" required>
              <option disabled value="">Selecione</option>
              <option
                v-for="b in filteredBreeds"
                :key="b.id"
                :value="b.id"
              >{{ b.name }}</option>
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
            <div v-if="editing">
              <select id="status" v-model="form.status" required>
                <option disabled value="">Selecione</option>
                <option v-for="o in statuses" :key="o.id" :value="o.id">{{ o.name }}</option>
              </select>
            </div>
            <div v-else>
              <input type="hidden" v-model="form.status" />
              <p class="status-default">Ativo</p>
            </div>

            <label for="identification_type">Tipo de Identificação</label>
            <select id="identification_type" v-model="form.identification_type" required>
              <option disabled value="">Selecione</option>
              <option
                v-for="o in identificationTypes"
                :key="o.id"
                :value="o.id"
              >{{ o.name }}</option>
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

    <!-- Tela de Lotes -->
    <LotContent v-else @back="closeGroupManager" />
  </div>
</template>

<script>
import {
  registerAnimal,
  getAnimals,
  updateAnimal,
  deleteAnimal
} from '@/services/animalService'
import {
  getSpecies,
  getBreeds,
  getAnimalGroups,
  getGenders,
  getStatuses,
  getIdentificationTypes,
  registerAnimalGroup
} from '@/services/lookupService'
import LotContent from '@/components/LotContent.vue'

export default {
  name: 'AnimalContent',
  components: { LotContent },
  data() {
    return {
      showGroupManager: false,
      animals: [],
      form: {
        identification: '',
        specie: '',
        breed: '',
        group: '',
        gender: '',
        status: 1,
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
    }
  },
  async created() {
    await this.loadLookups()
    await this.loadAnimals()
  },
  computed: {
    filteredBreeds() {
      return this.breeds.filter(b =>
        b.specie === this.form.specie || b.specie_id === this.form.specie
      )
    }
  },
  methods: {
    openGroupManager() {
      this.showGroupManager = true
    },
    closeGroupManager() {
      this.showGroupManager = false
    },
    async loadLookups() {
      this.species = await getSpecies()
      this.breeds = await getBreeds()
      this.animalGroups = await getAnimalGroups()
      this.genders = await getGenders()
      this.statuses = await getStatuses()
      this.identificationTypes = await getIdentificationTypes()
    },
    async loadAnimals() {
      try {
        // A chamada getAnimals() agora será filtrada por owner no backend (se você aplicou as mudanças no AnimalViewSet)
        // Se EventContent precisa de animais com status específico, animalService.getAnimals({ status: 1 }) ainda é válido
        // e o backend AnimalViewSet.get (list) precisa tratar esse parâmetro 'status'.
        const list = await getAnimals(); // Se AnimalContent só precisa dos animais do usuário, não são necessários filtros aqui.
                                        // Se EventContent chama getAnimals({ status: 1}), o backend (AnimalViewSet.get) precisa lidar com isso.

        this.animals = list.map(a => ({
          ...a,
          // Se o serializer já fornece _name, os fallbacks com .find são menos críticos
          // mas podem ser mantidos para robustez ou se o _name for opcional no serializer
          specie_name: a.specie_name || 'N/D', // Agora a.specie_name deve vir da API
          breed_name: a.breed_name || 'N/D',   // Agora a.breed_name deve vir da API
          group_name: a.group_name || 'N/D',   // Agora a.group_name deve vir da API
          gender_name: a.gender_name || 'N/D',
          status_name: a.status_name || 'N/D',
          identification_type_name: a.identification_type_name || 'N/D'
          // o a.specie (ID) agora será chamado de a.specie_id no payload da API
        }));
      } catch (error) {
          this.showAppNotification('Erro ao carregar lista de animais.', 'error');
          console.error("Erro em loadAnimals:", error);
      }
    },
    openModalForAdd() {
      this.editing = false
      this.editingId = null
      this.resetForm()
      this.showModal = true
    },
    openModalForEdit(animal) {
      this.editing = true
      this.editingId = animal.id
      this.form = {
        identification: animal.identification,
        // IMPORTANTE: o serializer agora envia 'specie_id' em vez de 'specie' para o ID da espécie
        specie: animal.specie_id || this.null_placeholder_specie,
        breed: animal.breed || this.null_placeholder_breed, // 'breed' é o ID da raça
        group: animal.group || this.null_placeholder_group,
        gender: animal.gender || this.null_placeholder_gender,
        status: animal.status || this.null_placeholder_status,
        identification_type: animal.identification_type || this.null_placeholder_id_type,
        birth_date: animal.birth_date,
        observations: animal.observations
      };
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    },
    onSpecieChange() {
      this.form.breed = ''
    },
    async handleSubmit() {
      if (this.editing) {
        const updated = await updateAnimal(this.editingId, this.form)
        const idx = this.animals.findIndex(a => a.id === this.editingId)
        this.animals.splice(idx, 1, {
          ...updated,
          specie_name: this.species.find(s => s.id === updated.specie)?.name || '',
          breed_name: this.breeds.find(b => b.id === updated.breed)?.name || '',
          group_name: this.animalGroups.find(g => g.id === updated.group)?.name || ''
        })
        alert('Animal atualizado com sucesso.')
      } else {
        const created = await registerAnimal(this.form)
        this.animals.push({
          ...created,
          specie_name: this.species.find(s => s.id === created.specie)?.name || '',
          breed_name: this.breeds.find(b => b.id === created.breed)?.name || '',
          group_name: this.animalGroups.find(g => g.id === created.group)?.name || ''
        })
        alert('Animal cadastrado com sucesso.')
      }
      this.closeModal()
    },
    async handleDelete(id) {
      if (!confirm('Deseja realmente deletar este animal?')) return
      await deleteAnimal(id)
      this.animals = this.animals.filter(a => a.id !== id)
      alert('Animal deletado com sucesso.')
    },
    handleGroupChange(e) {
      if (e.target.value === 'new') {
        this.showGroupModal = true
        this.newGroup = { name: '', description: '' }
      }
    },
    async saveNewGroup() {
      const created = await registerAnimalGroup(this.newGroup)
      this.animalGroups.push(created)
      this.form.group = created.id
      this.closeGroupModal()
      alert('Grupo cadastrado com sucesso.')
    },
    closeGroupModal() {
      this.showGroupModal = false
      if (!this.editing) this.form.group = ''
    },
    resetForm() {
      this.form = {
        identification: '',
        specie: '',
        breed: '',
        group: '',
        gender: '',
        status: 1,
        identification_type: '',
        birth_date: '',
        observations: ''
      }
    }
  }
}
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
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-sm);
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
  max-height: 90vh;           /* habilita scroll interno se for maior */
  overflow-y: auto;
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
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  padding: var(--sp-sm) var(--sp-lg);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.button-secondary:hover,
.button-secondary:focus {
  background-color: var(--color-accent);
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
