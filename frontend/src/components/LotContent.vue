<template>
  <section class="content-panel lot-content-panel">
    <div class="panel-header"> <button class="button button-outline-secondary button-sm back-button-styled" @click="goBack">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
        Voltar
      </button>
      <h2 class="panel-title-text">Gerenciar Lotes (Grupos de Animais)</h2>
    </div>
    <p class="panel-description">
      Visualize os lotes existentes, veja os animais em cada lote e realize edições em massa.
    </p>

    <div v-if="isLoadingGroups" class="loading-state">
        <p>Carregando lotes...</p>
    </div>
    <div v-else-if="groups.length" class="cards-grid">
      <div
        v-for="group in groups"
        :key="group.id"
        class="group-card card card-interactive" 
        @click="openGroupDetailsModal(group)"
        tabindex="0"
        @keydown.enter="openGroupDetailsModal(group)"
        :aria-label="`Ver detalhes do lote ${group.name}`"
      >
        <div class="card-header-custom"> <h3 class="group-card-title">{{ group.name }}</h3>
        </div>
        <div class="card-body-custom">
          <p class="group-animal-count">{{ groupAnimalsMap[group.id] || 0 }} animais</p>
          <p class="group-description">{{ group.description || 'Sem descrição.' }}</p>
        </div>
        <div class="card-footer-actions">
            <button class="button button-outline-primary button-sm" @click.stop="openGroupDetailsModal(group)">Ver Animais</button>
            </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>Nenhum lote cadastrado.</p>
      </div>

    <div v-if="showGroupDetailsModal" class="modal-overlay" @click.self="closeGroupDetailsModal">
      <div class="modal-content card large-modal">
        <div class="modal-header">
            <h3 class="modal-title-text">
            Animais do Lote: {{ selectedGroup ? selectedGroup.name : '' }}
            </h3>
            <button @click="closeGroupDetailsModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <div class="modal-body">
            <div class="batch-actions-bar">
                <span>{{ selectedAnimalIdsForBatch.length }} animal(is) selecionado(s)</span>
                <button 
                    class="button button-primary button-sm" 
                    @click="openBatchUpdateModal"
                    :disabled="selectedAnimalIdsForBatch.length === 0"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
                    Editar Selecionados
                </button>
            </div>

            <div v-if="isLoadingAnimalsInGroup" class="loading-state">
                <p>Carregando animais do lote...</p>
            </div>
            <ul v-else-if="selectedAnimals.length" class="animal-list-in-modal styled-list-group">
            <li v-for="animal in selectedAnimals" :key="animal.id" class="list-item">
                <label :for="`animal-check-${animal.id}`" class="animal-select-label">
                    <input 
                        type="checkbox" 
                        :id="`animal-check-${animal.id}`"
                        :value="animal.id" 
                        v-model="selectedAnimalIdsForBatch" 
                        class="checkbox-input"
                    />
                    <div class="animal-info-details">
                        <span class="animal-id-text">{{ animal.identification }}</span>
                        <span class="animal-detail-item">Status: <span :class="getStatusClass(animal.status_name)">{{ animal.status_name || 'N/D' }}</span></span>
                        <span class="animal-detail-item">Raça: {{ animal.breed_name || 'N/D' }} (Espécie: {{ animal.specie_name || 'N/D' }})</span>
                    </div>
                </label>
            </li>
            </ul>
            <p v-else class="empty-state small-empty-state">Nenhum animal encontrado neste lote.</p>
        </div>
        <div class="modal-actions form-actions">
          <button class="button button-secondary" @click="closeGroupDetailsModal">
            Fechar
          </button>
        </div>
      </div>
    </div>

    <div v-if="showBatchUpdateModal" class="modal-overlay" @click.self="closeBatchUpdateModal">
      <div class="modal-content card"> <div class="modal-header">
            <h3 class="modal-title-text">Atualizar Animais em Lote</h3>
            <button @click="closeBatchUpdateModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>
        <form @submit.prevent="handleBatchUpdate" class="modal-form">
            <p v-if="selectedAnimalIdsForBatch.length" class="selection-info">
            Você está atualizando <strong>{{ selectedAnimalIdsForBatch.length }} animal(is)</strong>.
            </p>

            <div class="form-group">
            <label for="batch-update-type" class="form-label">O que deseja atualizar?</label>
            <select id="batch-update-type" v-model="batchUpdateType" @change="resetBatchUpdateValue" class="select" required>
                <option disabled value="">Selecione um atributo</option>
                <option value="status">Status</option>
                <option value="group">Grupo/Lote</option>
                <option value="identification_type">Tipo de Identificação</option>
                <option value="breed">Raça (e Espécie associada)</option>
            </select>
            </div>

            <div class="form-group" v-if="batchUpdateType === 'status'">
            <label for="batch-status" class="form-label">Novo Status:</label>
            <select id="batch-status" v-model="newBatchValue.status_id" class="select" required>
                <option disabled :value="null_placeholder_batch_status">Selecione um status</option>
                <option v-for="s in statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            </div>

            <div class="form-group" v-else-if="batchUpdateType === 'group'">
            <label for="batch-group" class="form-label">Novo Grupo/Lote:</label>
            <select id="batch-group" v-model="newBatchValue.group_id" class="select">
                <option :value="null_placeholder_batch_group">(Remover do Lote / Sem Lote)</option>
                <option v-for="g in availableAnimalGroupsForBatch" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
            </div>

            <div class="form-group" v-else-if="batchUpdateType === 'identification_type'">
            <label for="batch-identification-type" class="form-label">Novo Tipo de Identificação:</label>
            <select id="batch-identification-type" v-model="newBatchValue.identification_type_id" class="select" required>
                <option disabled :value="null_placeholder_batch_id_type">Selecione um tipo</option>
                <option v-for="it in identificationTypes" :key="it.id" :value="it.id">{{ it.name }}</option>
            </select>
            </div>

            <div class="form-group" v-else-if="batchUpdateType === 'breed'">
            <label for="batch-specie-filter" class="form-label">Filtrar Raças por Espécie:</label>
            <select id="batch-specie-filter" v-model="selectedSpecieForBreedFilter" @change="onSpecieForBreedFilterChange" class="select">
                <option value="">Todas as Espécies</option>
                <option v-for="s in species" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>

            <label for="batch-breed" class="form-label">Nova Raça:</label>
            <select id="batch-breed" v-model="newBatchValue.breed_id" class="select" :disabled="filteredBreedsForBatch.length === 0 && !!selectedSpecieForBreedFilter">
                <option :value="null_placeholder_batch_breed">(Remover Raça)</option>
                <option v-for="b in filteredBreedsForBatch" :key="b.id" :value="b.id">{{ b.name }}</option>
            </select>
            <p v-if="filteredBreedsForBatch.length === 0 && !!selectedSpecieForBreedFilter" class="form-text text-warning">Nenhuma raça encontrada para a espécie selecionada.</p>
            </div>

            <div class="form-actions">
            <button type="submit" class="button button-primary" :disabled="!batchUpdateType">
                Aplicar Mudanças
            </button>
            <button type="button" class="button button-secondary" @click="closeBatchUpdateModal">
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
  </section>
</template>

<script>
// Seu script existente, com as melhorias de notificação e placeholders
import { getAnimals, updateAnimalsBatch } from '@/services/animalService';
import { getAnimalGroups, getStatuses, getIdentificationTypes, getBreeds, getSpecies } from '@/services/lookupService';
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'LotContent',
  components: {
    NotificationModal
  },
  emits: ['back'], // Declarar emits
  data() {
    const nullPlaceholder = null;
    return {
      groups: [],
      groupAnimalsMap: {},
      showGroupDetailsModal: false, // Renomeado de showModal
      selectedGroup: null,
      selectedAnimals: [],
      isLoadingGroups: true,
      isLoadingAnimalsInGroup: false,
      selectedAnimalIdsForBatch: [],

      showBatchUpdateModal: false,
      batchUpdateType: '',
      newBatchValue: {
        status_id: nullPlaceholder,
        group_id: nullPlaceholder,
        identification_type_id: nullPlaceholder,
        breed_id: nullPlaceholder,
        // specie_id não é diretamente atualizado no animal, é derivado da raça
      },
      selectedSpecieForBreedFilter: '',

      statuses: [],
      animalGroups: [], // Lista completa para selects
      identificationTypes: [],
      breeds: [],
      species: [],

      notification: { show: false, message: '', type: 'success' },

      // Placeholders para selects no modal de atualização em lote
      null_placeholder_batch_status: nullPlaceholder,
      null_placeholder_batch_group: nullPlaceholder, // Usado para "(Remover de Lote)"
      null_placeholder_batch_id_type: nullPlaceholder,
      null_placeholder_batch_breed: nullPlaceholder, // Usado para "(Remover Raça)"
    };
  },
  computed: {
    filteredBreedsForBatch() {
        if (!this.selectedSpecieForBreedFilter) {
            return this.breeds;
        }
        // `b.specie` no objeto Breed deve ser o ID da espécie
        return this.breeds.filter(b => b.specie === this.selectedSpecieForBreedFilter);
    },
    availableAnimalGroupsForBatch() {
        // Exclui o lote atual da lista de "novo grupo" para evitar mover para o mesmo lote
        if (this.selectedGroup) {
            return this.animalGroups.filter(g => g.id !== this.selectedGroup.id);
        }
        return this.animalGroups;
    }
  },
  async created() {
    await this.loadLookupsForBatchUpdate(); // Carrega todos os lookups primeiro
    await this.loadInitialData();
  },
  methods: {
    showAppNotification(message, type = 'success', duration = 3000) {
      this.notification.message = message;
      this.notification.type = type;
      this.notification.show = true;
      if (duration) { // Permite notificações que não fecham automaticamente
        setTimeout(() => { this.notification.show = false; }, duration);
      }
    },
    closeNotification() { this.notification.show = false; },
    async loadInitialData() {
      this.isLoadingGroups = true;
      try {
        // getAnimalGroups já deve ser filtrado por owner no backend ou no serviço
        const groupsData = await getAnimalGroups();
        this.groups = groupsData.sort((a,b) => a.name.localeCompare(b.name));
        await this.loadAnimalsCount();
      } catch (e) {
        console.error('Erro ao carregar lotes:', e);
        this.showAppNotification('Erro ao carregar lotes.', 'error');
      } finally {
        this.isLoadingGroups = false;
      }
    },
    async loadLookupsForBatchUpdate() {
      try {
        [
            this.statuses, this.animalGroups, this.identificationTypes,
            this.breeds, this.species
        ] = await Promise.all([
            getStatuses(), getAnimalGroups(), getIdentificationTypes(),
            getBreeds(), getSpecies()
        ]);
        // Ordenar listas para melhor UX nos selects
        this.statuses.sort((a,b) => a.name.localeCompare(b.name));
        this.animalGroups.sort((a,b) => a.name.localeCompare(b.name));
        this.identificationTypes.sort((a,b) => a.name.localeCompare(b.name));
        this.breeds.sort((a,b) => a.name.localeCompare(b.name));
        this.species.sort((a,b) => a.name.localeCompare(b.name));

      } catch (e) {
        console.error('Erro ao carregar dados de lookup para atualização em lote:', e);
        this.showAppNotification('Erro ao carregar dados de referência para atualização.', 'error');
      }
    },
    async loadAnimalsCount() {
      const counts = {};
      // Otimização: Buscar todos os animais uma vez e contar no frontend,
      // ou ter um endpoint que retorne contagens.
      // Por simplicidade, mantendo chamadas individuais por enquanto, mas ciente do N+1.
      const allAnimals = await getAnimals(); // Assumindo que isso busca todos os animais do usuário

      for (const group of this.groups) {
          counts[group.id] = allAnimals.filter(animal => animal.group === group.id).length;
      }
      this.groupAnimalsMap = counts;
    },
    async openGroupDetailsModal(group) {
      this.selectedGroup = group;
      this.selectedAnimalIdsForBatch = []; // Limpa seleção anterior
      this.isLoadingAnimalsInGroup = true;
      this.showGroupDetailsModal = true;
      try {
        // getAnimals já deve ser filtrado por owner no backend.
        // Aqui filtramos especificamente pelo grupo.
        const animalsInGroup = await getAnimals({ group: group.id });
        this.selectedAnimals = animalsInGroup.map(a => ({
            ...a,
            // Adiciona nomes para exibição na lista do modal, caso o serializer não os inclua
            status_name: a.status_name || this.getStatusName(a.status),
            breed_name: a.breed_name || this.getBreedName(a.breed),
            specie_name: a.specie_name || this.getSpecieNameFromBreed(a.breed) // Deriva espécie da raça
        })).sort((a,b) => a.identification.localeCompare(b.identification));
      } catch (e) {
        console.error('Erro ao carregar animais do lote:', e);
        this.selectedAnimals = [];
        this.showAppNotification('Erro ao carregar animais do lote.', 'error');
      } finally {
        this.isLoadingAnimalsInGroup = false;
      }
    },
    closeGroupDetailsModal() {
      this.showGroupDetailsModal = false;
      this.selectedGroup = null;
      this.selectedAnimals = [];
      this.selectedAnimalIdsForBatch = [];
    },
    goBack() {
      this.$emit('back');
    },
    openBatchUpdateModal() {
        if (this.selectedAnimalIdsForBatch.length === 0) {
            this.showAppNotification('Por favor, selecione pelo menos um animal para atualizar.', 'warning');
            return;
        }
        this.batchUpdateType = ''; // Reseta o tipo de atualização
        this.resetBatchUpdateValue(); // Reseta os valores
        this.showBatchUpdateModal = true;
    },
    closeBatchUpdateModal() {
      this.showBatchUpdateModal = false;
    },
    resetBatchUpdateValue() {
      this.newBatchValue = {
        status_id: this.null_placeholder_batch_status,
        group_id: this.null_placeholder_batch_group, // Permitir "nenhum lote"
        identification_type_id: this.null_placeholder_batch_id_type,
        breed_id: this.null_placeholder_batch_breed, // Permitir "nenhuma raça"
      };
      this.selectedSpecieForBreedFilter = ''; // Reseta filtro de espécie
    },
    onSpecieForBreedFilterChange() {
      this.newBatchValue.breed_id = this.null_placeholder_batch_breed; // Reseta a raça selecionada
    },
    async handleBatchUpdate() {
      if (this.selectedAnimalIdsForBatch.length === 0) {
        this.showAppNotification('Nenhum animal selecionado para atualização.', 'warning');
        return;
      }
      if (!this.batchUpdateType) {
          this.showAppNotification('Selecione um atributo para atualizar.', 'warning');
          return;
      }

      let updatePayload = {};
      let fieldDescription = ''; // Para a mensagem de sucesso/erro

      switch (this.batchUpdateType) {
        case 'status':
          if (this.newBatchValue.status_id === this.null_placeholder_batch_status) {
            this.showAppNotification('Por favor, selecione um novo status.', 'warning'); return;
          }
          updatePayload = { new_status_id: this.newBatchValue.status_id };
          fieldDescription = 'Status';
          break;
        case 'group':
          // new_group_id pode ser null se null_placeholder_batch_group for null
          updatePayload = { new_group_id: this.newBatchValue.group_id };
          fieldDescription = 'Grupo/Lote';
          break;
        case 'identification_type':
          if (this.newBatchValue.identification_type_id === this.null_placeholder_batch_id_type) {
            this.showAppNotification('Por favor, selecione um novo tipo de identificação.', 'warning'); return;
          }
          updatePayload = { new_identification_type_id: this.newBatchValue.identification_type_id };
          fieldDescription = 'Tipo de Identificação';
          break;
        case 'breed':
          updatePayload = { new_breed_id: this.newBatchValue.breed_id };
          // A espécie (new_specie_id) será derivada no backend ou no serviço pelo new_breed_id
          fieldDescription = 'Raça';
          break;
        default:
          this.showAppNotification('Tipo de atualização inválido.', 'error');
          return;
      }

      try {
        const response = await updateAnimalsBatch(this.selectedAnimalIdsForBatch, updatePayload);
        this.showAppNotification(
          `${response.updated_animals_count} animal(is) tiveram o(a) ${fieldDescription.toLowerCase()} atualizado(s) com sucesso!`,
          'success'
        );
        this.closeBatchUpdateModal();
        // Recarregar animais do lote selecionado após a atualização
        if (this.selectedGroup) {
            await this.openGroupDetailsModal(this.selectedGroup); // Reabre e recarrega
        }
        await this.loadAnimalsCount(); // Atualiza contagem nos cards principais
      } catch (error) {
        console.error(`Erro ao atualizar ${fieldDescription} em lote:`, error.response?.data || error);
        let errorMsg = `Erro ao atualizar ${fieldDescription.toLowerCase()} em lote.`;
        if (error.response && error.response.data) {
            const errors = error.response.data;
            if (errors.error) errorMsg += ` ${errors.error}`;
            // Adicionar mais detalhes se o backend os fornecer
            else if (typeof errors === 'object') {
                 errorMsg += ' Detalhes: ' + Object.values(errors).flat().join(' ');
            }
        }
        this.showAppNotification(errorMsg, 'error');
      }
    },
    getStatusName(statusId) {
      const status = this.statuses.find(s => s.id === statusId);
      return status ? status.name : 'N/D';
    },
    getStatusClass(statusName) { // Recebe o nome do status já
        if (!statusName) return 'status-badge status-default';
        const nameLower = statusName.toLowerCase();
        if (nameLower === 'ativo') return 'status-badge status-active';
        if (nameLower === 'vendido') return 'status-badge status-sold';
        if (nameLower === 'abatido') return 'status-badge status-slaughtered';
        return 'status-badge status-default';
    },
    getGroupName(groupId) {
      if (groupId === null || groupId === undefined) return 'Nenhum';
      const group = this.animalGroups.find(g => g.id === groupId);
      return group ? group.name : 'N/D';
    },
    getIdentificationTypeName(typeId) {
      const type = this.identificationTypes.find(it => it.id === typeId);
      return type ? type.name : 'N/D';
    },
    getBreedName(breedId) {
      if (!breedId) return 'N/D';
      const breed = this.breeds.find(b => b.id === breedId);
      return breed ? breed.name : 'N/D';
    },
    getSpecieNameFromBreed(breedId) { // Busca o nome da espécie através do ID da raça
        if (!breedId) return 'N/D';
        const breed = this.breeds.find(b => b.id === breedId);
        if (breed && breed.specie) { // breed.specie é o ID da espécie
            const specie = this.species.find(s => s.id === breed.specie);
            return specie ? specie.name : 'N/D';
        }
        return 'N/D';
    },
     getSpecieName(specieId) { // Método direto se você tiver o specieId (ex: do animal.specie_id)
        if (!specieId) return 'N/D';
        const specie = this.species.find(s => s.id === specieId);
        return specie ? specie.name : 'N/D';
    }
  }
}
</script>

<style scoped>
/* Estilos globais via classes e variáveis CSS são primários. */
/* Estes são estilos específicos para LotContent. */

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Ajustado para espaço entre o botão e o título */
  gap: var(--sp-md);
  margin-bottom: var(--sp-md); /* Reduzido */
  padding-bottom: var(--sp-md);
  border-bottom: var(--border-width) solid var(--color-border-light);
}

.back-button-styled { /* Renomeado de .back-button para não conflitar com classe global .button */
  /* Usar classes de botão globais e adicionar ajustes se necessário */
  /* Ex: class="button button-outline-secondary button-sm" */
  display: flex;
  align-items: center;
  gap: var(--sp-xs);
  font-weight: var(--fw-medium);
}
.panel-title-text { /* Renomeado de .panel-title */
  flex-grow: 1; /* Título ocupa espaço disponível */
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-text-primary);
  font-size: var(--fs-h3);
  margin: 0;
}
.panel-description {
  text-align: center; /* Centralizado para esta tela */
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); /* Cards um pouco maiores */
  gap: var(--sp-lg);
  padding: var(--sp-md) 0;
}
.group-card {
  /* .card e .card-interactive (se definida globalmente para hover) já aplicam estilos base */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 150px; /* Altura mínima aumentada */
  cursor: pointer;
}
.group-card:hover, .group-card:focus-within {
    border-color: var(--color-primary); /* Destaque no hover */
}

.card-header-custom { /* Para diferenciar do .card-header global se necessário */
    padding-bottom: var(--sp-sm);
    border-bottom: var(--border-width) solid var(--color-border-light);
    margin-bottom: var(--sp-sm);
}
.group-card-title { /* Era h3 */
  margin: 0;
  font-size: var(--fs-large); /* Título do card */
  color: var(--color-primary);
  font-weight: var(--fw-semibold);
}
.card-body-custom p {
  margin: var(--sp-xs) 0 0;
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
}
.group-animal-count {
    font-weight: var(--fw-medium);
}
.group-description {
    font-style: italic;
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    margin-top: var(--sp-xs);
    /* Limitar número de linhas se necessário */
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Mostrar no máximo 2 linhas */
    line-clamp: 2; /* Standard property for compatibility */
    -webkit-box-orient: vertical;
}
.card-footer-actions {
    margin-top: var(--sp-md);
    padding-top: var(--sp-sm);
    border-top: var(--border-width) solid var(--color-border-light);
    display: flex;
    justify-content: flex-end;
}


.empty-state, .loading-state { /* .empty-state global já tem estilos */
  padding: var(--sp-xl) 0;
  font-size: var(--fs-large); /* Maior para destaque */
}


/* Modal de Detalhes do Lote */
.modal-content.large-modal {
  max-width: 900px; /* Mantido */
}
.batch-actions-bar { /* Renomeado de .batch-actions-header */
  display: flex;
  justify-content: space-between; /* Botão à direita, texto à esquerda */
  align-items: center;
  margin-bottom: var(--sp-md);
  padding: var(--sp-sm) var(--sp-xs); /* Menor padding */
  border-bottom: var(--border-width) solid var(--color-border-light);
  background-color: var(--color-bg-muted);
  border-radius: var(--border-radius-sm);
}
.batch-actions-bar span {
    font-size: var(--fs-small);
    color: var(--color-text-secondary);
}
.batch-actions-bar .button { /* Botão de editar em lote */
    font-size: var(--fs-small);
    padding: var(--sp-xs) var(--sp-sm);
}
.batch-actions-bar .button svg {
    margin-right: var(--sp-xs);
}


.animal-list-in-modal { /* Renomeado de .modal-list */
  list-style: none;
  padding: 0;
  margin: 0 0 var(--sp-md);
  max-height: 40vh; /* Ajustar altura máxima */
  overflow-y: auto;
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-sm);
}
.animal-list-in-modal .list-item { /* Usando .list-item para consistência */
  padding: var(--sp-sm) var(--sp-md);
  border-bottom: var(--border-width) solid var(--color-border-light);
  display: flex; /* Já é flex, mas confirmar */
  align-items: center;
  gap: var(--sp-md); /* Maior gap */
  background-color: var(--color-bg-component);
}
.animal-list-in-modal .list-item:last-child {
  border-bottom: none;
}
.animal-list-in-modal .list-item:hover {
  background-color: var(--color-bg-hover);
}

.animal-select-label { /* Label envolvendo checkbox e info para melhor clique */
    display: flex;
    align-items: center;
    gap: var(--sp-md);
    width: 100%;
    cursor: pointer;
}
.checkbox-input { /* Classe para o input checkbox */
  transform: scale(1.3); /* Checkbox maior */
  margin-right: var(--sp-sm); /* Mantém o gap se o label não for usado para envolver */
  flex-shrink: 0;
}
.animal-info-details { /* Renomeado de .animal-info */
  flex-grow: 1;
  text-align: left;
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
}
.animal-id-text { /* Renomeado de .animal-id */
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
}
.animal-detail-item { /* Para cada detalhe do animal na lista */
    display: block; /* Cada detalhe em uma nova linha */
    font-size: var(--fs-small);
    color: var(--color-text-muted);
    margin-top: var(--sp-xxs);
}
.animal-detail-item .status-badge { /* Para o status dentro da lista */
    display: inline-block; /* Para o padding funcionar bem */
    margin-left: var(--sp-xs);
}

/* Modal de Atualização em Lote */
.modal-content .form-group { /* Estilos para form-groups dentro de modais */
  margin-top: var(--sp-md);
  text-align: left;
}
.modal-content .form-group label.form-label { /* Estilos para labels dentro de modais */
  /* .form-label global já deve ter estilos */
  margin-bottom: var(--sp-xs); /* Espaço menor abaixo do label */
}
.selection-info {
    font-size: var(--fs-base);
    color: var(--color-text-secondary);
    margin-bottom: var(--sp-md);
    padding: var(--sp-sm);
    background-color: var(--color-primary-light);
    border-left: 4px solid var(--color-primary);
    border-radius: var(--border-radius-sm);
}
.form-text.text-warning { /* Para mensagens de aviso em formulários */
    font-size: var(--fs-small);
    color: var(--color-warning); /* Assumindo que --color-warning está definido */
    margin-top: var(--sp-xs);
}

/* Classes de status (reutilizadas de AnimalContent) */
.status-badge {
    font-size: var(--fs-smaller);
    padding: calc(var(--sp-xxs) / 2) var(--sp-xs);
    border-radius: var(--border-radius-pill);
    font-weight: var(--fw-medium);
    color: var(--color-text-inverted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block; /* Para padding funcionar corretamente */
}
.status-active { background-color: var(--color-success); }
.status-sold { background-color: var(--color-danger); }
.status-slaughtered { background-color: var(--color-secondary); } /* Exemplo */
.status-default { background-color: var(--color-text-muted); }

/* Animação de entrada para modal (se .fadeInScale não estiver global) */
@keyframes fadeInScale {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.small-empty-state {
    font-size: var(--fs-base);
    padding: var(--sp-md);
}
</style>