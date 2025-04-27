# frontend/Dockerfile  ── DEV ONLY
FROM node:18-alpine

# 1. diretório de trabalho
WORKDIR /app

# 2. copiar arquivos de dependência e instalar TUDO (inclui vite)
COPY package.json package-lock.json ./
RUN npm install            # ou: npm ci

# 3. copiar o resto do código
COPY . .

# 4. expor a porta padrão do Vite
EXPOSE 5173

# 5. garantir modo dev
ENV NODE_ENV=development

# 6. comando default
CMD ["npm", "run", "dev", "--", "--host"]
