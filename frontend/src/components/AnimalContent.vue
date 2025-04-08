<template>
  <div class="animal-content">
    <h2>Gerenciar Animais</h2>

    <!-- Lista de animais do usuário -->
    <div v-if="animals.length">
      <h3>Animais Cadastrados</h3>
      <ul>
        <li v-for="animal in animals" :key="animal.id">
          <strong>{{ animal.identification }}</strong>
          <button @click="loadAnimalForEdit(animal)">Editar</button>
          <button @click="handleDelete(animal.id)">Deletar</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Nenhum animal cadastrado.</p>
    </div>

    <!-- Formulário para cadastro/edição -->
    <div class="animal-form">
      <h3>{{ editing ? "Editar Animal" : "Cadastrar Animal" }}</h3>
      <form @submit.prevent="handleSubmit">
        <!-- Campos do formulário de animal -->
        <div>
          <label>Identificação:</label>
          <input v-model="form.identification" type="text" required />
        </div>

        <!-- Select para Espécie -->
        <div>
          <label>Espécie:</label>
          <select v-model="form.specie" required>
            <option disabled value="">Selecione</option>
            <option v-for="option in species" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>

        <!-- Select para Raça -->
        <div>
          <label>Raça:</label>
          <select v-model="form.breed" required>
            <option disabled value="">Selecione</option>
            <option v-for="option in breeds" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>

        <!-- Select para Grupo com opção "Novo Grupo" -->
        <div>
          <label>Grupo:</label>
          <select v-model="form.group" @change="handleGroupChange" required>
            <option disabled value="">Selecione</option>
            <option value="new">-- Novo Grupo --</option>
            <option v-for="option in animalGroups" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>

        <!-- Formulário para novo grupo, se selecionado -->
        <div v-if="isNewGroupSelected" class="new-group-form">
          <h4>Cadastrar Novo Grupo</h4>
          <div>
            <label>Nome do Grupo:</label>
            <input v-model="newGroup.name" type="text" required />
          </div>
          <div>
            <label>Descrição:</label>
            <input v-model="newGroup.description" type="text" />
          </div>
          <!-- O botão chama a função saveNewGroup -->
          <button type="button" @click="saveNewGroup">Salvar Novo Grupo</button>
        </div>

        <!-- Select para Gênero -->
        <div>
          <label>Gênero:</label>
          <select v-model="form.gender" required>
            <option disabled value="">Selecione</option>
            <option v-for="option in genders" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>

        <!-- Select para Status -->
        <div>
          <label>Status:</label>
          <select v-model="form.status" required>
            <option disabled value="">Selecione</option>
            <option v-for="option in statuses" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>

        <!-- Select para Tipo de Identificação -->
        <div>
          <label>Tipo de Identificação:</label>
          <select v-model="form.identification_type" required>
            <option disabled value="">Selecione</option>
            <option v-for="option in identificationTypes" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>

        <div>
          <label>Data de Nascimento:</label>
          <input v-model="form.birth_date" type="date" required />
        </div>

        <div>
          <label>Observações:</label>
          <textarea v-model="form.observations"></textarea>
        </div>

        <button type="submit">{{ editing ? "Atualizar" : "Cadastrar" }}</button>
        <button type="button" v-if="editing" @click="cancelEdit">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
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
  setup() {
    // Dados do animal
    const animals = ref([]);
    const editing = ref(false);
    const editingId = ref(null);
    const form = ref({
      identification: '',
      specie: '',
      breed: '',
      group: '',
      gender: '',
      status: '',
      identification_type: '',
      birth_date: '',
      observations: ''
    });

    // Dados de referência
    const species = ref([]);
    const breeds = ref([]);
    const animalGroups = ref([]);
    const genders = ref([]);
    const statuses = ref([]);
    const identificationTypes = ref([]);

    // Dados para novo grupo
    const isNewGroupSelected = computed(() => form.value.group === 'new');
    const newGroup = ref({
      name: '',
      description: ''
    });

    // Função para registrar novo grupo
    const saveNewGroup = async () => {
      try {
        console.log("DEBUG - Dados do novo grupo:", newGroup.value);
        const groupData = { ...newGroup.value };
        const createdGroup = await registerAnimalGroup(groupData);
        console.log("DEBUG - Novo grupo criado:", createdGroup);
        animalGroups.value.push(createdGroup);
        // Define o grupo do formulário com o novo grupo criado
        form.value.group = createdGroup.id;
        // Limpa os dados do novo grupo
        newGroup.value = { name: '', description: '' };
        alert('Novo grupo cadastrado com sucesso.');
      } catch (error) {
        console.error('Erro ao cadastrar novo grupo:', error);
        alert('Erro ao cadastrar novo grupo.');
      }
    };

    const resetForm = () => {
      form.value = {
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
      editing.value = false;
      editingId.value = null;
    };

    const handleSubmit = async () => {
      try {
        if (editing.value) {
          const updatedAnimal = await updateAnimal(editingId.value, form.value);
          animals.value = animals.value.map(animal =>
            animal.id === editingId.value ? updatedAnimal : animal
          );
          alert('Animal atualizado com sucesso.');
        } else {
          const newAnimal = await registerAnimal(form.value);
          animals.value.push(newAnimal);
          alert('Animal cadastrado com sucesso.');
        }
        resetForm();
      } catch (error) {
        console.error('Erro ao salvar animal:', error);
        alert('Erro ao salvar animal.');
      }
    };

    const loadAnimalForEdit = (animal) => {
      editing.value = true;
      editingId.value = animal.id;
      form.value = { ...animal };
    };

    const handleDelete = async (id) => {
      if (confirm('Tem certeza que deseja deletar este animal?')) {
        try {
          await deleteAnimal(id);
          animals.value = animals.value.filter(a => a.id !== id);
          alert('Animal deletado com sucesso.');
        } catch (error) {
          console.error('Erro ao deletar animal:', error);
          alert('Erro ao deletar animal.');
        }
      }
    };

    const handleGroupChange = () => {
      if (form.value.group === 'new') {
        newGroup.value = { name: '', description: '' };
      }
    };

    const loadAnimals = async () => {
      try {
        animals.value = await getAnimals();
      } catch (error) {
        console.error('Erro ao carregar animais:', error);
      }
    };

    const loadLookups = async () => {
      try {
        species.value = await getSpecies();
        breeds.value = await getBreeds();
        animalGroups.value = await getAnimalGroups();
        genders.value = await getGenders();
        statuses.value = await getStatuses();
        identificationTypes.value = await getIdentificationTypes();
      } catch (error) {
        console.error('Erro ao carregar dados de referência:', error);
      }
    };

    onMounted(() => {
      loadAnimals();
      loadLookups();
    });

    return {
      animals,
      form,
      species,
      breeds,
      animalGroups,
      genders,
      statuses,
      identificationTypes,
      editing,
      isNewGroupSelected,
      newGroup,
      handleSubmit,
      resetForm,
      loadAnimalForEdit,
      handleDelete,
      handleGroupChange,
      saveNewGroup  // Certifique-se de retornar a função para que ela seja acessível na template
    };
  }
};
</script>

<style scoped>
.animal-content {
  padding: 1rem;
}

.animal-form {
  margin-top: 2rem;
}

.animal-form form {
  max-width: 500px;
}

.animal-form div {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

input, select, textarea {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

button {
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.new-group-form {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f0f0f0;
}
</style>
