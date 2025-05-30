import axiosInstance from './axiosSetup';

  /**
   * Realiza o cadastro de um novo usuário.
   * @param {Object} data - Dados do usuário a ser cadastrado.
   * @returns {Promise<Object>} - Resposta da API.
   */
  export async function registerUser(data) {
    try {
      const response = await axiosInstance.post('user/register/', data);
      return response.data;
    } catch (error) {
      console.error("Erro ao registrar usuário:", error);
      throw error.response ? error.response.data : error;
    }
  }

  /**
   * Obtém os dados do perfil do usuário autenticado.
   * @returns {Promise<Object>} - Dados do perfil.
   */
  export async function getUserProfile() {
    try {
      const response = await axiosInstance.get('user/profile/');
      return response.data;
    } catch (error) {
      console.error("Erro ao obter perfil:", error);
      throw error.response ? error.response.data : error;
    }
  }

  /**
   * Atualiza os dados do perfil do usuário autenticado.
   * @param {Object} data - Dados para atualização.
   * @returns {Promise<Object>} - Resposta da API.
   */
  export async function updateUserProfile(data) {
    try {
      const response = await axiosInstance.put('user/update/', data);
      return response.data;
    } catch (error) {
      console.error("Erro ao atualizar perfil:", error);
      throw error.response ? error.response.data : error;
    }
  }

/**
 * Deleta a conta do usuário autenticado.
 * @returns {Promise<Object>} - Resposta da API.
 */
export async function deleteUserAccount() {
  try {
    const response = await axiosInstance.delete('user/delete/');
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar conta:', error);
    throw error;
  }
}

/**
 * Obtém a lista de todos os usuários.
 * @returns {Promise<Array>} - Lista de usuários.
 */
export async function getAllUsers() { // Função adicionada
  try {
    const response = await axiosInstance.get('user/all_users/');
    return response.data;
  } catch (error) {
    console.error("Erro ao obter todos os usuários:", error);
    throw error.response ? error.response.data : error;
  }
}

/**
 * Busca um usuário pelo seu user_hash.
 * @param {string} hash - O user_hash a ser buscado.
 * @returns {Promise<Object>} - Dados do usuário encontrado (ex: id, username, user_hash).
 */
export async function getUserByHash(hash) {
  if (!hash || typeof hash !== 'string' || hash.trim() === '') {
    // Validação básica no lado do cliente para evitar chamadas desnecessárias
    const error = new Error("O hash do usuário não pode ser vazio.");
    // @ts-ignore
    error.isClientError = true; // Adiciona uma flag para identificar erro do cliente
    throw error;
  }
  try {
    // A URL deve corresponder à definida no Django user/urls.py, incluindo o prefixo do app
    // Ex: se o prefixo do app user no urls.py principal for 'user/', então 'user/get-by-hash/'
    const response = await axiosInstance.get('user/get-by-hash/', { 
      params: { hash: hash.trim() } 
    });
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar usuário pelo hash "${hash}":`, error.response ? error.response.data : error);
    // Relança o erro para ser tratado pelo componente chamador
    // Se o erro for 404, error.response.data pode conter { detail: "Usuário não encontrado..." }
    throw error.response ? error.response.data : error;
  }
}