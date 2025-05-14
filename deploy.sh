#!/usr/bin/env bash
set -e

echo ":: build blockchain image"
docker-compose build blockchain

echo ":: up blockchain container"
docker-compose up -d blockchain

echo ":: waiting for Hardhat RPC to be ready at http://localhost:8545"
# espera até o host conseguir falar com o container via porta exposta
until curl -sSf http://localhost:8545 >/dev/null 2>&1; do
  printf "."
  sleep 1
done
echo " Hardhat RPC is up!"

echo ":: running deploy script inside blockchain container"
# captura stdout+stderr
DEPLOY_LOG=$(docker-compose exec -T blockchain sh -c "npx hardhat run scripts/deploy.js --network \$NETWORK" 2>&1) || {
  echo "❌ Deploy failed:"
  echo "$DEPLOY_LOG"
  exit 1
}
echo "$DEPLOY_LOG"

CONTRACT_ADDRESS=$(printf '%s\n' "$DEPLOY_LOG" | grep DEPLOYED_ADDRESS | head -n1 | cut -d'=' -f2)
if [ -z "$CONTRACT_ADDRESS" ]; then
  echo "❌ Não foi possível extrair CONTRACT_ADDRESS do deploy."
  exit 1
fi
echo ":: contract deployed at $CONTRACT_ADDRESS"

# Atualiza o .env
ENV_FILE="./.env"
VAR_NAME="CONTRACT_ADDRESS"
if grep -q "^$VAR_NAME=" "$ENV_FILE"; then
  sed -i.bak -E "s|^$VAR_NAME=.*|$VAR_NAME=$CONTRACT_ADDRESS|" "$ENV_FILE"
else
  echo "$VAR_NAME=$CONTRACT_ADDRESS" >> "$ENV_FILE"
fi
echo ":: updated $ENV_FILE with $VAR_NAME=$CONTRACT_ADDRESS"

echo ":: up backend & frontend (sem recriar blockchain)"
docker-compose up -d --no-recreate backend frontend

echo "✅ Tudo pronto!"
