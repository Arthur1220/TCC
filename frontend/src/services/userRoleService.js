// src/services/userRoleService.js
import axiosInstance from './axiosSetup'; // Certifique-se que o path está correto

const BASE_URL_USER = '/user'; // Base URL para as APIs do seu app 'User'

/**
 * Obtém todas as roles disponíveis.
 * @returns {Promise<Array>} - Lista de roles.
 */
export async function getRoles() {
  try {
    const response = await axiosInstance.get(`${BASE_URL_USER}/roles/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar roles:', error.response?.data || error.message);
    throw error;
  }
}

/**
 * Atribui uma role a um usuário.
 * @param {number} userId - ID do usuário.
 * @param {number} roleId - ID da role a ser atribuída.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function assignUserRole(userId, roleId) {
  try {
    const response = await axiosInstance.post(`${BASE_URL_USER}/user_roles/assign/`, {
      user_id: userId,
      role_id: roleId
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao atribuir role:', error.response?.data || error.message);
    throw error;
  }
}

/**
 * Remove uma role de um usuário.
 * @param {number} userId - ID do usuário.
 * @param {number} roleId - ID da role a ser removida.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function removeUserRole(userId, roleId) {
  try {
    const response = await axiosInstance.delete(`${BASE_URL_USER}/user_roles/remove/${userId}/${roleId}/`);
    return response.data;
  } catch (error) {
    console.error('Erro ao remover role:', error.response?.data || error.message);
    throw error;
  }
}