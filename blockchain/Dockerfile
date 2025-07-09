# Stage 1: build
FROM node:18-alpine AS builder
RUN apk add --no-cache curl
WORKDIR /app
COPY .env .env
COPY blockchain/package*.json ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY blockchain/ ./
RUN npx hardhat compile

# Stage 2: runtime
FROM node:18-alpine
WORKDIR /app

# Copiar artefatos compilados
COPY --from=builder /app /app

# Diretório de dados (persistência)
VOLUME ["/data"]

# Expor porta JSON-RPC (Hardhat Node)
EXPOSE 8545

# ENTRYPOINT só inicia o nó persistente
#ENTRYPOINT ["sh","-c","npx hardhat node --db $HARDHAT_DB_PATH"]
ENTRYPOINT ["sh","-c","npx hardhat node --hostname 0.0.0.0"]
