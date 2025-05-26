// src/services/contractService.js
import axiosInstance from './axiosSetup';

/**
 * Verifica o status do contrato.
 */
export async function checkContractStatus() {
  //console.log("DEBUG - checkContractStatus: Chamando /contract/status/");
  try {
    const response = await axiosInstance.get('contract/status/');
    //console.log("DEBUG - checkContractStatus: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - checkContractStatus: Erro ao verificar status do contrato:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Registra um evento crítico no contrato.
 * @param {Object} data - Dados do evento (event_id, animal_id, event_type, data_hash, user_hash)
 */
export async function registerContractEvent(data) {
  //console.log("DEBUG - registerContractEvent: Payload enviado:", data);
  try {
    const response = await axiosInstance.post('contract/register-event/', data);
    //console.log("DEBUG - registerContractEvent: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - registerContractEvent: Erro ao registrar evento crítico:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Adiciona um novo registrador (carteira) no contrato.
 * @param {string} address - Endereço da carteira.
 */
export async function addRegistrar(address) {
  //console.log("DEBUG - addRegistrar: Chamando /contract/add-registrar/ com endereço:", address);
  try {
    // Envia o objeto com a chave "registrar_address"
    const response = await axiosInstance.post('contract/add-registrar/', { registrar_address: address });
    //console.log("DEBUG - addRegistrar: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - addRegistrar: Erro ao adicionar registrador:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Remove um registrador (carteira) do contrato.
 * @param {string} address - Endereço da carteira.
 */
export async function removeRegistrar(address) {
  //console.log("DEBUG - removeRegistrar: Chamando /contract/remove-registrar/ com endereço:", address);
  try {
    const response = await axiosInstance.post('contract/remove-registrar/', { address });
    //console.log("DEBUG - removeRegistrar: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - removeRegistrar: Erro ao remover registrador:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém um evento específico por animal e índice.
 * @param {number} animalId - ID do animal.
 * @param {number} index - Índice do evento (default: 0).
 */
export async function getContractEvent(animalId, index = 0) {
  //console.log(`DEBUG - getContractEvent: Chamando /contract/get-event/${animalId}/ com index: ${index}`);
  try {
    const response = await axiosInstance.get(
      `contract/get-event/${animalId}/`,
      { params: { index } }
    );
    //console.log("DEBUG - getContractEvent: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - getContractEvent: Erro ao obter evento por animal:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Lista todos os eventos de um animal.
 * @param {number} animalId - ID do animal.
 */
export async function listContractEvents(animalId) {
  //console.log(`DEBUG - listContractEvents: Chamando /contract/list-events/${animalId}/`);
  try {
    const response = await axiosInstance.get(
      `contract/list-events/${animalId}/`
    );
    //console.log("DEBUG - listContractEvents: Resposta recebida:", response.data);
    return response.data.events;
  } catch (error) {
    console.error('ERRO - listContractEvents: Erro ao listar eventos do contrato:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém o número de eventos para um animal.
 * @param {number} animalId - ID do animal.
 */
export async function getNumberOfEvents(animalId) {
  //console.log(`DEBUG - getNumberOfEvents: Chamando /contract/get-number-events/ com animal_id: ${animalId}`);
  try {
    const response = await axiosInstance.get(
      'contract/get-number-events/',
      { params: { animal_id: animalId } }
    );
    //console.log("DEBUG - getNumberOfEvents: Resposta recebida:", response.data);
    return response.data.count;
  } catch (error) {
    console.error('ERRO - getNumberOfEvents: Erro ao obter número de eventos:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Pausa o contrato.
 */
export async function pauseContract() {
  //console.log("DEBUG - pauseContract: Chamando /contract/pause/");
  try {
    const response = await axiosInstance.post('contract/pause/');
    //console.log("DEBUG - pauseContract: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - pauseContract: Erro ao pausar contrato:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Despausa o contrato.
 */
export async function unpauseContract() {
  //console.log("DEBUG - unpauseContract: Chamando /contract/unpause/");
  try {
    const response = await axiosInstance.post('contract/unpause/');
    //console.log("DEBUG - unpauseContract: Resposta recebida:", response.data);
    return response.data;
  } catch (error) {
    console.error('ERRO - unpauseContract: Erro ao despausar contrato:', error.response ? error.response.data : error);
    throw error;
  }
}