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
 * @param {Object} data - Dados do evento.
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
 * @param {string} registrar - Endereço da carteira.
 */
export async function addRegistrar(registrar) {
  try {
    // Envia o objeto com a chave "registrar_address"
    const response = await axiosInstance.post('contract/add-registrar/', { registrar_address: registrar });
    return response.data;
  } catch (error) {
    console.error('Erro ao adicionar registrador:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Remove um registrador (carteira) do contrato.
 * @param {string} registrar - Endereço da carteira.
 */
export async function removeRegistrar(registrar) {
  try {
    const response = await axiosInstance.post('contract/remove-registrar/', { registrar });
    return response.data;
  } catch (error) {
    console.error('Erro ao remover registrador:', error);
    throw error;
  }
}

/**
 * Obtém um evento por animal e índice.
 * @param {number} animalId - ID do animal.
 * @param {number} index - Índice do evento (opcional, default 0).
 */
export async function getEventByAnimal(animalId, index = 0) {
  try {
    const response = await axiosInstance.get(`contract/get-event/${animalId}/`, {
      params: { index }
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter evento por animal:', error);
    throw error;
  }
}

/**
 * Obtém o número de eventos para um animal.
 * @param {number} animalId - ID do animal.
 */
export async function getNumberOfEvents(animalId) {
  try {
    const response = await axiosInstance.get(`contract/get-number/${animalId}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao obter número de eventos:', error);
    throw error;
  }
}