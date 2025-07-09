import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // ADICIONE ESTE BLOCO:
  server: {
    proxy: {
      // Qualquer requisição para /api será redirecionada para o seu backend local
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})