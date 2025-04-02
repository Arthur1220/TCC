// services/authService.js
import axiosInstance from './axiosSetup';

/**
 * Realiza o login do usuário.
 * O backend define os tokens JWT em cookies HTTP‑only.
 * @param {string} username - Nome de usuário.
 * @param {string} password - Senha do usuário.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function login(username, password) {
  try {
    const response = await axiosInstance.post('user/login/', { username, password });
    // Os cookies são definidos automaticamente pelo navegador, pois usamos withCredentials.
    return response.data;
  } catch (error) {
    console.error('Erro ao fazer login:', error);
    throw error;
  }
}

/**
 * Realiza a renovação do token de acesso utilizando o endpoint de refresh.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function refreshToken() {
  try {
    const response = await axiosInstance.post('user/refresh/', {});
    return response.data;
  } catch (error) {
    console.error('Erro ao renovar token:', error);
    throw error;
  }
}

/**
 * Realiza o logout do usuário.
 * Chama o endpoint de logout e remove os cookies.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function logout() {
  try {
    const response = await axiosInstance.post('user/logout/');
    return response.data;
  } catch (error) {
    console.error('Erro ao fazer logout:', error);
    throw error;
  }
}