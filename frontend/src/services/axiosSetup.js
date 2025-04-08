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
        refreshToken();
        // Reenvia a requisição original; o navegador deve enviar os novos cookies automaticamente
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