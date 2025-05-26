// src/services/eventService.js
import axiosInstance from './axiosSetup';
import { getEventTypes, getProperties } from './lookupService'; // Importa getEventTypes e getProperties do lookupService

/**
 * Registra um novo evento individual.
 * @param {Object} data - Dados do evento (deve incluir animal, event_type, date, location, observations, etc.)
 * @returns {Promise<Object>} - Dados do evento registrado.
 */
export async function registerEvent(data) {
  try {
    const response = await axiosInstance.post('event/event-register/', data);
    return response.data;
  } catch (error) {
    console.error("Erro ao registrar evento:", error);
    throw error.response ? error.response.data : error;
  }
}

/**
 * Obtém os dados de um evento pelo ID.
 * @param {number} id - ID do evento.
 * @returns {Promise<Object>} - Dados do evento.
 */
export async function getEvents(id) {
  try {
    // Se um ID específico for passado, busca apenas aquele evento
    // Caso contrário, busca todos os eventos do usuário logado (assumindo que o backend já faz essa filtragem)
    const url = id ? `event/event-get/${id}/` : `event/event-get/`;
    const response = await axiosInstance.get(url);
    return response.data;
  } catch (error) {
    console.error("Erro ao obter evento:", error);
    throw error.response ? error.response.data : error;
  }
}

/**
 * Atualiza os dados de um evento.
 * @param {number} id - ID do evento a atualizar.
 * @param {Object} data - Dados atualizados do evento.
 * @returns {Promise<Object>} - Dados do evento atualizado.
 */
export async function updateEvent(id, data) {
  try {
    const response = await axiosInstance.put(`event/event-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar evento:", error);
    throw error.response ? error.response.data : error;
  }
}

/**
 * Deleta um evento pelo ID.
 * @param {number} id - ID do evento a ser deletado.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function deleteEvent(id) {
  try {
    const response = await axiosInstance.delete(`event/event-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao deletar evento:", error);
    throw error.response ? error.response.data : error;
  }
}

/**
 * Filtra eventos com base nos parâmetros passados.
 * @param {Object} queryParams - Objeto contendo os filtros (ex.: { animal: 1, event_type: 2 }).
 * @returns {Promise<Array>} - Lista de eventos que atendem aos filtros.
*/
export async function filterEvents(queryParams) {
  try {
    const response = await axiosInstance.get('event/event-filter/', {
      params: queryParams
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao filtrar eventos:", error);
    throw error.response ? error.response.data : error;
  }
}
  
/**
 * Função para recuperar os detalhes completos de um evento.
 * Essa função obtém os dados gerais do evento e, com base no tipo,
 * chama o endpoint específico para pegar os detalhes.
 *
 * @param {number} eventId - O ID do evento geral.
 * @param {number} eventTypeId - O ID do tipo de evento.
 * @returns {Promise<Object>} - Objeto contendo os dados gerais e os detalhes.
 */
export async function getEventDetails(eventId, eventTypeId) {
  try {
    // Primeiro, obtém os dados gerais do evento.
    const eventData = await getEvents(eventId); // Busca o evento pelo ID

    let detailData = null;
    const eventTypeName = (await getEventTypes()).find(type => type.id === eventTypeId)?.name; // Buscar o nome do tipo de evento
    
    // A API de detalhes específicos deve filtrar pelo ID do Evento principal
    // Assumi que os endpoints `getMovement`, `getWeighing`, etc. podem receber o `eventId`
    // e retornar o detalhe específico associado a ele.
    switch (eventTypeName.toLowerCase()) {
      case 'movimento':
        detailData = (await getMovements(null, { event: eventData.id }))[0]; // Assume que retorna uma lista, pega o primeiro
        break;
      case 'pesagem':
        detailData = (await getWeighings(null, { event: eventData.id }))[0];
        break;
      case 'vacinação':
        detailData = (await getVacines(null, { event: eventData.id }))[0];
        break;
      case 'medicação':
        detailData = (await getMedicines(null, { event: eventData.id }))[0];
        break;
      case 'reprodução':
        detailData = (await getReproductions(null, { event: eventData.id }))[0];
        break;
      case 'abate':
        detailData = (await getSlaughters(null, { event: eventData.id }))[0];
        break;
      case 'ocorrência especial':
        detailData = (await getSpecialOccurrences(null, { event: eventData.id }))[0];
        break;
      default:
        console.warn("Tipo de evento não reconhecido para detalhes.");
        break;
    }
    return { ...eventData, details: detailData };
  } catch (error) {
    console.error("Erro ao obter detalhes do evento:", error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Registra um evento para múltiplos animais (lote).
 * @param {Object} payload - Dados do evento em lote, incluindo animal_ids e detalhes específicos.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function registerBatchEvent(payload) {
  try {
    const response = await axiosInstance.post('event/event-register-batch/', payload);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar evento em lote:', error);
    throw error.response ? error.response.data : error;
  }
}


/** ############### MOVEMENT ############### **/
// Todas as funções abaixo foram atualizadas para incluir um parâmetro queryParams,
// o que permite filtrar por 'event' ID no backend se necessário.

export async function registerMovement(data) {
  try {
    const response = await axiosInstance.post('event/movement-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar movimento:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getMovements(id = null, queryParams = {}) {
  try {
    const url = id ? `event/movement-get/${id}/` : `event/movement-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter movimentos:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateMovement(id, data) {
  try {
    const response = await axiosInstance.put(`event/movement-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar movimento:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteMovement(id) {
  try {
    const response = await axiosInstance.delete(`event/movement-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar movimento:', error.response ? error.response.data : error);
    throw error;
  }
}

/** ############### WEIGHING (PESAGEM) ############### **/

export async function registerWeighing(data) {
  try {
    const response = await axiosInstance.post('event/weighing-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar pesagem:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getWeighings(id = null, queryParams = {}) {
  try {
    const url = id ? `event/weighing-get/${id}/` : `event/weighing-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter pesagem:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateWeighing(id, data) {
  try {
    const response = await axiosInstance.put(`event/weighing-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar pesagem:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteWeighing(id) {
  try {
    const response = await axiosInstance.delete(`event/weighing-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar pesagem:', error.response ? error.response.data : error);
    throw error;
  }
}

/** ############### VACINE ############### **/

export async function registerVacine(data) {
  try {
    const response = await axiosInstance.post('event/vacine-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar vacina:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getVacines(id = null, queryParams = {}) {
  try {
    const url = id ? `event/vacine-get/${id}/` : `event/vacine-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter vacina:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateVacine(id, data) {
  try {
    const response = await axiosInstance.put(`event/vacine-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar vacina:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteVacine(id) {
  try {
    const response = await axiosInstance.delete(`event/vacine-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar vacina:', error.response ? error.response.data : error);
    throw error;
  }
}

/** ############### MEDICINE (MEDICAÇÃO) ############### **/

export async function registerMedicine(data) {
  try {
    const response = await axiosInstance.post('event/medicine-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar medicação:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getMedicines(id = null, queryParams = {}) {
  try {
    const url = id ? `event/medicine-get/${id}/` : `event/medicine-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter medicação:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateMedicine(id, data) {
  try {
    const response = await axiosInstance.put(`event/medicine-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar medicação:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteMedicine(id) {
  try {
    const response = await axiosInstance.delete(`event/medicine-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar medicação:', error.response ? error.response.data : error);
    throw error;
  }
}

/** ############### REPRODUCTION ############### **/

export async function registerReproduction(data) {
  try {
    const response = await axiosInstance.post('event/reproduction-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar reprodução:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getReproductions(id = null, queryParams = {}) {
  try {
    const url = id ? `event/reproduction-get/${id}/` : `event/reproduction-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter reprodução:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateReproduction(id, data) {
  try {
    const response = await axiosInstance.put(`event/reproduction-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar reprodução:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteReproduction(id) {
  try {
    const response = await axiosInstance.delete(`event/reproduction-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar reprodução:', error.response ? error.response.data : error);
    throw error;
  }
}

/** ############### SLAUGHTER (ABATE) ############### **/

export async function registerSlaughter(data) {
  try {
    const response = await axiosInstance.post('event/slaughter-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar abate:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getSlaughters(id = null, queryParams = {}) {
  try {
    const url = id ? `event/slaughter-get/${id}/` : `event/slaughter-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter abate:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateSlaughter(id, data) {
  try {
    const response = await axiosInstance.put(`event/slaughter-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar abate:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteSlaughter(id) {
  try {
    const response = await axiosInstance.delete(`event/slaughter-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar abate:', error.response ? error.response.data : error);
    throw error;
  }
}

/** ############### SPECIAL OCCURRENCES ############### **/

export async function registerSpecialOccurrence(data) {
  try {
    const response = await axiosInstance.post('event/special-occurrences-register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar ocorrência especial:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function getSpecialOccurrences(id = null, queryParams = {}) {
  try {
    const url = id ? `event/special-occurrences-get/${id}/` : `event/special-occurrences-filter/`;
    const response = await axiosInstance.get(url, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Erro ao obter ocorrência especial:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function updateSpecialOccurrence(id, data) {
  try {
    const response = await axiosInstance.put(`event/special-occurrences-update/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar ocorrência especial:', error.response ? error.response.data : error);
    throw error;
  }
}

export async function deleteSpecialOccurrence(id) {
  try {
    const response = await axiosInstance.delete(`event/special-occurrences-delete/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar ocorrência especial:', error.response ? error.response.data : error);
    throw error;
  }
}