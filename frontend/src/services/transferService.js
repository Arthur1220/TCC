import axiosInstance from './axiosSetup'; // Certifique-se que o caminho para axiosSetup está correto

const BASE_URL = 'transfer/requests'; // Base URL para as rotas de transferência

/**
 * Cria uma nova solicitação de transferência de titularidade.
 * @param {Object} requestData - Dados da solicitação.
 * Ex: { animals: [animalId1, animalId2], requested_to_id: userId, initiator_notes: "..." }
 * @returns {Promise<Object>} - Dados da solicitação criada.
 */
export async function createTransferRequest(requestData) {
  try {
    const response = await axiosInstance.post(`${BASE_URL}/create/`, requestData);
    return response.data;
  } catch (error) {
    console.error('Erro ao criar solicitação de transferência:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Lista as solicitações de transferência enviadas pelo usuário logado.
 * @returns {Promise<Array<Object>>} - Lista de solicitações enviadas.
 */
export async function listSentTransferRequests() {
  try {
    const response = await axiosInstance.get(`${BASE_URL}/sent/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao listar solicitações de transferência enviadas:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Lista as solicitações de transferência recebidas pelo usuário logado (pendentes de aprovação).
 * @returns {Promise<Array<Object>>} - Lista de solicitações recebidas.
 */
export async function listReceivedTransferRequests() {
  try {
    const response = await axiosInstance.get(`${BASE_URL}/received/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao listar solicitações de transferência recebidas:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém os detalhes de uma solicitação de transferência específica.
 * @param {number} requestId - ID da solicitação de transferência.
 * @returns {Promise<Object>} - Dados da solicitação.
 */
export async function getTransferRequestDetails(requestId) {
  try {
    const response = await axiosInstance.get(`${BASE_URL}/${requestId}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao obter detalhes da solicitação de transferência:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Cancela uma solicitação de transferência (pelo solicitante).
 * @param {number} requestId - ID da solicitação a ser cancelada.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function cancelTransferRequest(requestId) {
  try {
    const response = await axiosInstance.post(`${BASE_URL}/${requestId}/cancel/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao cancelar solicitação de transferência:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Rejeita uma solicitação de transferência (pelo destinatário).
 * @param {number} requestId - ID da solicitação a ser rejeitada.
 * @param {Object} data - Dados para a rejeição (ex: { recipient_notes: "..." }).
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function rejectTransferRequest(requestId, data = {}) {
  try {
    const response = await axiosInstance.post(`${BASE_URL}/${requestId}/reject/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao rejeitar solicitação de transferência:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Aprova e processa uma solicitação de transferência (pelo destinatário).
 * @param {number} requestId - ID da solicitação a ser aprovada.
 * @param {Object} data - Dados para a aprovação (ex: { recipient_notes: "..." }).
 * @returns {Promise<Object>} - Dados da solicitação atualizada (status COMPLETED ou ERROR).
 */
export async function approveAndProcessTransferRequest(requestId, data = {}) {
  try {
    const response = await axiosInstance.post(`${BASE_URL}/${requestId}/approve/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao aprovar e processar solicitação de transferência:', error.response ? error.response.data : error);
    throw error;
  }
}