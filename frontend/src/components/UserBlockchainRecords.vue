<template>
  <div class="user-blockchain-records-content content-panel">
    <h3 class="panel-title">Meus Registros na Blockchain</h3>
    <p class="panel-description">
      Aqui estão os eventos e informações dos seus animais que foram registrados na blockchain.
    </p>

    <div v-if="isLoading" class="loading-state">
      <p>Carregando registros...</p>
    </div>
    <div v-else-if="errorLoading" class="error-state">
      <p>Ocorreu um erro ao carregar seus registros. Por favor, tente novamente mais tarde.</p>
      <button @click="loadUserRecords" class="button-secondary">Tentar Novamente</button>
    </div>
    <div v-else-if="userRecords.length === 0" class="empty-state">
      <p>Você ainda não possui registros na blockchain.</p>
    </div>

    <div v-else class="records-list-container">
      <ul class="records-list">
        <li v-for="record in userRecords" :key="record.id" class="record-item">
          <div class="record-header">
            <strong>Registro ID:</strong> {{ record.id }}
          </div>
          <div class="record-body">
            <p><strong>Animal ID:</strong> {{ record.animal }}</p>
            <p><strong>Evento ID:</strong> {{ record.event }}</p>
            <p><strong>Hash da Transação:</strong> <span class="transaction-hash">{{ record.transaction_hash }}</span></p>
            <p><strong>Status Blockchain:</strong> {{ record.status }}</p>
            <p><strong>Data do Registro:</strong> {{ formatDate(record.created_at) }}</p>
          </div>
          </li>
      </ul>
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
import { ref, onMounted } from 'vue';
import { filterBlockchain } from '@/services/blockchainService';
import { getUserProfile } from '@/services/userService'; // Para obter o ID do usuário logado
import NotificationModal from '@/components/NotificationModal.vue';

export default {
  name: 'UserBlockchainRecords',
  components: {
    NotificationModal,
  },
  setup() {
    const userRecords = ref([]);
    const currentUser = ref(null);
    const isLoading = ref(true);
    const errorLoading = ref(false);
    const notification = ref({ show: false, message: '', type: 'success' });

    const showAppNotification = (message, type = 'error') => {
      notification.value.message = message;
      notification.value.type = type;
      notification.value.show = true;
    };

    const closeNotification = () => {
      notification.value.show = false;
    };

    const fetchCurrentUser = async () => {
      try {
        currentUser.value = await getUserProfile();
      } catch (error) {
        console.error('Erro ao buscar perfil do usuário para registros blockchain:', error);
        errorLoading.value = true;
        showAppNotification('Não foi possível identificar o usuário para buscar os registros.');
        throw error; // Propaga o erro para interromper o carregamento dos registros
      }
    };

    const loadUserRecords = async () => {
      isLoading.value = true;
      errorLoading.value = false;
      userRecords.value = []; // Limpa registros anteriores

      if (!currentUser.value || !currentUser.value.id) {
        try {
          await fetchCurrentUser();
        } catch (error) {
          // fetchCurrentUser já lida com errorLoading e notificação
          isLoading.value = false;
          return;
        }
      }
      
      // Se ainda não tem currentUser.value.id, não prossegue
      if (!currentUser.value || !currentUser.value.id) {
          isLoading.value = false;
          errorLoading.value = true; // Marcar erro se usuário não pôde ser carregado
          showAppNotification('ID do usuário não encontrado para filtrar registros.');
          return;
      }

      try {
        // Assumindo que o filtro no backend é 'owner' ou 'user' ou 'recorded_by'
        // Verifique qual o parâmetro correto que seu backend espera para o ID do usuário.
        const records = await filterBlockchain({ owner: currentUser.value.id }); // ou user_id, etc.
        userRecords.value = records.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // Ordena pelos mais recentes
      } catch (error) {
        console.error('Erro ao carregar registros de blockchain do usuário:', error);
        errorLoading.value = true;
        showAppNotification('Erro ao carregar seus registros da blockchain.');
      } finally {
        isLoading.value = false;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      try {
        const date = new Date(dateString);
        return date.toLocaleString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        });
      } catch (e) {
        return dateString;
      }
    };

    onMounted(async () => {
      await loadUserRecords();
    });

    return {
      userRecords,
      isLoading,
      errorLoading,
      loadUserRecords, // Expor para o botão "Tentar Novamente"
      formatDate,
      notification,
      closeNotification
    };
  }
};
</script>

<style scoped>
/* Usando variáveis CSS globais se definidas, com fallbacks */
.user-blockchain-records-content {
  /* Estilos baseados no .content-panel da DashboardPage */
  background-color: var(--color-white, #FFFFFF);
  padding: var(--sp-lg, 1.5rem);
  border-radius: var(--sp-sm, 0.5rem);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  text-align: left; /* Alinha texto à esquerda por padrão */
}

.panel-title {
  text-align: center;
  font-family: var(--font-heading, serif);
  color: var(--color-primary, #1A73E8);
  margin-bottom: var(--sp-xs, 0.25rem);
  font-size: 1.75rem; /* Ajuste conforme necessário */
}

.panel-description {
  text-align: center;
  color: var(--color-dark-gray, #555);
  margin-bottom: var(--sp-xl, 2rem);
  font-size: var(--fs-base, 14px);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.loading-state, .empty-state, .error-state {
  text-align: center;
  padding: var(--sp-xl, 2rem);
  color: var(--color-dark-gray, #555);
  font-size: var(--fs-base, 1rem);
}
.error-state button {
    margin-top: var(--sp-md, 1rem);
}

.records-list-container {
  margin-top: var(--sp-lg, 1.5rem);
}

.records-list {
  list-style: none;
  padding: 0;
}

.record-item {
  background-color: var(--color-muted, #F5F5F5);
  border: 1px solid var(--color-border, #E0E0E0);
  border-radius: var(--sp-sm, 0.5rem);
  padding: var(--sp-md, 1rem);
  margin-bottom: var(--sp-md, 1rem);
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.record-header {
  font-size: var(--fs-base, 1.05rem);
  color: var(--color-text, #333);
  margin-bottom: var(--sp-sm, 0.5rem);
  padding-bottom: var(--sp-sm, 0.5rem);
  border-bottom: 1px dashed var(--color-border, #E0E0E0);
}

.record-body p {
  margin-bottom: var(--sp-xs, 0.25rem);
  font-size: var(--fs-base, 0.95rem);
  color: var(--color-dark-gray, #555);
  line-height: 1.6;
}

.record-body p strong {
  color: var(--color-text, #333);
}

.transaction-hash {
  font-family: monospace;
  word-break: break-all; /* Quebra hashes longos */
  font-size: 0.9em;
}

/* Reutilizando estilos de botões se necessário, ou defina os seus */
.button-secondary {
  background-color: var(--color-muted, #f5f5f5);
  color: var(--color-text, #333);
  border: 2px solid var(--color-border, #ccc);
  padding: var(--sp-sm, 0.65rem) var(--sp-md, 1rem);
  border-radius: var(--sp-sm, 0.5rem);
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}
.button-secondary:hover,
.button-secondary:focus {
  background-color: var(--color-dark-gray, #555);
  color: var(--color-bg, #FFFFFF);
  border-color: var(--color-dark-gray, #555);
  outline: none;
}
</style>