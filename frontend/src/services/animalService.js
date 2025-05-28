import axiosInstance from './axiosSetup';

/**
 * Registra um novo animal.
 * @param {Object} data - Dados do animal.
 * @returns {Promise<Object>} - Dados do animal cadastrado.
 */
export async function registerAnimal(data) {
  try {
    const response = await axiosInstance.post('animal/animal-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar animal:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém os dados de um animal pelo ID.
 * @param {number} id - ID do animal.
 * @returns {Promise<Object>} - Dados do animal.
 */
export async function getAnimal(id) {
  try {
    const response = await axiosInstance.get(`animal/animal-get/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao obter animal:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém todos os animais (ou os filtrados).
 * @param {Object} filters - Parâmetros de filtro (opcional).
 * @returns {Promise<Array>} - Lista de animais.
 */
export async function getAnimals(filters = {}) {
  try {
    const response = await axiosInstance.get('animal/animal-get/', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter lista de animais:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Busca animais pela string de identificação (busca parcial, case-insensitive).
 * @param {string} identificationString - A string de identificação para buscar.
 * @returns {Promise<Array>} - Lista de animais que correspondem à busca.
 */
export async function searchAnimalsByIdentification(identificationString) {
  try {
    // O backend deve ter um endpoint que suporte ?identification__icontains=valor
    const response = await axiosInstance.get('animal/animal-filter/', { // Ou o endpoint correto de filtro de animais
      params: { identification__icontains: identificationString }
    });
    return response.data; // Espera-se uma lista de objetos de animais [{id, identification, ...}]
  } catch (error) {
    console.error('Erro ao buscar animais por identificação:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Atualiza um animal.
 * @param {number} id - ID do animal a ser atualizado.
 * @param {Object} data - Dados para atualização.
 * @returns {Promise<Object>} - Dados do animal atualizado.
 */
export async function updateAnimal(id, data) {
  try {
    const response = await axiosInstance.put(`animal/animal-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar animal:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Deleta um animal.
 * @param {number} id - ID do animal a ser deletado.
 * @returns {Promise<void>} - Resposta da API.
 */
export async function deleteAnimal(id) {
  try {
    const response = await axiosInstance.delete(`animal/animal-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar animal:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Atualiza múltiplos campos (status, grupo, tipo de identificação, raça, espécie) de animais em lote.
 * @param {Array<number>} animal_ids - Lista de IDs dos animais a serem atualizados.
 * @param {Object} updateData - Objeto contendo os campos e novos IDs (ex: { new_status_id: 1, new_group_id: 5 }).
 * @returns {Promise<Object>} - Resposta da API, incluindo a contagem de animais atualizados.
*/
export async function updateAnimalsBatch(animal_ids, updateData) {
  try {
    const response = await axiosInstance.patch('animal/update-batch/', {
      animal_ids,
      ...updateData // Espalha os campos de atualização diretamente
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar animais em lote:', error.response ? error.response.data : error);
    throw error;
  }
}