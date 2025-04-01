// Hardhat Runtime Environment (HRE)
const hre = require("hardhat");
const { ethers } = hre;

async function main() {
  console.log("Deploy script started...");

  // 1) Faz deploy do contrato AnimalTracking
  const AnimalTracking = await ethers.getContractFactory("AnimalTracking");
  const contract = await AnimalTracking.deploy();   // Deploy
  await contract.waitForDeployment();               // Espera ser minerado

  const address = await contract.getAddress();
  console.log("AnimalTracking deployed to:", address);

  // 2) Verifica se estamos numa rede suportada
  const chainId = hre.network.config.chainId; 
  console.log(`Current network: ${hre.network.name} (chainId: ${chainId})`);

  // Se for localhost/hardhat, chainId normalmente é 31337 ou 1337
  if (chainId === 31337 || hre.network.name === "localhost" || hre.network.name === "hardhat") {
    console.log("Skipping Etherscan verification on local network");
    return;
  }

  // 3) Caso seja uma rede pública/testnet suportada, tentamos verificar:
  try {
    console.log("Waiting some seconds before verification...");
    await sleep(10000); // Espera 10 segundos, tempo para o contrato propagar no block explorer

    console.log("Verifying on Etherscan...");
    await hre.run("verify:verify", {
      address: address,
      constructorArguments: [],
    });
    console.log("Contract verified successfully!");
  } catch (err) {
    console.warn("Verification attempt failed:", err);
  }
}

// Simples função de espera
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Execução
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error in deployment script:", error);
    process.exit(1);
  });
