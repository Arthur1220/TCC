// src/services/blockchainService.js
import axiosInstance from './axiosSetup';

/**
 * Registra um novo registro na tabela Blockchain.
 * Exige: animal, event, transaction_hash e status.
 * O owner é definido automaticamente no backend (request.user).
 * @param {Object} data - Dados do registro.
 * @returns {Promise<Object>}
 */
export async function registerBlockchain(data) {
  try {
    const response = await axiosInstance.post('blockchain/blockchain-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar blockchain:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Retorna todos os registros da blockchain.
 * @returns {Promise<Array>}
 */
export async function getBlockchains() {
  try {
    const response = await axiosInstance.get('blockchain/blockchain-get/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter registros de blockchain:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Atualiza um registro da blockchain pelo ID.
 * @param {number} id - ID do registro.
 * @param {Object} data - Dados para atualização.
 * @returns {Promise<Object>}
 */
export async function updateBlockchain(id, data) {
  try {
    const response = await axiosInstance.put(`blockchain/blockchain-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar blockchain:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Deleta um registro da blockchain pelo ID.
 * @param {number} id - ID do registro.
 * @returns {Promise<Object>}
 */
export async function deleteBlockchain(id) {
  try {
    const response = await axiosInstance.delete(`blockchain/blockchain-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar blockchain:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Filtra os registros de blockchain com base nos parâmetros enviados.
 * @param {Object} filters - Objeto com filtros (ex: {animal: 1}).
 * @returns {Promise<Array>}
 */
export async function filterBlockchain(filters) {
  try {
    const response = await axiosInstance.get('blockchain/blockchain-filter/', {
      params: filters
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao filtrar registros de blockchain:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém os custos de blockchain para o usuário logado, com filtros opcionais.
 * @param {Object} filters - Filtros opcionais.
 * Ex: { filter_type: 'last_month' }
 * Ex: { filter_type: 'specific_month', year: 2025, month: 5 }
 * Ex: { filter_type: 'by_month_in_year', year: 2025 }
 * Ex: { filter_type: 'all_months_summary' }
 * Se nenhum filtro for passado, o backend assume 'all_time'.
 * @returns {Promise<Object>} - Objeto com os custos.
 */
export async function fetchUserBlockchainCosts(filters = {}) {
  try {
    const response = await axiosInstance.get('blockchain/user-costs/', { params: filters }); 
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar custos de blockchain do usuário:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Busca o resumo dos custos de blockchain para o usuário logado.
 * @returns {Promise<Object>} - Objeto com os custos.
 */
export async function fetchUserBlockchainCostsSummary() {
  try {
    // Ajuste a URL para corresponder exatamente ao seu endpoint Django
    // Ex: 'api/blockchain/user-costs-summary/'
    const response = await axiosInstance.get(`blockchain/user-costs-summary/`); 
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar resumo de custos da blockchain:', error.response ? error.response.data : error);
    throw error; // Permite que o componente trate o erro
  }
}