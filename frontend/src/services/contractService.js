import axiosInstance from './axiosSetup';

/**
 * Verifica o status do funcionamento do contrato.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function checkContractStatus() {
  try {
    const response = await axiosInstance.get('contract/status/');
    return response.data;
  } catch (e) {
    console.error('Erro ao verificar status do contrato:', e);
    throw e;
  }
}

/**
 * Registra o evento critico utilizando o contrato.
 * @param {Object} data - Dados do evento critico.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function registerCriticalEvent(data) {
  try {
    const response = await axiosInstance.post('contract/register-event/', data);
    return response.data;
  } catch (e) {
    console.error('Erro ao registrar evento critico:', e);
    throw e;
  }
}

/**
 * Obtém a quantidade de eventos para um animal especifico.
 * @param {string} animalId - ID do animal.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function getAnimalEvents(animalId) {
  try {
    const response = await axiosInstance.get(`contract/get-event/${animalId}/`);
    return response.data;
  } catch (e) {
    console.error('Erro ao obter eventos do animal:', e);
    throw e;
  }
}

