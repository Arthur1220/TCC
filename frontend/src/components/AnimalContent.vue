<template>
  <div>
    <section v-if="!showGroupManager" class="content-panel animal-content-panel">
      <div class="panel-header">
        <h2 class="panel-title-text">Gerenciar Animais</h2>
        <div class="panel-actions">
          <button class="button button-primary" @click="openModalForAdd">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
            Cadastrar Animal
          </button>
          <button class="button button-secondary" @click="openGroupManager">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-3 9h-3v3h-2v-3H8V9h3V6h2v3h3v2z"/></svg>
            Gerenciar Lotes
          </button>
        </div>
      </div>
      <p class="panel-description">
        Nesta tela você pode cadastrar novos animais, visualizar, editar dados existentes ou removê-los da sua base.
      </p>

      <div v-if="isLoadingAnimals" class="loading-state">
        <p>Carregando animais...</p>
      </div>
      <div v-else-if="animals.length" class="animal-list styled-list-group">
        <ul>
          <li
            v-for="animal in animals"
            :key="animal.id"
            class="list-item card-hover"
            :data-animal-id="animal.id"
            @click="openModalForEdit(animal)"
            tabindex="0"
            @keydown.enter="openModalForEdit(animal)"
            role="button"
            :aria-label="`Ver detalhes do animal ${animal.identification}`"
          >
            <div class="item-info">
              <strong class="animal-identification">{{ animal.identification }}</strong>
              <span class="animal-detail">Espécie: {{ animal.specie_name || 'N/D' }}</span>
              <span class="animal-detail">Raça: {{ animal.breed_name || 'N/D' }}</span>
              <span class="animal-detail">Grupo: {{ animal.group_name || 'Nenhum' }}</span>
              <span class="animal-detail">Nascimento: {{ formatDate(animal.birth_date) || 'N/D' }}</span>
              <span class="animal-detail">Status: <span :class="getStatusClass(animal.status_name)">{{ animal.status_name || 'N/D' }}</span></span>
            </div>
            <div class="item-actions">
              <button class="button button-outline-primary button-sm" @click.stop="openModalForEdit(animal)">Editar</button>
              <button class="button button-danger button-sm" @click.stop="handleDelete(animal.id)">Deletar</button>
            </div>
          </li>
        </ul>
      </div>
      <div v-else class="empty-state">
        <p>Nenhum animal cadastrado ainda. Que tal <a href="#" @click.prevent="openModalForAdd" class="link">adicionar o primeiro</a>?</p>
      </div>

      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content card large-modal">
          <div class="modal-header">
            <h3 class="modal-title-text">{{ editing ? 'Editar Animal' : 'Cadastrar Novo Animal' }}</h3>
            <button @click="closeModal" class="button-close" aria-label="Fechar modal">&times;</button>
          </div>
          <form @submit.prevent="handleSubmit" class="modal-form form-grid">
            <div class="form-group full-width">
              <label for="identification" class="form-label">Identificação*</label>
              <input id="identification" v-model="form.identification" type="text" class="input" required />
            </div>

            <div class="form-group">
              <label for="specie" class="form-label">Espécie*</label>
              <select id="specie" v-model="form.specie" @change="onSpecieChange" class="select" required>
                <option disabled :value="null_placeholder_specie">Selecione a espécie</option>
                <option v-for="s in species" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="breed" class="form-label">Raça*</label>
              <select id="breed" v-model="form.breed" class="select" required :disabled="!form.specie || form.specie === null_placeholder_specie || filteredBreeds.length === 0">
                <option disabled :value="null_placeholder_breed">
                  {{ !form.specie || form.specie === null_placeholder_specie ? 'Selecione uma espécie primeiro' : (filteredBreeds.length === 0 ? 'Nenhuma raça para esta espécie' : 'Selecione a raça') }}
                </option>
                <option v-for="b in filteredBreeds" :key="b.id" :value="b.id">{{ b.name }}</option>
              </select>
            </div>

            <div class="form-group">
              <label for="group" class="form-label">Grupo / Lote</label>
              <select id="group" v-model="form.group" @change="handleGroupChange" class="select">
                <option :value="null_placeholder_group">(Sem Lote)</option>
                <option v-for="o in animalGroups" :key="o.id" :value="o.id">{{ o.name }}</option>
                <option value="new">+ Criar Novo Grupo</option>
              </select>
            </div>
            <div class="form-group">
              <label for="gender" class="form-label">Gênero*</label>
              <select id="gender" v-model="form.gender" class="select" required>
                <option disabled :value="null_placeholder_gender">Selecione o gênero</option>
                <option v-for="o in genders" :key="o.id" :value="o.id">{{ o.name }}</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="status" class="form-label">Status*</label>
              <div v-if="editing">
                <select id="status" v-model="form.status" class="select" required>
                  <option disabled :value="null_placeholder_status">Selecione o status</option>
                  <option v-for="o in statuses" :key="o.id" :value="o.id">{{ o.name }}</option>
                </select>
              </div>
              <div v-else class="status-default-display input">
                {{ defaultStatusName }}
              </div>
            </div>
            <div class="form-group">
              <label for="identification_type" class="form-label">Tipo de Identificação*</label>
              <select id="identification_type" v-model="form.identification_type" class="select" required>
                <option disabled :value="null_placeholder_id_type">Selecione o tipo</option>
                <option v-for="o in identificationTypes" :key="o.id" :value="o.id">{{ o.name }}</option>
              </select>
            </div>

            <div class="form-group full-width">
              <label for="birth_date" class="form-label">Data de Nascimento*</label>
              <input id="birth_date" v-model="form.birth_date" type="date" class="input" required />
            </div>

            <div class="form-group full-width">
              <label for="observations" class="form-label">Observações</label>
              <textarea id="observations" v-model="form.observations" class="textarea" rows="3"></textarea>
            </div>

            <div class="form-actions full-width">
              <button type="submit" class="button button-primary">
                {{ editing ? 'Atualizar Animal' : 'Cadastrar Animal' }}
              </button>
              <button type="button" class="button button-secondary" @click="closeModal">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>

      <div v-if="showGroupModal" class="modal-overlay" @click.self="closeGroupModal">
        <div class="modal-content card">
          <div class="modal-header">
            <h3 class="modal-title-text">Cadastrar Novo Grupo/Lote</h3>
            <button @click="closeGroupModal" class="button-close" aria-label="Fechar modal">&times;</button>
          </div>
          <form @submit.prevent="saveNewGroup" class="modal-form">
            <div class="form-group">
              <label for="new-group-name" class="form-label">Nome do Grupo*</label>
              <input id="new-group-name" v-model="newGroup.name" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label for="new-group-desc" class="form-label">Descrição</label>
              <input id="new-group-desc" v-model="newGroup.description" type="text" class="input" />
            </div>
            <div class="form-actions">
              <button type="submit" class="button button-primary">Salvar Grupo</button>
              <button type="button" class="button button-secondary" @click="closeGroupModal">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>

    <LotContent v-else @back="closeGroupManager" :key="lotContentKey" />

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
import LotContent from '@/components/LotContent.vue';
import NotificationModal from '@/components/NotificationModal.vue';

const DEFAULT_STATUS_NAME_LOWER = 'ativo';

export default {
  name: 'AnimalContent',
  components: { LotContent, NotificationModal },
  props: {
    searchQueryProp: {
      type: [Number, String],
      default: null
    }
  },
  data() {
    const nullPlaceholder = null; 
    return {
      showGroupManager: false,
      animals: [],
      isLoadingAnimals: true,
      form: {
        identification: '',
        specie: nullPlaceholder, 
        breed: nullPlaceholder,   
        group: nullPlaceholder,
        gender: nullPlaceholder,
        status: nullPlaceholder,
        identification_type: nullPlaceholder,
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
      showGroupModal: false,
      lotContentKey: 0,
      notification: { show: false, message: '', type: 'success' },
      null_placeholder_specie: nullPlaceholder,
      null_placeholder_breed: nullPlaceholder,
      null_placeholder_group: nullPlaceholder,
      null_placeholder_gender: nullPlaceholder,
      null_placeholder_status: nullPlaceholder,
      null_placeholder_id_type: nullPlaceholder,
    };
  },
  computed: {
    filteredBreeds() {
      // console.log("[DEBUG] Recalculando filteredBreeds...");
      // console.log("[DEBUG] form.specie atual:", this.form.specie, "(tipo:", typeof this.form.specie, ")");
      // console.log("[DEBUG] Lista this.breeds (primeiros 5):", JSON.parse(JSON.stringify(this.breeds.slice(0,5))));

      if (this.form.specie === this.null_placeholder_specie || this.form.specie === null || !this.breeds.length) {
        // console.log("[DEBUG] filteredBreeds: Retornando array vazio (sem espécie selecionada ou sem raças carregadas)");
        return [];
      }
      const currentSpecieId = Number(this.form.specie);
      const filtered = this.breeds.filter(breed => {
        // *** CORREÇÃO APLICADA AQUI ***
        // Acessa o ID da espécie dentro do objeto aninhado 'breed.specie.id'
        const breedSpecieFkObject = breed.specie; 

        // console.log(`[DEBUG] Filtrando Raça: '${breed.name}' (ID: ${breed.id}). Objeto specie da raça:`, JSON.parse(JSON.stringify(breedSpecieFkObject)), `Comparando com ID de espécie selecionada: ${currentSpecieId}`);
        
        // Verifica se breedSpecieFkObject existe e tem a propriedade 'id'
        if (breedSpecieFkObject && typeof breedSpecieFkObject === 'object' && breedSpecieFkObject.hasOwnProperty('id')) {
          return Number(breedSpecieFkObject.id) === currentSpecieId;
        }
        // Se a estrutura for diferente (ex: breed.specie já é o ID), descomente o log acima para ver e ajuste aqui.
        // console.warn(`[DEBUG] Raça '${breed.name}' não possui 'specie.id' esperado. Objeto specie:`, breedSpecieFkObject);
        return false; 
      });
      // console.log("[DEBUG] filteredBreeds resultado para espécie ID " + currentSpecieId + ":", JSON.parse(JSON.stringify(filtered)));
      return filtered;
    },
    defaultStatusName() {
      const activeStatus = this.statuses.find(s => s.name && s.name.toLowerCase() === DEFAULT_STATUS_NAME_LOWER);
      return activeStatus ? activeStatus.name : 'Ativo (Padrão)';
    },
    defaultStatusId() {
      const activeStatus = this.statuses.find(s => s.name && s.name.toLowerCase() === DEFAULT_STATUS_NAME_LOWER);
      return activeStatus ? activeStatus.id : null;
    }
  },
  watch: {
      searchQueryProp(newVal) {
          if (newVal && this.animals.length > 0) { 
              this.findAndOpenAnimal(newVal);
          }
      },
      // 'form.breed'(newVal, oldVal) {
      //   console.log(`[DEBUG] form.breed (v-model) mudou de ${oldVal} para ${newVal}`);
      // }
  },
  async created() {
    // console.log("[DEBUG] Componente AnimalContent - CREATED hook iniciado.");
    await this.loadLookups(); 
    this.setDefaultStatusInForm(); 
    await this.loadAnimals();    

    if (this.searchQueryProp) {
        this.findAndOpenAnimal(this.searchQueryProp);
    }
    // console.log("[DEBUG] Componente AnimalContent - CREATED hook finalizado.");
  },
  methods: {
    findAndOpenAnimal(query) {
        const animalToEdit = this.animals.find(a => String(a.id) === String(query) || a.identification === query);
        if (animalToEdit) {
            this.openModalForEdit(animalToEdit);
        } else {
            // this.showAppNotification(`Animal com ID/Identificação "${query}" não encontrado na lista atual.`, 'info');
            // console.warn(`[DEBUG] Animal com ID/Identificação "${query}" não encontrado na lista atual para edição via prop.`);
        }
    },
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
        if (!dateString) return null;
        if (/^\d{2}\/\d{2}\/\d{4}$/.test(dateString)) {
            return dateString;
        }
        const dateParts = dateString.split('-');
        if (dateParts.length === 3) {
            return `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
        }
        return dateString; 
    },
    getStatusClass(statusName) {
        if (!statusName) return 'status-default';
        const nameLower = statusName.toLowerCase();
        if (nameLower === 'ativo') return 'status-badge status-active';
        if (nameLower === 'vendido') return 'status-badge status-sold';
        if (nameLower === 'abatido') return 'status-badge status-slaughtered';
        if (nameLower === 'morto') return 'status-badge status-dead';
        return 'status-badge status-default';
    },
    openGroupManager() {
      this.showGroupManager = true;
      this.lotContentKey++;
    },
    closeGroupManager() {
      this.showGroupManager = false;
      this.loadAnimals(); 
      this.loadLookups();
    },
    async loadLookups() {
      // console.log("[DEBUG] loadLookups: Iniciando carregamento de dados de referência...");
      try {
        const [species, breeds, animalGroups, genders, statuses, identificationTypes] = await Promise.all([
          getSpecies(), getBreeds(), getAnimalGroups(),
          getGenders(), getStatuses(), getIdentificationTypes()
        ]);
        this.species = species.sort((a,b) => a.name.localeCompare(b.name));
        this.breeds = breeds.sort((a,b) => a.name.localeCompare(b.name)); 
        this.animalGroups = animalGroups.sort((a,b) => a.name.localeCompare(b.name));
        this.genders = genders.sort((a,b) => a.name.localeCompare(b.name));
        this.statuses = statuses.sort((a,b) => a.name.localeCompare(b.name));
        this.identificationTypes = identificationTypes.sort((a,b) => a.name.localeCompare(b.name));

        // console.log("[DEBUG] loadLookups: Espécies carregadas:", JSON.parse(JSON.stringify(this.species)));
        // console.log("[DEBUG] loadLookups: TODAS as Raças carregadas (this.breeds) - primeiros 5:", JSON.parse(JSON.stringify(this.breeds.slice(0,5))));
        // if (this.breeds.length > 0) {
        //     console.log("[DEBUG] loadLookups: Exemplo de objeto de Raça (primeiro item de this.breeds):", JSON.parse(JSON.stringify(this.breeds[0])));
        // }

      } catch (error) {
          this.showAppNotification('Erro ao carregar dados de referência.', 'error');
          console.error("Erro em loadLookups (AnimalContent):", error);
      }
      // console.log("[DEBUG] loadLookups: Finalizado.");
    },
    setDefaultStatusInForm() {
      this.form.status = this.defaultStatusId || this.null_placeholder_status;
    },
    async loadAnimals() {
      this.isLoadingAnimals = true;
      // console.log("[DEBUG] loadAnimals: Iniciando carregamento de animais...");
      try {
        const list = await getAnimals();
        this.animals = list.map(a => ({
          ...a,
          specie_name: a.specie_name || this.species.find(s => s.id === a.specie_id)?.name || 'N/D',
          breed_name: a.breed_name || this.breeds.find(b => b.id === a.breed)?.name || 'N/D',
          group_name: a.group_name || this.animalGroups.find(g => g.id === a.group)?.name || 'Nenhum',
          status_name: a.status_name || this.statuses.find(s => s.id === a.status)?.name || 'N/D',
        })).sort((a, b) => a.identification.localeCompare(b.identification));
        // console.log("[DEBUG] loadAnimals: Animais carregados e mapeados (primeiro):", this.animals.length > 0 ? JSON.parse(JSON.stringify(this.animals[0])) : "Nenhum animal");
      } catch (error) {
          this.showAppNotification('Erro ao carregar lista de animais.', 'error');
          console.error("Erro em loadAnimals (AnimalContent):", error);
      } finally {
          this.isLoadingAnimals = false;
          // console.log("[DEBUG] loadAnimals: Finalizado.");
      }
    },
    openModalForAdd() {
      // console.log("[DEBUG] openModalForAdd: Abrindo modal para adicionar.");
      this.editing = false;
      this.editingId = null;
      this.resetForm();
      this.showModal = true;
      // console.log("[DEBUG] openModalForAdd: Estado inicial do form:", JSON.parse(JSON.stringify(this.form)));
    },
    openModalForEdit(animal) {
      this.editing = true;
      this.editingId = animal.id;

      // console.log("[DEBUG] openModalForEdit: Abrindo modal para editar animal:", JSON.parse(JSON.stringify(animal)));
      // console.log("[DEBUG] openModalForEdit: animal.specie_id:", animal.specie_id, "(tipo:", typeof animal.specie_id, ")");
      // console.log("[DEBUG] openModalForEdit: animal.breed (ID da raça):", animal.breed, "(tipo:", typeof animal.breed, ")");

      this.form = {
        identification: animal.identification,
        specie: animal.specie_id !== undefined && animal.specie_id !== null ? Number(animal.specie_id) : this.null_placeholder_specie,
        breed: animal.breed !== undefined && animal.breed !== null ? Number(animal.breed) : this.null_placeholder_breed,
        group: animal.group !== undefined && animal.group !== null ? Number(animal.group) : this.null_placeholder_group,
        gender: animal.gender !== undefined && animal.gender !== null ? Number(animal.gender) : this.null_placeholder_gender,
        status: animal.status !== undefined && animal.status !== null ? Number(animal.status) : this.null_placeholder_status,
        identification_type: animal.identification_type !== undefined && animal.identification_type !== null ? Number(animal.identification_type) : this.null_placeholder_id_type,
        birth_date: animal.birth_date,
        observations: animal.observations || ''
      };
      
      // console.log("[DEBUG] openModalForEdit: Form após atribuição inicial:", JSON.parse(JSON.stringify(this.form)));
      
      this.$nextTick(() => {
        // console.log("[DEBUG] openModalForEdit ($nextTick): form.specie:", this.form.specie);
        const breedsForCurrentSpecie = this.filteredBreeds; 
        // console.log("[DEBUG] openModalForEdit ($nextTick): filteredBreeds recalculada:", JSON.parse(JSON.stringify(breedsForCurrentSpecie)));
        
        const targetBreedId = animal.breed !== undefined && animal.breed !== null ? Number(animal.breed) : this.null_placeholder_breed;
        // console.log("[DEBUG] openModalForEdit ($nextTick): Tentando selecionar breed ID:", targetBreedId);

        if (breedsForCurrentSpecie.some(b => b.id === targetBreedId)) {
            this.form.breed = targetBreedId; 
            // console.log("[DEBUG] openModalForEdit ($nextTick): Raça ID", targetBreedId, "encontrada e atribuída ao form.breed.");
        } else {
            this.form.breed = this.null_placeholder_breed; 
            // console.warn("[DEBUG] openModalForEdit ($nextTick): Raça ID", targetBreedId, "NÃO encontrada na lista filteredBreeds. Definindo form.breed como placeholder.");
        }
        // console.log("[DEBUG] openModalForEdit ($nextTick): Form APÓS tentativa de ajuste da raça:", JSON.parse(JSON.stringify(this.form)));
      });

      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    onSpecieChange() {
      // console.log("[DEBUG] onSpecieChange - form.specie selecionado:", this.form.specie, "(tipo:", typeof this.form.specie, ")");
      this.form.breed = this.null_placeholder_breed; 
    },
    async handleSubmit() {
      if (!this.form.identification || this.form.specie === this.null_placeholder_specie || this.form.breed === this.null_placeholder_breed || this.form.gender === this.null_placeholder_gender || this.form.status === this.null_placeholder_status || this.form.identification_type === this.null_placeholder_id_type || !this.form.birth_date) {
          this.showAppNotification('Preencha todos os campos obrigatórios (*).', 'error');
          return;
      }
      const payload = { ...this.form };
      
      // console.log("[DEBUG] handleSubmit: Payload a ser enviado:", JSON.parse(JSON.stringify(payload)));

      try {
        let apiResponse;
        if (this.editing) {
          apiResponse = await updateAnimal(this.editingId, payload);
          this.showAppNotification('Animal atualizado com sucesso!', 'success');
        } else {
          apiResponse = await registerAnimal(payload);
          this.showAppNotification('Animal cadastrado com sucesso!', 'success');
        }
        this.closeModal(); 
        await this.loadAnimals();
      } catch (error) {
        console.error("Erro ao salvar animal:", error.response?.data || error);
        let errorMessage = (this.editing ? 'Erro ao atualizar animal: ' : 'Erro ao cadastrar animal: ');
        if (error.response && error.response.data && typeof error.response.data === 'object') {
            const errors = error.response.data;
            errorMessage += Object.entries(errors)
                .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                .join('; ');
        } else if (error.response && error.response.data) {
            errorMessage += error.response.data;
        } else {
            errorMessage += error.message || 'Erro desconhecido.';
        }
        this.showAppNotification(errorMessage, 'error');
      }
    },
    async handleDelete(id) {
      if (!confirm('Deseja realmente deletar este animal? Esta ação não pode ser desfeita e deletará também todos os eventos associados.')) return;
      try {
        await deleteAnimal(id);
        await this.loadAnimals(); 
        this.showAppNotification('Animal deletado com sucesso.', 'success');
      } catch (error) {
          this.showAppNotification('Erro ao deletar animal.', 'error');
          console.error("Erro ao deletar animal:", error.response?.data || error);
      }
    },
    handleGroupChange(event) {
      const selectedValue = event.target.value;
      if (selectedValue === 'new') {
        this.showGroupModal = true;
        this.newGroup = { name: '', description: '' };
      } else if (selectedValue === String(this.null_placeholder_group) || selectedValue === "") {
        this.form.group = this.null_placeholder_group;
      } else {
        this.form.group = parseInt(selectedValue, 10);
      }
    },
    async saveNewGroup() {
      if (!this.newGroup.name || !this.newGroup.name.trim()) {
          this.showAppNotification('O nome do grupo é obrigatório.', 'error');
          return;
      }
      try {
        const createdGroup = await registerAnimalGroup(this.newGroup);
        this.animalGroups.push(createdGroup);
        this.animalGroups.sort((a,b) => a.name.localeCompare(b.name));
        this.form.group = createdGroup.id; 
        this.closeGroupModal();
        this.showAppNotification('Grupo cadastrado com sucesso.', 'success');
      } catch (error) {
        this.showAppNotification('Erro ao salvar novo grupo.', 'error');
        console.error("Erro ao salvar novo grupo:", error.response?.data || error);
      }
    },
    closeGroupModal() {
      this.showGroupModal = false;
      if (String(this.form.group) === 'new') { 
          this.form.group = this.null_placeholder_group;
      }
    },
    resetForm() {
      this.form = {
        identification: '',
        specie: this.null_placeholder_specie,
        breed: this.null_placeholder_breed,
        group: this.null_placeholder_group,
        gender: this.null_placeholder_gender,
        status: this.defaultStatusId || this.null_placeholder_status,
        identification_type: this.null_placeholder_id_type,
        birth_date: '',
        observations: ''
      };
      // console.log("[DEBUG] resetForm: Form resetado para:", JSON.parse(JSON.stringify(this.form)));
    }
  }
}
</script>

<style scoped>
/* Seu CSS Scoped Existente */
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
.panel-actions {
  display: flex;
  gap: var(--sp-sm);
}
.panel-actions .button {
    font-size: var(--fs-small);
    padding: var(--sp-xs) var(--sp-sm);
    display: flex;
    align-items: center;
    gap: var(--sp-xs);
}
.panel-actions .button svg {
    margin-right: 0;
}

.panel-description {
  text-align: left;
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
  max-width: none;
}

.animal-list {
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
  cursor: pointer;
}
.list-item.card-hover:hover, .list-item.card-hover:focus-within {
    border-color: var(--color-primary-light);
    box-shadow: var(--shadow);
    transform: translateY(-2px);
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--sp-xxs);
}
.animal-identification {
    font-size: var(--fs-large);
    font-weight: var(--fw-semibold);
    color: var(--color-primary);
    margin-bottom: var(--sp-xs);
}
.animal-detail {
    font-size: var(--fs-small);
    color: var(--color-text-secondary);
}
.animal-detail .status-badge {
    font-size: var(--fs-smaller);
    padding: calc(var(--sp-xxs) / 2) var(--sp-xs);
    border-radius: var(--border-radius-pill);
    font-weight: var(--fw-medium);
    color: var(--color-text-inverted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block; 
    line-height: 1.2; 
}
.status-active { background-color: var(--color-success); }
.status-sold { background-color: var(--color-danger); }
.status-slaughtered { background-color: var(--color-info); }
.status-dead { background-color: var(--color-text-muted); }
.status-default { background-color: var(--color-secondary); }


.item-actions {
  display: flex;
  gap: var(--sp-xs);
}
.item-actions .button {
    font-size: var(--fs-small);
    padding: var(--sp-xs) var(--sp-sm);
}

.empty-state {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--sp-xl) var(--sp-md);
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius);
  font-size: var(--fs-base);
}
.empty-state p .link {
    font-weight: var(--fw-medium);
}

.modal-content.large-modal {
    max-width: 800px;
}

.status-default-display {
    background-color: var(--color-bg-disabled);
    color: var(--color-text-muted);
    padding: var(--sp-sm) var(--sp-md);
    border-radius: var(--border-radius);
    border: var(--border-width) solid var(--color-border);
    cursor: not-allowed;
    font-size: var(--fs-base); 
    line-height: var(--lh-base); 
    width: 100%;
    display: block;
}
.loading-state {
    text-align: center;
    padding: var(--sp-xl);
    color: var(--color-text-muted);
    font-size: var(--fs-large);
}
</style>