#
docker-compose down --rmi all --volumes --remove-orphans

# 
docker-compose up --build -d

docker compose down -v --rmi all --remove-orphans
docker compose build --no-cache
docker compose up -d

# Blockchain
cd blockchain

npm install

npx hardhat compile

npx hardhat run scripts/deploy.js --network localhost