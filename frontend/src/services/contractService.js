import axiosInstance from './axiosSetup';

/**
 * Verifica o status do contrato.
 */
export async function checkContractStatus() {
  try {
    const response = await axiosInstance.get('contract/status/');
    return response.data;
  } catch (error) {
    console.error('Erro ao verificar status do contrato:', error);
    throw error;
  }
}

/**
 * Registra um evento crítico no contrato.
 * @param {Object} data - Dados do evento (event_id, animal_id, event_type, data_hash, user_hash)
 */
export async function registerContractEvent(data) {
  try {
    console.log("DEBUG - registerContractEvent payload:", data);
    const response = await axiosInstance.post('contract/register-event/', data);
    console.log("DEBUG - Response from registerContractEvent:", response.data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar evento crítico:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Adiciona um novo registrador (carteira) no contrato.
 * @param {string} address - Endereço da carteira.
 */
export async function addRegistrar(address) {
  try {
    // Envia o objeto com a chave "registrar_address"
    const response = await axiosInstance.post('contract/add-registrar/', { registrar_address: address });
    return response.data;
  } catch (error) {
    console.error('Erro ao adicionar registrador:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Remove um registrador (carteira) do contrato.
 * @param {string} address - Endereço da carteira.
 */
export async function removeRegistrar(address) {
  try {
    const response = await axiosInstance.post('contract/remove-registrar/', { address });
    return response.data;
  } catch (error) {
    console.error('Erro ao remover registrador:', error);
    throw error;
  }
}

/**
 * Obtém um evento específico por animal e índice.
 * @param {number} animalId - ID do animal.
 * @param {number} index - Índice do evento (default: 0).
 */
export async function getContractEvent(animalId, index = 0) {
  try {
    const response = await axiosInstance.get(
      `contract/get-event/${animalId}/`,
      { params: { index } }
    );
    return response.data;
  } catch (error) {
    console.error('Erro ao obter evento por animal:', error);
    throw error;
  }
}

/**
 * Lista todos os eventos de um animal.
 * @param {number} animalId - ID do animal.
 */
export async function listContractEvents(animalId) {
  try {
    const response = await axiosInstance.get(
      `contract/list-events/${animalId}/`
    );
    return response.data.events;
  } catch (error) {
    console.error('Erro ao listar eventos do contrato:', error);
    throw error;
  }
}

/**
 * Obtém o número de eventos para um animal.
 * @param {number} animalId - ID do animal.
 */
export async function getNumberOfEvents(animalId) {
  try {
    const response = await axiosInstance.get(
      'contract/get-number-events/',
      { params: { animal_id: animalId } }
    );
    return response.data.count;
  } catch (error) {
    console.error('Erro ao obter número de eventos:', error);
    throw error;
  }
}

/**
 * Pausa o contrato.
 */
export async function pauseContract() {
  try {
    const response = await axiosInstance.post('contract/pause/');
    return response.data;
  } catch (error) {
    console.error('Erro ao pausar contrato:', error);
    throw error;
  }
}

/**
 * Despausa o contrato.
 */
export async function unpauseContract() {
  try {
    const response = await axiosInstance.post('contract/unpause/');
    return response.data;
  } catch (error) {
    console.error('Erro ao despausar contrato:', error);
    throw error;
  }
}