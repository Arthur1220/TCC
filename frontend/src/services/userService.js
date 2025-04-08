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
