<!-- File: src/components/LotContent.vue -->
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

    <!-- Modal de Animais do Lote -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">
          Animais do Lote “{{ selectedGroup.name }}”
        </h3>
        <ul class="modal-list">
          <li v-for="animal in selectedAnimals" :key="animal.id">
            {{ animal.identification }}
          </li>
        </ul>
        <button class="button-primary" @click="closeModal">
          Fechar
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import { getAnimalGroups } from '@/services/lookupService'
import { getAnimals } from '@/services/animalService'

export default {
  name: 'LotContent',
  data() {
    return {
      groups: [],
      groupAnimalsMap: {},
      showModal: false,
      selectedGroup: null,
      selectedAnimals: []
    }
  },
  async created() {
    try {
      this.groups = await getAnimalGroups()
      await this.loadAnimalsCount()
    } catch (e) {
      console.error('Erro ao carregar lotes:', e)
    }
  },
  methods: {
    async loadAnimalsCount() {
      for (const g of this.groups) {
        try {
          // filtra animais ativos (status=1) por group_id
          const list = await getAnimals({ group_id: g.id, status: 1 })
          this.$set(this.groupAnimalsMap, g.id, list.length)
        } catch {
          this.$set(this.groupAnimalsMap, g.id, 0)
        }
      }
    },
    async openGroup(group) {
      this.selectedGroup = group
      try {
        this.selectedAnimals = await getAnimals({ group_id: group.id, status: 1 })
      } catch (e) {
        console.error('Erro ao carregar animais:', e)
        this.selectedAnimals = []
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.selectedGroup = null
      this.selectedAnimals = []
    },
    goBack() {
      this.$emit('back')
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
.header-row {
  display: flex;
  align-items: center;
  gap: var(--sp-md);
  margin-bottom: var(--sp-lg);
}
.header-row .panel-title {
  flex: 1;
  margin: 0;
  text-align: center;
  font-family: var(--font-heading);
  color: var(--color-primary);
}
.back-button {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 1rem;
  cursor: pointer;
  transition: color 0.2s;
}
.back-button:hover {
  color: var(--color-accent);
}
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill,minmax(180px,1fr));
  gap: var(--sp-lg);
}
.group-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: var(--sp-md);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.group-card:hover,
.group-card:focus {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  outline: none;
}
.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--color-dark-gray);
}
.card-body p {
  margin: var(--sp-xs) 0 0;
  font-size: var(--font-size-small);
  color: var(--color-secondary);
}
.empty-state {
  text-align: center;
  color: var(--color-dark-gray);
  padding: var(--sp-lg) 0;
}
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #ffffff !important;
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  width: 100%; max-width: 400px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  text-align: center;
}
.modal-title {
  font-family: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
}
.modal-list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--sp-md);
  max-height: 200px;
  overflow-y: auto;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}
.modal-list li {
  padding: var(--sp-xs) 0;
  border-bottom: 1px solid var(--color-light-gray);
  font-size: var(--font-size-base);
  color: var(--color-dark-gray);
}
.modal-list li:last-child {
  border-bottom: none;
}
.button-primary {
  padding: var(--sp-sm) var(--sp-lg);
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
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
</style>
