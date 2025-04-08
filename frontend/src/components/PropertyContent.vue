<!-- src/components/PropriedadeContent.vue -->
<template>
    <div class="property-content">
      <h2>Minhas Propriedades</h2>
  
      <!-- Lista de propriedades -->
      <div v-if="properties && properties.length">
        <ul>
          <li v-for="prop in properties" :key="prop.id">
            <div>
              <strong>{{ prop.name }}</strong> - {{ prop.address }}, {{ prop.city }}, {{ prop.state }} - {{ prop.zip_code }}
            </div>
            <button @click="editProperty(prop)">Editar</button>
            <button @click="removeProperty(prop.id)">Deletar</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>Você não possui nenhuma propriedade cadastrada.</p>
      </div>
  
      <!-- Formulário para cadastro/edição -->
      <div class="property-form">
        <h3>{{ editing ? "Editar Propriedade" : "Adicionar Propriedade" }}</h3>
        <form @submit.prevent="submitForm">
          <label>
            Nome:
            <input type="text" v-model="formData.name" required />
          </label>
          <label>
            Endereço:
            <input type="text" v-model="formData.address" required />
          </label>
          <label>
            Cidade:
            <input type="text" v-model="formData.city" required />
          </label>
          <label>
            Estado:
            <input type="text" v-model="formData.state" required />
          </label>
          <label>
            CEP:
            <input type="text" v-model="formData.zip_code" required />
          </label>
          <button type="submit">{{ editing ? "Atualizar" : "Cadastrar" }}</button>
          <button type="button" v-if="editing" @click="cancelEdit">Cancelar</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { getUserProperties, registerProperty, updateProperty, deleteProperty } from '@/services/propertyService';
  
  export default {
    name: 'PropriedadeContent',
    data() {
      return {
        properties: [],
        formData: {
          name: '',
          address: '',
          city: '',
          state: '',
          zip_code: '',
        },
        editing: false,
        editingId: null,
      };
    },
    created() {
      this.loadProperties();
    },
    methods: {
      async loadProperties() {
        try {
          const data = await getUserProperties();
          this.properties = data;
        } catch (error) {
          console.error('Erro ao carregar propriedades:', error);
        }
      },
      async submitForm() {
        try {
          if (this.editing) {
            // Atualiza a propriedade
            const updatedProperty = await updateProperty(this.editingId, this.formData);
            // Atualiza a lista local
            this.properties = this.properties.map((p) =>
              p.id === this.editingId ? updatedProperty : p
            );
            alert('Propriedade atualizada com sucesso.');
          } else {
            // Registra nova propriedade
            const newProperty = await registerProperty(this.formData);
            this.properties.push(newProperty);
            alert('Propriedade cadastrada com sucesso.');
          }
          this.resetForm();
        } catch (error) {
          console.error('Erro no cadastro/atualização da propriedade:', error);
          alert('Erro ao salvar propriedade.');
        }
      },
      editProperty(property) {
        this.editing = true;
        this.editingId = property.id;
        this.formData = { ...property };
      },
      cancelEdit() {
        this.editing = false;
        this.editingId = null;
        this.resetForm();
      },
      resetForm() {
        this.formData = {
          name: '',
          address: '',
          city: '',
          state: '',
          zip_code: '',
        };
      },
      async removeProperty(propertyId) {
        if (confirm('Tem certeza que deseja deletar esta propriedade?')) {
          try {
            await deleteProperty(propertyId);
            this.properties = this.properties.filter(p => p.id !== propertyId);
            alert('Propriedade removida com sucesso.');
          } catch (error) {
            console.error('Erro ao deletar propriedade:', error);
            alert('Erro ao deletar propriedade.');
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .property-content {
    padding: 1rem;
  }
  
  .property-form form {
    margin-top: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  input[type="text"] {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
  }
  
  button {
    margin-right: 0.5rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
  </style>
  