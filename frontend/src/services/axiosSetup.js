// services/axiosSetup.js
import axios from 'axios';
import { logout, refreshToken } from './authService';

const baseURL = 'http://localhost:8000/';

const axiosInstance = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Garante que cookies sejam enviados com as requisições
});

// Request interceptor (não precisamos adicionar Authorization manualmente, pois os cookies são enviados automaticamente)
axiosInstance.interceptors.request.use(
    (config) => {
      // Se desejar, você pode adicionar alguma lógica extra aqui, mas
      // quando se utiliza cookies HTTP‑only, não há acesso ao token via JS.
      return config;
    },
    (error) => Promise.reject(error)
  );

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // Se a resposta for 401 (não autorizado) e a requisição ainda não foi reexecutada...
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        // Chama o endpoint de refresh.
        // Como o refresh token está em um cookie HTTP‑only, não precisamos enviá-lo no corpo.
        refreshToken();
        // Se a renovação for bem-sucedida, o backend já atualizou o cookie 'access'.
        // Agora, refazemos a requisição original. O navegador enviará o novo cookie automaticamente.
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error('Erro ao renovar token:', refreshError);
        // Se a renovação falhar, efetuamos logout.
        logout();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;