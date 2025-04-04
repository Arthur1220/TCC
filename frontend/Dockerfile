# frontend/Dockerfile

# Etapa 1: Construção da aplicação com Node.js
FROM node:18-alpine AS build

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependências
COPY package.json package-lock.json ./

# Instalar dependências
RUN npm install

# Copiar o restante do código fonte
COPY . .

# (Opcional) Executar build para verificar se tudo está funcionando
# RUN npm run build

# Etapa 2: Ambiente de Desenvolvimento
FROM node:18-alpine

# Definir o diretório de trabalho
WORKDIR /app

# Copiar apenas as dependências instaladas da etapa de build
COPY --from=build /app/node_modules ./node_modules

# Copiar o restante do código fonte
COPY . .

# Expor a porta utilizada pelo Vite (por padrão, 5173)
EXPOSE 5173

# Definir variáveis de ambiente (se necessário)
ENV NODE_ENV=development

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]