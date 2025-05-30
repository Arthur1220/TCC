<template>
  <section class="content-panel transfer-ownership-panel">
    <div class="panel-header">
      <h2 class="panel-title-text">Transferência de Titularidade de Animais</h2>
    </div>
    <p class="panel-description">
      Gerencie suas solicitações de transferência de animais e inicie novas transferências para outros usuários registrados no sistema.
      Para iniciar uma transferência, você precisará do "Hash de Usuário" do destinatário.
    </p>

    <div v-if="currentUser && currentUser.user_hash" class="current-user-hash-section card">
      <div class="hash-info">
        <span class="hash-label">Seu Hash de Usuário (para compartilhar):</span>
        <strong class="hash-value" @click="copyToClipboard(currentUser.user_hash)" title="Clique para copiar">{{ currentUser.user_hash }}</strong>
      </div>
      <button class="button button-outline-secondary button-sm" @click="copyToClipboard(currentUser.user_hash)">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
        Copiar Hash
      </button>
    </div>

    <div class="transfer-layout">
      <div class="column requests-column">
        <h3 class="column-title">Minhas Solicitações de Transferência</h3>

        <div class="request-section">
          <h4><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M3 14h2v2H3v-2zm0-4h2v2H3v-2zm0-4h2v2H3V6zm4 8h14v-2H7v2zm0-4h14v-2H7v2zm0-8v2h14V2H7z"/></svg> Solicitações Enviadas</h4>
          <div v-if="isLoadingSentRequests" class="loading-state small-loading">Carregando...</div>
          <ul v-else-if="sentRequests.length" class="styled-list-group compact-list">
            <li v-for="req in sentRequests" :key="req.id" class="list-item request-item">
              <div class="item-info">
                <span>Para: <strong>{{ req.requested_to_username }}</strong></span>
                <span>Animais: {{ req.animals_details.length }}</span>
                <span>Status: <span :class="getRequestStatusClass(req.status)">{{ req.status_display }}</span></span>
                <span class="request-date">Data: {{ formatDate(req.request_date) }}</span>
              </div>
              <div class="item-actions">
                <button class="button button-outline-secondary button-sm" @click="viewRequestDetails(req)">Ver Detalhes</button>
                <button v-if="req.status === 'PENDING_APPROVAL'" class="button button-danger button-sm" @click="promptCancelRequest(req)">Cancelar</button>
              </div>
            </li>
          </ul>
          <p v-else class="empty-state small-empty-state">Nenhuma solicitação enviada.</p>
        </div>

        <hr class="column-divider">

        <div class="request-section">
          <h4><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-4 14h-2v-4H9V7h2v4h2v2h2v4zm-2-7h-2V7h2v3z"/></svg> Solicitações Recebidas (Pendentes)</h4>
          <div v-if="isLoadingReceivedRequests" class="loading-state small-loading">Carregando...</div>
          <ul v-else-if="receivedPendingRequests.length" class="styled-list-group compact-list">
            <li v-for="req in receivedPendingRequests" :key="req.id" class="list-item request-item">
              <div class="item-info">
                <span>De: <strong>{{ req.initiated_by_username }}</strong></span>
                <span>Animais: {{ req.animals_details.length }}</span>
                <span class="request-date">Data: {{ formatDate(req.request_date) }}</span>
              </div>
              <div class="item-actions">
                <button class="button button-success button-sm" @click="promptAcceptRequest(req)">Aceitar</button>
                <button class="button button-danger button-sm" @click="promptRejectRequest(req)">Rejeitar</button>
                <button class="button button-outline-secondary button-sm" @click="viewRequestDetails(req)">Ver Detalhes</button>
              </div>
            </li>
          </ul>
          <p v-else class="empty-state small-empty-state">Nenhuma solicitação pendente recebida.</p>
        </div>
      </div>

      <div class="column new-request-column">
        <h3 class="column-title">Nova Solicitação de Transferência</h3>
        <form @submit.prevent="findUserByHashAndOpenModal" class="form-grid single-column-form">
          <div class="form-group">
            <label for="user-hash" class="form-label">Hash de Usuário do Destinatário*</label>
            <input id="user-hash" v-model="recipientUserHash" type="text" class="input" placeholder="Insira o hash do usuário aqui" required />
          </div>
          <div class="form-actions">
            <button type="submit" class="button button-primary" :disabled="!recipientUserHash.trim() || isLoadingUserByHash">
              <span v-if="isLoadingUserByHash">Buscando Usuário...</span>
              <span v-else>Buscar Usuário e Selecionar Animais</span>
            </button>
          </div>
        </form>
        <p v-if="userSearchError" class="text-danger error-message">{{ userSearchError }}</p>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div :class="['modal-content', 'card', modalSizeClass]">
        <div class="modal-header">
          <h3 class="modal-title-text">{{ modalTitle }}</h3>
          <button @click="closeModal" class="button-close" aria-label="Fechar modal">&times;</button>
        </div>

        <div v-if="modalMode === 'selectAnimals'" class="modal-body">
          <p>Destinatário: <strong>{{ foundRecipientUser.username }}</strong> (Hash: {{ foundRecipientUser.user_hash }})</p>
          <p>Selecione os animais que deseja transferir:</p>
          <div v-if="isLoadingAnimalsForSelection" class="loading-state small-loading">Carregando seus animais...</div>
          <ul v-else-if="userOwnedAnimals.length" class="animal-list-in-modal styled-list-group">
             <li v-for="animal in userOwnedAnimals" :key="animal.id" class="list-item">
                <label :for="`animal-transfer-check-${animal.id}`" class="animal-select-label">
                    <input 
                        type="checkbox" 
                        :id="`animal-transfer-check-${animal.id}`"
                        :value="animal.id" 
                        v-model="selectedAnimalIdsForTransfer" 
                        class="checkbox-input"
                        :disabled="!isAnimalTransferable(animal)"
                    />
                    <div class="animal-info-details">
                        <span class="animal-id-text">{{ animal.identification }}</span>
                        <span class="animal-detail-item">Raça: {{ animal.breed_name || 'N/D' }} (Espécie: {{ animal.specie_name || 'N/D' }})</span>
                        <span class="animal-detail-item">Status: 
                          <span :class="getStatusClass(animal.status_name)">{{ animal.status_name || 'N/D' }}</span>
                          <span v-if="!isAnimalTransferable(animal)" class="text-danger small-text"> (Não transferível)</span>
                        </span>
                    </div>
                </label>
            </li>
          </ul>
          <p v-else class="empty-state small-empty-state">Você não possui animais que podem ser transferidos no momento.</p>
          
          <div class="form-group modal-form-group">
            <label for="initiator-notes" class="form-label">Observações (Opcional):</label>
            <textarea id="initiator-notes" v-model="newRequestNotes" class="textarea" rows="2"></textarea>
          </div>

          <div class="form-actions">
            <button @click="confirmAndCreateRequest" class="button button-primary" :disabled="selectedAnimalIdsForTransfer.length === 0">
              Revisar e Enviar Solicitação ({{ selectedAnimalIdsForTransfer.length }})
            </button>
            <button type="button" class="button button-secondary" @click="closeModal">Cancelar</button>
          </div>
        </div>

        <div v-if="modalMode === 'viewDetails'" class="modal-body">
          <div v-if="currentRequestDetails">
            <p><strong>Solicitante:</strong> {{ currentRequestDetails.initiated_by_username }}</p>
            <p><strong>Destinatário:</strong> {{ currentRequestDetails.requested_to_username }}</p>
            <p><strong>Data da Solicitação:</strong> {{ formatDate(currentRequestDetails.request_date) }}</p>
            <p><strong>Status:</strong> <span :class="getRequestStatusClass(currentRequestDetails.status)">{{ currentRequestDetails.status_display }}</span></p>
            <p v-if="currentRequestDetails.initiator_notes"><strong>Obs. Solicitante:</strong> {{ currentRequestDetails.initiator_notes }}</p>
            <p v-if="currentRequestDetails.recipient_notes"><strong>Obs. Destinatário:</strong> {{ currentRequestDetails.recipient_notes }}</p>
            
            <h4>Animais na Solicitação ({{ currentRequestDetails.animals_details.length }}):</h4>
            <ul class="styled-list-group compact-list scrollable-list">
              <li v-for="animal in currentRequestDetails.animals_details" :key="animal.id" class="list-item-condensed">
                <strong>{{ animal.identification }}</strong> - {{ animal.breed_name || 'Raça N/D' }} ({{ animal.status_name || 'Status N/D'}})
              </li>
            </ul>
          </div>
          <div class="form-actions">
            <button type="button" class="button button-secondary" @click="closeModal">Fechar</button>
          </div>
        </div>

        <div v-if="['confirmAccept', 'confirmReject', 'confirmCancel'].includes(modalMode)" class="modal-body">
           <p>{{ confirmationMessage }}</p>
          <div v-if="modalMode === 'confirmAccept' || modalMode === 'confirmReject'" class="form-group modal-form-group">
            <label for="action-notes" class="form-label">Suas Observações (Opcional):</label>
            <textarea id="action-notes" v-model="actionNotes" class="textarea" rows="2"></textarea>
          </div>
          <div class="form-actions">
            <button @click="executeConfirmedAction" :class="['button', confirmationButtonClass]">
              {{ confirmationButtonText }}
            </button>
            <button type="button" class="button button-secondary" @click="closeModal">Cancelar</button>
          </div>
        </div>

      </div>
    </div>

    <NotificationModal
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
      :title="notification.title"
      @close="closeNotification"
    />
  </section>
</template>

<script>
import NotificationModal from '@/components/NotificationModal.vue';
import { 
  createTransferRequest, 
  listSentTransferRequests, 
  listReceivedTransferRequests, 
  getTransferRequestDetails, 
  cancelTransferRequest, 
  rejectTransferRequest, 
  approveAndProcessTransferRequest 
} from '@/services/transferService';
import { getAnimals } from '@/services/animalService';
import { getUserByHash, getUserProfile } from '@/services/userService'; // getUserByHash é novo

export default {
  name: 'TransferOwnershipContent',
  components: { NotificationModal },
  data() {
    return {
      isLoadingSentRequests: false,
      isLoadingReceivedRequests: false,
      isLoadingAnimalsForSelection: false,
      isLoadingUserByHash: false,
      // isLoadingAllUsers: false, // Não mais necessário para este componente

      sentRequests: [],
      receivedPendingRequests: [],
      userOwnedAnimals: [],
      // allUsers: [], // Não mais necessário para este componente

      recipientUserHash: '',
      foundRecipientUser: null,
      userSearchError: '',
      selectedAnimalIdsForTransfer: [],
      newRequestNotes: '',

      showModal: false,
      modalMode: '', 
      modalTitle: '',
      currentRequestDetails: null,
      actionNotes: '',

      notification: { show: false, message: '', type: 'success', title: '' },
      currentUser: null, 
    };
  },
  computed: {
    // ... (computed properties: modalSizeClass, confirmationMessage, etc. permanecem as mesmas)
    modalSizeClass() {
      if (this.modalMode === 'selectAnimals' || this.modalMode === 'viewDetails') {
        return 'large-modal';
      }
      return '';
    },
    confirmationMessage() {
      if (this.modalMode === 'confirmAccept') return `Tem certeza que deseja ACEITAR esta transferência de ${this.currentRequestDetails?.animals_details?.length || ''} animal(is) de ${this.currentRequestDetails?.initiated_by_username}? Os animais serão adicionados à sua propriedade.`;
      if (this.modalMode === 'confirmReject') return 'Tem certeza que deseja REJEITAR esta transferência?';
      if (this.modalMode === 'confirmCancel') return 'Tem certeza que deseja CANCELAR esta solicitação de transferência?';
      return '';
    },
    confirmationButtonText() {
      if (this.modalMode === 'confirmAccept') return 'Sim, Aceitar';
      if (this.modalMode === 'confirmReject') return 'Sim, Rejeitar';
      if (this.modalMode === 'confirmCancel') return 'Sim, Cancelar';
      return 'Confirmar';
    },
    confirmationButtonClass() {
      if (this.modalMode === 'confirmAccept') return 'button-success';
      if (this.modalMode === 'confirmReject' || this.modalMode === 'confirmCancel') return 'button-danger';
      return 'button-primary';
    }
  },
  methods: {
    // ... (showAppNotification, closeNotification, formatDate, getRequestStatusClass, getStatusClass, isAnimalTransferable) ...
    // ... (loadSentRequests, loadReceivedRequests) ...
    // Estas funções auxiliares e de carregamento de listas permanecem as mesmas.
    showAppNotification(message, type = 'success', title = '', duration = 4000) {
        let notificationTitle = title;
        if (!notificationTitle) {
            if (type === 'success') notificationTitle = 'Sucesso!';
            else if (type === 'error') notificationTitle = 'Erro!';
            else if (type === 'warning') notificationTitle = 'Atenção!';
            else notificationTitle = 'Informação';
        }
      this.notification = { message, type, title: notificationTitle, show: true };
      if (duration !== null && duration > 0) {
        setTimeout(() => this.closeNotification(), duration);
      }
    },
    closeNotification() {
      this.notification.show = false;
    },
    formatDate(dateString) {
      if (!dateString) return 'N/D';
      try {
        return new Date(dateString).toLocaleDateString('pt-BR', {
          day: '2-digit', month: '2-digit', year: 'numeric',
          hour: '2-digit', minute: '2-digit'
        });
      } catch (e) {
        return dateString;
      }
    },
    getRequestStatusClass(statusKey) {
      const statusClassMap = {
        PENDING_APPROVAL: 'status-badge status-warning',
        APPROVED: 'status-badge status-info',
        PROCESSING: 'status-badge status-processing',
        COMPLETED: 'status-badge status-active',
        REJECTED: 'status-badge status-danger',
        ERROR_PROCESSING: 'status-badge status-danger',
        CANCELLED_BY_INITIATOR: 'status-badge status-muted',
      };
      return statusClassMap[statusKey] || 'status-badge status-default';
    },
    getStatusClass(statusName) {
        if (!statusName) return 'status-badge status-default';
        const nameLower = statusName.toLowerCase();
        if (nameLower === 'ativo') return 'status-badge status-active';
        if (nameLower === 'vendido') return 'status-badge status-sold';
        if (nameLower === 'abatido') return 'status-badge status-slaughtered';
        if (nameLower === 'morto') return 'status-badge status-dead';
        return 'status-badge status-default';
    },
    isAnimalTransferable(animal) {
        const nonTransferableStatus = ['vendido', 'morto', 'abatido'];
        return animal.status_name && !nonTransferableStatus.includes(animal.status_name.toLowerCase());
    },
    async loadSentRequests() {
      this.isLoadingSentRequests = true;
      try {
        this.sentRequests = await listSentTransferRequests();
      } catch (error) {
        this.showAppNotification('Erro ao carregar solicitações enviadas.', 'error', 'Falha na Busca');
      } finally {
        this.isLoadingSentRequests = false;
      }
    },
    async loadReceivedRequests() {
      this.isLoadingReceivedRequests = true;
      try {
        this.receivedPendingRequests = await listReceivedTransferRequests();
      } catch (error) {
        this.showAppNotification('Erro ao carregar solicitações recebidas.', 'error', 'Falha na Busca');
      } finally {
        this.isLoadingReceivedRequests = false;
      }
    },
    async loadCurrentUser() {
        try {
            this.currentUser = await getUserProfile();
        } catch (error) {
            console.error("Erro ao carregar perfil do usuário logado:", error);
            this.showAppNotification('Não foi possível carregar dados do usuário logado.', 'error', 'Erro Interno');
        }
    },

    // MÉTODO MODIFICADO para usar getUserByHash do service
    async findUserByHashAndOpenModal() {
      const hashToSearch = this.recipientUserHash.trim();
      if (!hashToSearch) {
        this.userSearchError = 'O Hash de Usuário não pode estar vazio.';
        return;
      }
      if (this.currentUser && hashToSearch.toLowerCase() === this.currentUser.user_hash?.toLowerCase()) {
        this.userSearchError = 'Você não pode iniciar uma transferência para si mesmo.';
        return;
      }

      this.isLoadingUserByHash = true;
      this.userSearchError = '';
      try {
        // Chama o novo serviço para buscar o usuário pelo hash no backend
        const userData = await getUserByHash(hashToSearch); 
        // Assumindo que getUserByHash retorna o objeto do usuário se encontrado,
        // ou lança um erro (que será pego no catch) se não encontrado (ex: 404).
        this.foundRecipientUser = { // Mapeia os campos esperados
            id: userData.id, 
            username: userData.username, 
            user_hash: userData.user_hash 
        };
        this.openModalForAnimalSelection();
      } catch (error) {
        // @ts-ignore
        if (error.isClientError) { // Erro de validação do próprio serviço (hash vazio)
            this.userSearchError = error.message;
        // @ts-ignore
        } else if (error.detail) { // Erro vindo do backend com uma mensagem 'detail'
            this.userSearchError = error.detail;
        } else {
            this.userSearchError = 'Erro ao buscar usuário. Verifique o hash e tente novamente.';
        }
        console.error("Erro ao buscar usuário por hash:", error);
        this.foundRecipientUser = null;
      } finally {
        this.isLoadingUserByHash = false;
      }
    },

    // openModalForAnimalSelection, confirmAndCreateRequest, viewRequestDetails,
    // promptCancelRequest, promptRejectRequest, promptAcceptRequest, executeConfirmedAction, closeModal
    // permanecem com a mesma lógica interna, mas agora findUserByHashAndOpenModal é mais eficiente.
    async openModalForAnimalSelection() {
      this.modalTitle = 'Selecionar Animais para Transferência';
      this.modalMode = 'selectAnimals';
      this.selectedAnimalIdsForTransfer = [];
      this.newRequestNotes = '';
      this.showModal = true;
      
      this.isLoadingAnimalsForSelection = true;
      try {
        const allMyAnimals = await getAnimals();
        this.userOwnedAnimals = allMyAnimals.filter(animal => this.isAnimalTransferable(animal));
        if(this.userOwnedAnimals.length === 0){
            this.showAppNotification('Você não possui animais que podem ser transferidos no momento.', 'info', 'Aviso');
        }
      } catch (error) {
        this.showAppNotification('Erro ao carregar seus animais.', 'error', 'Falha na Busca');
        this.userOwnedAnimals = [];
      } finally {
        this.isLoadingAnimalsForSelection = false;
      }
    },
    async confirmAndCreateRequest() {
      if (this.selectedAnimalIdsForTransfer.length === 0) {
        this.showAppNotification('Selecione pelo menos um animal para transferir.', 'warning', 'Atenção');
        return;
      }
      if (!this.foundRecipientUser || !this.foundRecipientUser.id) {
        this.showAppNotification('Destinatário inválido. Por favor, busque o usuário pelo hash novamente.', 'error', 'Erro');
        return;
      }
      const payload = {
        animals: this.selectedAnimalIdsForTransfer,
        requested_to_id: this.foundRecipientUser.id,
        initiator_notes: this.newRequestNotes.trim()
      };
      try {
        await createTransferRequest(payload);
        this.showAppNotification('Solicitação de transferência enviada com sucesso!', 'success', 'Sucesso!');
        this.closeModal();
        this.recipientUserHash = '';
        this.foundRecipientUser = null;
        this.loadSentRequests();
      } catch (error) {
        const errorData = error.response?.data;
        let errorMsg = "Erro ao enviar solicitação.";
        if (typeof errorData === 'object' && errorData !== null) {
            errorMsg = Object.entries(errorData)
                .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                .join('; ');
        } else if (typeof errorData === 'string') {
            errorMsg = errorData;
        }
        this.showAppNotification(`Erro ao enviar solicitação: ${errorMsg}`, 'error', 'Falha no Envio');
      }
    },
    async viewRequestDetails(request) {
      this.modalTitle = 'Detalhes da Solicitação';
      this.modalMode = 'viewDetails';
      // @ts-ignore
      this.isLoadingDetails = true; 
      this.showModal = true;
      try {
        this.currentRequestDetails = await getTransferRequestDetails(request.id);
      } catch(error) {
        this.showAppNotification('Erro ao carregar detalhes da solicitação.', 'error', 'Falha na Busca');
        this.closeModal(); 
      } finally {
        // @ts-ignore
        this.isLoadingDetails = false;
      }
    },
    promptCancelRequest(request) {
      this.currentRequestDetails = request;
      this.modalTitle = 'Cancelar Solicitação';
      this.modalMode = 'confirmCancel';
      this.showModal = true;
    },
    promptRejectRequest(request) {
      this.currentRequestDetails = request;
      this.modalTitle = 'Rejeitar Solicitação';
      this.modalMode = 'confirmReject';
      this.actionNotes = '';
      this.showModal = true;
    },
    promptAcceptRequest(request) {
      this.currentRequestDetails = request;
      this.modalTitle = 'Aceitar Solicitação';
      this.modalMode = 'confirmAccept';
      this.actionNotes = '';
      this.showModal = true;
    },
    async executeConfirmedAction() {
      if (!this.currentRequestDetails || !this.currentRequestDetails.id) return;
      const requestId = this.currentRequestDetails.id;
      let actionPromise;
      let successMessage = '';
      let title = 'Sucesso!';

      try {
        if (this.modalMode === 'confirmCancel') {
          actionPromise = cancelTransferRequest(requestId);
          successMessage = 'Solicitação cancelada com sucesso.';
        } else if (this.modalMode === 'confirmReject') {
          actionPromise = rejectTransferRequest(requestId, { recipient_notes: this.actionNotes.trim() });
          successMessage = 'Solicitação rejeitada com sucesso.';
        } else if (this.modalMode === 'confirmAccept') {
          actionPromise = approveAndProcessTransferRequest(requestId, { recipient_notes: this.actionNotes.trim() });
          successMessage = 'Transferência aprovada e processada com sucesso!';
        } else { return; }
        
        await actionPromise;
        this.showAppNotification(successMessage, 'success', title);
        this.closeModal();
        this.fetchAllRequests();
      } catch (error) {
        const errorData = error.response?.data;
        let errorDetail = "Erro ao executar ação.";
         if (errorData && errorData.error) { 
            errorDetail = errorData.error;
        } else if (errorData && errorData.detail) { // Captura o 'detail' do 404 ou 400 do backend
            errorDetail = errorData.detail;
        } else if (typeof errorData === 'object' && errorData !== null) {
            errorDetail = Object.entries(errorData)
                .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
                .join('; ');
        } else if (typeof errorData === 'string') {
            errorDetail = errorData;
        }
        this.showAppNotification(`Erro: ${errorDetail}`, 'error', 'Falha na Operação', 6000);
      }
    },
    closeModal() {
      this.showModal = false;
      this.modalMode = '';
      this.currentRequestDetails = null;
      this.selectedAnimalIdsForTransfer = [];
      this.newRequestNotes = '';
      this.actionNotes = '';
    },
    fetchAllRequests() {
      this.loadSentRequests();
      this.loadReceivedRequests();
    },
    async copyToClipboard(textToCopy) {
      if (!textToCopy) return;
      try {
        await navigator.clipboard.writeText(textToCopy);
        this.showAppNotification('Hash copiado para a área de transferência!', 'success', 'Copiado!');
      } catch (err) {
        console.error('Falha ao copiar hash: ', err);
        // Tenta um fallback ou informa o usuário se o clipboard API não estiver disponível/permitido
        if (document.execCommand) {
            const textArea = document.createElement("textarea");
            textArea.value = textToCopy;
            textArea.style.position = "fixed"; // Evita scroll
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                this.showAppNotification('Hash copiado para a área de transferência!', 'success', 'Copiado!');
            } catch (execErr) {
                console.error('Falha ao copiar com execCommand: ', execErr);
                this.showAppNotification('Falha ao copiar. Seu navegador pode não suportar esta ação ou permissão foi negada.', 'warning', 'Aviso', 6000);
            }
            document.body.removeChild(textArea);
        } else {
            this.showAppNotification('Falha ao copiar. Seu navegador pode não suportar esta ação.', 'warning', 'Aviso', 6000);
        }
      }
    }
  },
  async mounted() {
    await this.loadCurrentUser(); // Carrega dados do usuário logado primeiro
    // this.loadAllUsersForLookup(); // Não mais necessário carregar todos os usuários aqui
    this.fetchAllRequests(); // Carrega solicitações enviadas e recebidas
  }
}
</script>

<style scoped>
/* ... (seus estilos existentes para .transfer-ownership-panel, .transfer-layout, .column, etc.) ... */
/* Adicione este novo estilo para a seção do hash do usuário */
.current-user-hash-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-sm) var(--sp-md);
  margin-bottom: var(--sp-lg);
  background-color: var(--color-bg-muted); /* Um fundo sutil */
  border-left: 4px solid var(--color-primary); /* Destaque */
}
.hash-info {
  display: flex;
  flex-direction: column;
  gap: var(--sp-xxs);
}
.hash-label {
  font-size: var(--fs-small);
  color: var(--color-text-secondary);
}
.hash-value {
  font-family: var(--font-monospace); /* Fonte monoespaçada para hashes */
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
  cursor: pointer; /* Indica que é clicável */
  padding: var(--sp-xxs) var(--sp-xs);
  background-color: var(--color-white);
  border: 1px dashed var(--color-border);
  border-radius: var(--border-radius-sm);
  transition: background-color var(--transition-fast);
}
.hash-value:hover {
  background-color: var(--color-primary-light);
}
.current-user-hash-section .button svg {
  margin-right: var(--sp-xs); /* Espaço entre ícone e texto no botão copiar */
}
/* Outros estilos como definidos anteriormente */
.transfer-ownership-panel {}
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
}
.panel-description {
  text-align: left; 
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  font-size: var(--fs-base);
}
.transfer-layout {
  display: flex;
  gap: var(--sp-lg);
  flex-wrap: wrap; 
}
.column {
  flex: 1;
  min-width: 320px;
  padding: var(--sp-md);
  background-color: var(--color-bg-component);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}
.column-title {
  font-size: var(--fs-h5);
  color: var(--color-primary);
  margin-bottom: var(--sp-md);
  padding-bottom: var(--sp-sm);
  border-bottom: var(--border-width) solid var(--color-border-light);
  text-align: center;
}
.request-section {
  margin-bottom: var(--sp-lg);
}
.request-section h4 {
  font-size: var(--fs-large);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-sm);
  display: flex;
  align-items: center;
  gap: var(--sp-xs);
}
.request-section h4 svg {
  color: var(--color-primary); 
  flex-shrink: 0;
}
.styled-list-group.compact-list .list-item {
  padding: var(--sp-sm); 
  margin-bottom: var(--sp-xs);
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
}
.request-item .item-info {
    flex-grow: 1; 
}
.request-item .item-info span {
  display: block;
  font-size: var(--fs-small);
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-xxs);
}
.request-item .item-info strong {
  color: var(--color-text-primary);
}
.request-item .request-date {
  font-size: var(--fs-smaller);
  color: var(--color-text-muted);
  margin-top: var(--sp-xxs);
}
.request-item .item-actions {
  display: flex;
  flex-direction: column;
  gap: var(--sp-xs);
  align-items: flex-end; 
  flex-shrink: 0; 
  margin-left: var(--sp-sm); 
}
@media (min-width: 500px) { 
    .request-item .item-actions {
        flex-direction: row; 
        align-items: center;
    }
}
.column-divider {
  margin-top: var(--sp-lg);
  margin-bottom: var(--sp-lg);
  border-color: var(--color-border-light);
}
.single-column-form .form-group {
  grid-column: 1 / -1; 
}
.single-column-form .form-actions {
  justify-content: flex-start; 
  margin-top: var(--sp-md); 
}
.error-message {
    margin-top: var(--sp-sm);
    font-size: var(--fs-small);
}
.text-danger { 
  color: var(--color-danger) !important; 
}
.small-text {
    font-size: var(--fs-smaller);
}
.modal-form-group {
    margin-top: var(--sp-md);
    margin-bottom: var(--sp-md); 
}
.animal-list-in-modal {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--sp-md);
  max-height: 300px; 
  overflow-y: auto;
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-sm);
}
.animal-list-in-modal .list-item {
  padding: var(--sp-sm) var(--sp-md);
  border-bottom: var(--border-width) solid var(--color-border-light);
}
.animal-list-in-modal .list-item:last-child {
  border-bottom: none;
}
.animal-list-in-modal .list-item:hover {
  background-color: var(--color-bg-hover);
}
.animal-select-label {
    display: flex;
    align-items: center;
    gap: var(--sp-sm);
    width: 100%;
    cursor: pointer;
}
.checkbox-input {
  transform: scale(1.2);
  margin-right: var(--sp-xs);
  flex-shrink: 0;
  accent-color: var(--color-primary); 
}
.animal-info-details {
  flex-grow: 1;
  text-align: left;
  font-size: var(--fs-base);
}
.animal-id-text {
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
}
.animal-detail-item {
    display: block;
    font-size: var(--fs-small);
    color: var(--color-text-secondary);
    margin-top: var(--sp-xxs);
}
.status-badge { 
    font-size: var(--fs-smaller);
    padding: calc(var(--sp-xxs) / 1.5) var(--sp-xs); 
    border-radius: var(--border-radius-pill);
    font-weight: var(--fw-medium);
    color: var(--color-text-inverted);
    text-transform: uppercase;
    letter-spacing: 0.5px; 
    line-height: 1.2; 
    display: inline-block; 
}
.status-warning { background-color: var(--color-warning); color: var(--color-text-primary); }
.status-info { background-color: var(--color-info); }
.status-processing { background-color: var(--color-secondary); }
.status-active { background-color: var(--color-success); } 
.status-danger { background-color: var(--color-danger); } 
.status-muted { background-color: var(--color-text-muted); } 
.status-default { background-color: var(--color-text-secondary); }
.loading-state.small-loading {
    padding: var(--sp-md);
    font-size: var(--fs-base);
    text-align: center;
    color: var(--color-text-muted);
}
.empty-state.small-empty-state {
    padding: var(--sp-md);
    font-size: var(--fs-small);
    text-align: left;
    color: var(--color-text-muted);
    background-color: transparent;
    border: var(--border-width) dashed var(--color-border);
    border-radius: var(--border-radius-sm);
}
.scrollable-list {
    max-height: 200px; 
    overflow-y: auto;
    border: var(--border-width) solid var(--color-border-light);
    padding: var(--sp-xs);
    border-radius: var(--border-radius-sm);
    background-color: var(--color-bg-muted);
}
.list-item-condensed {
    font-size: var(--fs-small);
    padding: var(--sp-xs);
    border-bottom: var(--border-width) solid var(--color-border-light);
    background-color: var(--color-bg-component);
}
.list-item-condensed:last-child {
    border-bottom: none;
}
.list-item-condensed strong {
    color: var(--color-text-primary);
}
</style>