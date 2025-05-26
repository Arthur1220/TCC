import axiosInstance from './axiosSetup';

/**
 * Obtém a lista de espécies.
 * @returns {Promise<Array>}
 */
export async function getSpecies() {
  try {
    const response = await axiosInstance.get('animal/species/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter espécies:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de raças.
 * @returns {Promise<Array>}
 */
export async function getBreeds() {
  try {
    const response = await axiosInstance.get('animal/breed/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter raças:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de grupos de animais.
 * @returns {Promise<Array>}
 */
export async function getAnimalGroups() {
  try {
    const response = await axiosInstance.get('animal/animal-group/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter grupos de animais:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Cadastra um novo grupo de animais.
 * @param {Object} data - Dados do novo grupo (name, description, owner).
 * @returns {Promise<Object>} - Dados do grupo criado.
 */
export async function registerAnimalGroup(data) {
  try {
    const response = await axiosInstance.post('animal/animal-group/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar novo grupo de animais:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de gêneros.
 * @returns {Promise<Array>}
 */
export async function getGenders() {
  try {
    const response = await axiosInstance.get('animal/gender/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter gêneros:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de status.
 * @returns {Promise<Array>}
 */
export async function getStatuses() {
  try {
    const response = await axiosInstance.get('animal/status/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter status:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de tipos de identificação.
 * @returns {Promise<Array>}
 */
export async function getIdentificationTypes() {
  try {
    const response = await axiosInstance.get('animal/identification-type/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter tipos de identificação:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de tipos de eventos em ordem alfabética.
 * @returns {Promise<Array>}
 */
export async function getEventTypes() {
  try {
    const response = await axiosInstance.get('event/event-type/');
    // Ordena a lista de tipos de eventos pelo campo "name"
    const sortedEventTypes = response.data.sort((a, b) => {
      return a.name.localeCompare(b.name);
    });
    return sortedEventTypes;
  } catch (error) {
    console.error('Erro ao obter tipos de eventos:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém a lista de propriedades.
 * @returns {Promise<Array>}
 */
export async function getProperties() {
  try {
    const response = await axiosInstance.get('property/get/'); // Confirme se este é o endpoint correto
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar propriedades:', error.response ? error.response.data : error);
    throw error;
  }
}