// src/services/propertyService.js

import axiosInstance from './axiosSetup';

/**
 * Registra uma nova propriedade para o usuário autenticado.
 * @param {Object} data - Dados da propriedade.
 * @returns {Promise<Object>} - Dados da propriedade registrada.
 */
export async function registerProperty(data) {
  try {
    const response = await axiosInstance.post('property/register/', data);
    return response.data;
  } catch (error) {
    console.error('Erro ao registrar propriedade:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Obtém as propriedades do usuário autenticado.
 * @returns {Promise<Array>} - Lista de propriedades.
 */
export async function getUserProperties() {
  try {
    // O backend foi configurado para retornar apenas as propriedades do usuário autenticado quando nenhum ID for passado.
    const response = await axiosInstance.get('property/get/');
    return response.data;
  } catch (error) {
    console.error('Erro ao obter propriedades:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Atualiza uma propriedade.
 * @param {number} propertyId - ID da propriedade a ser atualizada.
 * @param {Object} data - Dados para atualização.
 * @returns {Promise<Object>} - Dados da propriedade atualizada.
 */
export async function updateProperty(propertyId, data) {
  try {
    const response = await axiosInstance.put(`property/update/${propertyId}/`, data);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar propriedade:', error.response ? error.response.data : error);
    throw error;
  }
}

/**
 * Deleta uma propriedade.
 * @param {number} propertyId - ID da propriedade a ser deletada.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function deleteProperty(propertyId) {
  try {
    const response = await axiosInstance.delete(`property/delete/${propertyId}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar propriedade:', error.response ? error.response.data : error);
    throw error;
  }
}
