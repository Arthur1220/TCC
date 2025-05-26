<template>
  <section class="content-panel">
    <div class="header-row">
      <button class="back-button" @click="goBack">
        ← Voltar aos Animais
      </button>
      <h2 class="panel-title">Gerenciar Lotes</h2>
    </div>

    <div v-if="groups.length" class="cards-grid">
      <div
        v-for="group in groups"
        :key="group.id"
        class="group-card"
        @click="openGroup(group)"
        tabindex="0"
      >
        <div class="card-header">
          <h3>{{ group.name }}</h3>
        </div>
        <div class="card-body">
          <p>{{ groupAnimalsMap[group.id] }} animais</p>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>Nenhum lote cadastrado.</p>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content large-modal">
        <h3 class="modal-title">
          Animais do Lote “{{ selectedGroup ? selectedGroup.name : '' }}”
        </h3>

        <div class="batch-actions-header">
          <button v-if="selectedAnimalIdsForBatch.length > 0" class="button-secondary" @click="openBatchUpdateModal">
            Editar em Lote ({{ selectedAnimalIdsForBatch.length }})
          </button>
          <button v-else class="button-secondary" disabled>
            Editar em Lote
          </button>
        </div>

        <ul class="modal-list">
          <li v-for="animal in selectedAnimals" :key="animal.id">
            <input type="checkbox" :value="animal.id" v-model="selectedAnimalIdsForBatch" />
            <div class="animal-info">
              <span class="animal-id">{{ animal.identification }}</span> -
              Status: <span :class="getStatusClass(animal.status)">{{ getStatusName(animal.status) }}</span> -
              Grupo: {{ getGroupName(animal.group) }} -
              Tipo ID: {{ getIdentificationTypeName(animal.identification_type) }} -
              Raça: {{ getBreedName(animal.breed) }} (Espécie: {{ getSpecieName(animal.specie) }})
            </div>
          </li>
        </ul>
        <div class="form-actions">
          <button class="button-primary" @click="closeModal">
            Fechar
          </button>
        </div>
      </div>
    </div>

    <div v-if="showBatchUpdateModal" class="modal-overlay" @click.self="closeBatchUpdateModal">
      <div class="modal-content">
        <h3 class="modal-title">Atualizar em Lote</h3>
        <p v-if="selectedAnimalIdsForBatch.length">
          Você selecionou **{{ selectedAnimalIdsForBatch.length }} animal(is)** para atualização.
        </p>

        <div class="form-group">
          <label for="batch-update-type">O que deseja atualizar?</label>
          <select id="batch-update-type" v-model="batchUpdateType" @change="resetBatchUpdateValue">
            <option disabled value="">Selecione um tipo de atualização</option>
            <option value="status">Status</option>
            <option value="group">Grupo/Lote</option>
            <option value="identification_type">Tipo de Identificação</option>
            <option value="breed">Raça</option>
          </select>
        </div>

        <div class="form-group" v-if="batchUpdateType === 'status'">
          <label for="batch-status">Novo Status:</label>
          <select id="batch-status" v-model="newBatchValue.status_id" required>
            <option disabled value="">Selecione um status</option>
            <option v-for="s in statuses" :key="s.id" :value="s.id">
              {{ s.name }}
            </option>
          </select>
        </div>

        <div class="form-group" v-else-if="batchUpdateType === 'group'">
          <label for="batch-group">Novo Grupo/Lote:</label>
          <select id="batch-group" v-model="newBatchValue.group_id">
            <option value="">(Remover de Lote)</option>
            <option v-for="g in animalGroups" :key="g.id" :value="g.id">
              {{ g.name }}
            </option>
          </select>
        </div>

        <div class="form-group" v-else-if="batchUpdateType === 'identification_type'">
          <label for="batch-identification-type">Novo Tipo de Identificação:</label>
          <select id="batch-identification-type" v-model="newBatchValue.identification_type_id" required>
            <option disabled value="">Selecione um tipo</option>
            <option v-for="it in identificationTypes" :key="it.id" :value="it.id">
              {{ it.name }}
            </option>
          </select>
        </div>

        <div class="form-group" v-else-if="batchUpdateType === 'breed'">
          <label for="batch-specie">Espécie (para filtrar raças):</label>
          <select id="batch-specie" v-model="selectedSpecieForBreedFilter" @change="onSpecieForBreedFilterChange">
            <option value="">Todas as Espécies</option>
            <option v-for="s in species" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>

          <label for="batch-breed">Nova Raça:</label>
          <select id="batch-breed" v-model="newBatchValue.breed_id" required>
            <option value="">(Remover Raça)</option>
            <option
              v-for="b in filteredBreedsForBatch"
              :key="b.id"
              :value="b.id"
            >
              {{ b.name }}
            </option>
          </select>
        </div>

        <div class="form-actions">
          <button class="button-primary" @click="handleBatchUpdate">
            Aplicar Mudanças
          </button>
          <button type="button" class="button-secondary" @click="closeBatchUpdateModal">
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <NotificationModal
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
      @close="notification.show = false"
    />
  </section>
</template>

<script>
import { getAnimals, updateAnimalsBatch } from '@/services/animalService';
import { getAnimalGroups, getStatuses, getIdentificationTypes, getBreeds, getSpecies } from '@/services/lookupService';
import NotificationModal from '@/components/NotificationModal.vue'; // Importa o novo componente

export default {
  name: 'LotContent',
  components: {
    NotificationModal // Registra o componente
  },
  data() {
    return {
      groups: [],
      groupAnimalsMap: {},
      showModal: false,
      selectedGroup: null,
      selectedAnimals: [],
      selectedAnimalIdsForBatch: [],

      showBatchUpdateModal: false,
      batchUpdateType: '',
      newBatchValue: {
        status_id: null,
        group_id: null,
        identification_type_id: null,
        breed_id: null,
        specie_id: null,
      },
      selectedSpecieForBreedFilter: '',

      statuses: [],
      animalGroups: [],
      identificationTypes: [],
      breeds: [],
      species: [],

      // Dados para o modal de notificação
      notification: {
        show: false,
        message: '',
        type: 'success' // ou 'error'
      }
    }
  },
  async created() {
    await this.loadLookupsForBatchUpdate();
    await this.loadInitialData();
  },
  computed: {
    filteredBreedsForBatch() {
        if (!this.selectedSpecieForBreedFilter) {
            return this.breeds;
        }
        return this.breeds.filter(b => b.specie === this.selectedSpecieForBreedFilter);
    }
  },
  methods: {
    async loadInitialData() {
      try {
        this.groups = await getAnimalGroups();
        await this.loadAnimalsCount();
      } catch (e) {
        console.error('Erro ao carregar lotes:', e);
        this.showNotification('Erro ao carregar lotes.', 'error');
      }
    },
    async loadLookupsForBatchUpdate() {
        try {
            this.statuses = await getStatuses();
            this.animalGroups = await getAnimalGroups();
            this.identificationTypes = await getIdentificationTypes();
            this.breeds = await getBreeds();
            this.species = await getSpecies();
        } catch (e) {
            console.error('Erro ao carregar dados de lookup:', e);
            this.showNotification('Erro ao carregar dados de lookup.', 'error');
        }
    },
    async loadAnimalsCount() {
      for (const g of this.groups) {
        try {
          const list = await getAnimals({ group: g.id });
          this.$set(this.groupAnimalsMap, g.id, list.length);
        } catch {
          this.$set(this.groupAnimalsMap, g.id, 0);
        }
      }
    },
    async openGroup(group) {
      this.selectedGroup = group;
      this.selectedAnimalIdsForBatch = [];
      try {
        this.selectedAnimals = await getAnimals({ group: group.id });
      } catch (e) {
        console.error('Erro ao carregar animais do lote:', e);
        this.selectedAnimals = [];
        this.showNotification('Erro ao carregar animais do lote.', 'error');
      }
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedGroup = null;
      this.selectedAnimals = [];
      this.selectedAnimalIdsForBatch = [];
    },
    goBack() {
      this.$emit('back');
    },

    openBatchUpdateModal() {
        if (this.selectedAnimalIdsForBatch.length === 0) {
            this.showNotification('Por favor, selecione pelo menos um animal para atualizar.', 'error');
            return;
        }
        this.batchUpdateType = '';
        this.resetBatchUpdateValue();
        this.selectedSpecieForBreedFilter = '';
        this.showBatchUpdateModal = true;
    },
    closeBatchUpdateModal() {
      this.showBatchUpdateModal = false;
    },
    resetBatchUpdateValue() {
        this.newBatchValue = {
            status_id: null,
            group_id: null,
            identification_type_id: null,
            breed_id: null,
            specie_id: null,
        };
        this.selectedSpecieForBreedFilter = '';
    },
    onSpecieForBreedFilterChange() {
        this.newBatchValue.breed_id = null;
    },

    async handleBatchUpdate() {
        if (this.selectedAnimalIdsForBatch.length === 0) {
            this.showNotification('Nenhum animal selecionado para atualização.', 'error');
            return;
        }

        let updatePayload = {};
        let successMessage = '';
        let errorMessage = '';

        switch (this.batchUpdateType) {
            case 'status':
                if (this.newBatchValue.status_id === null) { // Usar null para verificar se algo foi selecionado
                    this.showNotification('Por favor, selecione um novo status.', 'error');
                    return;
                }
                updatePayload = { new_status_id: this.newBatchValue.status_id };
                successMessage = 'Status';
                errorMessage = 'status';
                break;
            case 'group':
                updatePayload = { new_group_id: this.newBatchValue.group_id || null };
                successMessage = 'Grupo/Lote';
                errorMessage = 'grupo/lote';
                break;
            case 'identification_type':
                if (this.newBatchValue.identification_type_id === null) {
                    this.showNotification('Por favor, selecione um novo tipo de identificação.', 'error');
                    return;
                }
                updatePayload = { new_identification_type_id: this.newBatchValue.identification_type_id };
                successMessage = 'Tipo de Identificação';
                errorMessage = 'tipo de identificação';
                break;
            case 'breed':
                updatePayload = { new_breed_id: this.newBatchValue.breed_id || null };

                if (this.newBatchValue.breed_id) {
                    const selectedBreed = this.breeds.find(b => b.id === this.newBatchValue.breed_id);
                    if (selectedBreed) {
                        updatePayload.new_specie_id = selectedBreed.specie;
                    }
                } else {
                    updatePayload.new_specie_id = null;
                }

                successMessage = 'Raça e Espécie';
                errorMessage = 'raça e espécie';
                break;
            default:
                this.showNotification('Selecione um tipo de atualização e um valor válido.', 'error');
                return;
        }

        try {
            const response = await updateAnimalsBatch(
                this.selectedAnimalIdsForBatch,
                updatePayload
            );
            this.showNotification(`${response.updated_animals_count} animais tiveram o(a) ${successMessage.toLowerCase()} atualizado(s) com sucesso!`, 'success');

            this.closeBatchUpdateModal();
            this.closeModal();

            await this.loadInitialData();

        } catch (error) {
            this.showNotification(`Erro ao atualizar ${errorMessage} em lote: ` + (error.response?.data?.error || error.message), 'error');
        }
    },

    // Novo método para exibir o modal de notificação
    showNotification(message, type) {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      setTimeout(() => {
        this.notification.show = false;
      }, 3000); // 3 segundos
    },

    getStatusName(statusId) {
        const status = this.statuses.find(s => s.id === statusId);
        return status ? status.name : 'Desconhecido';
    },
    getStatusClass(statusId) {
        const statusName = this.getStatusName(statusId).toLowerCase();
        if (statusName === 'ativo') return 'status-active';
        if (statusName === 'vendido') return 'status-sold';
        return 'status-default';
    },
    getGroupName(groupId) {
        if (!groupId) return 'Nenhum Lote';
        const group = this.animalGroups.find(g => g.id === groupId);
        return group ? group.name : 'Desconhecido';
    },
    getIdentificationTypeName(typeId) {
        const type = this.identificationTypes.find(it => it.id === typeId);
        return type ? type.name : 'Desconhecido';
    },
    getBreedName(breedId) {
        if (!breedId) return 'Nenhuma Raça';
        const breed = this.breeds.find(b => b.id === breedId);
        return breed ? breed.name : 'Desconhecido';
    },
    getSpecieName(specieId) {
        if (!specieId) return 'Nenhuma Espécie';
        const specie = this.species.find(s => s.id === specieId);
        return specie ? specie.name : 'Desconhecida';
    }
  }
}
</script>

<style scoped>
/* Variáveis CSS para um tema mais limpo */
:root {
  --color-primary: #4CAF50; /* Verde principal */
  --color-accent: #FF9800; /* Laranja de destaque */
  --color-secondary: #757575; /* Cinza secundário */
  --color-dark-gray: #333333;
  --color-light-gray: #eeeeee;
  --color-border: #e0e0e0;
  --color-white: #ffffff;
  --color-bg: #f9f9f9; /* Fundo mais claro */
  --color-success: #4CAF50;
  --color-danger: #F44336; /* Vermelho para erros/vendido */

  --sp-xs: 4px;
  --sp-sm: 8px;
  --sp-md: 16px;
  --sp-lg: 24px;
  --sp-xl: 32px;

  --font-heading: 'Roboto', sans-serif;
  --font-body: 'Open Sans', sans-serif;
  --font-size-small: 0.875rem;
  --font-size-base: 1rem;
}

body {
  font-family: var(--font-body);
  margin: 0;
  background-color: var(--color-bg);
  color: var(--color-dark-gray);
}

.content-panel {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Sombra mais suave */
  margin-bottom: var(--sp-xl);
}
.header-row {
  display: flex;
  align-items: center;
  gap: var(--sp-md);
  margin-bottom: var(--sp-lg);
  padding-bottom: var(--sp-md);
  border-bottom: 1px solid var(--color-light-gray);
}
.header-row .panel-title {
  flex: 1;
  margin: 0;
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
  font-size: 1.8rem; /* Título maior */
  font-weight: 700;
}
.back-button {
  background: none;
  border: none;
  color: var(--color-secondary); /* Cor mais neutra */
  font-size: 1rem;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: var(--sp-sm);
  border-radius: var(--sp-sm);
}
.back-button:hover {
  color: var(--color-primary);
  background-color: var(--color-light-gray);
}
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill,minmax(200px,1fr)); /* Cards um pouco maiores */
  gap: var(--sp-lg);
  padding: var(--sp-md) 0;
}
.group-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: var(--sp-md);
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 120px; /* Altura mínima para cards */
}
.group-card:hover,
.group-card:focus {
  transform: translateY(-5px); /* Mais destaque no hover */
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  outline: none;
}
.card-header h3 {
  margin: 0;
  font-size: 1.3rem; /* Título do card maior */
  color: var(--color-primary);
  font-weight: 600;
  margin-bottom: var(--sp-sm);
}
.card-body p {
  margin: var(--sp-xs) 0 0;
  font-size: var(--font-size-base);
  color: var(--color-secondary);
}
.empty-state {
  text-align: center;
  color: var(--color-secondary);
  padding: var(--sp-xl) 0;
  font-size: 1.1rem;
}

/* Estilos de Modal */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); /* Fundo mais escuro para modals */
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(3px); /* Efeito de blur no fundo */
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%; max-width: 500px; /* Largura padrão para modals */
  box-shadow: 0 8px 24px rgba(0,0,0,0.2); /* Sombra mais forte */
  text-align: center;
  position: relative;
  animation: fadeInScale 0.3s ease-out; /* Animação de entrada */
}
.large-modal {
  max-width: 900px; /* Aumenta a largura do modal de animais do lote */
}
.modal-title {
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
  font-size: 1.5rem;
  font-weight: 700;
  border-bottom: 1px solid var(--color-light-gray);
  padding-bottom: var(--sp-sm);
}
.modal-list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--sp-md);
  max-height: 350px; /* Altura maior para a lista de animais */
  overflow-y: auto;
  border: 1px solid var(--color-border); /* Borda ao redor da lista */
  border-radius: var(--sp-sm);
  text-align: left;
  background-color: var(--color-bg); /* Fundo da lista */
}
.modal-list li {
  padding: var(--sp-sm) var(--sp-md);
  border-bottom: 1px solid var(--color-light-gray);
  font-size: var(--font-size-base);
  color: var(--color-dark-gray);
  display: flex;
  align-items: center;
  gap: var(--sp-sm);
  background-color: var(--color-white);
  transition: background-color 0.2s ease-in-out;
}
.modal-list li:hover {
  background-color: var(--color-light-gray);
}
.modal-list li:last-child {
  border-bottom: none;
}

/* Estilos para o Checkbox e Info do Animal */
.modal-list li input[type="checkbox"] {
  transform: scale(1.2); /* Checkbox um pouco maior */
  cursor: pointer;
}
.animal-info {
  flex: 1;
  text-align: left;
  white-space: normal; /* Permite quebras de linha no info para melhor leitura */
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4; /* Espaçamento entre linhas */
}
.animal-info .animal-id {
  font-weight: bold;
  color: var(--color-primary);
}

/* Estilos de Botões */
.button-primary, .button-secondary {
  padding: var(--sp-sm) var(--sp-lg);
  border-radius: var(--sp-sm);
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
}
.button-primary {
  background-color: var(--color-primary);
  color: var(--color-white);
  border: 2px solid var(--color-primary);
}
.button-primary:hover, .button-primary:focus {
  background-color: #43A047; /* Um tom mais escuro de verde */
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
  transform: translateY(-2px);
}
.button-secondary {
  background-color: var(--color-white);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
}
.button-secondary:hover, .button-secondary:focus {
  background-color: var(--color-accent);
  color: var(--color-white);
  box-shadow: 0 4px 10px rgba(255, 152, 0, 0.3);
  transform: translateY(-2px);
}
.button-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--color-light-gray);
  border-color: var(--color-border);
  color: var(--color-secondary);
  transform: none;
  box-shadow: none;
}

.batch-actions-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: var(--sp-md);
  padding-bottom: var(--sp-sm);
  border-bottom: 1px solid var(--color-light-gray);
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--sp-sm); /* Espaçamento menor entre label e input */
  margin-top: var(--sp-md);
  text-align: left;
}
.form-group label {
  font-weight: 600;
  color: var(--color-dark-gray);
  font-size: 0.95rem;
}
.form-group select {
  padding: var(--sp-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  width: 100%;
  font-size: var(--font-size-base);
  background-color: var(--color-white);
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
  appearance: none; /* Remove a seta padrão */
  background-image: url('data:image/svg+xml;utf8,<svg fill="%23757575" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/><path d="M0 0h24v24H0z" fill="none"/></svg>');
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 20px;
}
.form-group select:focus {
  border-color: var(--color-accent);
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 152, 0, 0.2);
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-sm);
  margin-top: var(--sp-lg);
  padding-top: var(--sp-md);
  border-top: 1px solid var(--color-light-gray);
}

/* Animações */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Classes para status de animais */
.status-active {
  color: var(--color-success);
  font-weight: bold;
}
.status-sold {
  color: var(--color-danger);
  font-weight: bold;
}
.status-default {
  color: var(--color-secondary);
}
</style>