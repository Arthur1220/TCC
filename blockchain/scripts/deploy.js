const { ethers, upgrades } = require("hardhat");

async function main() {
  console.log("Deploying upgradeable AnimalTracking...");

  // 1) Pegamos o factory
  const AnimalTracking = await ethers.getContractFactory("AnimalTracking");

  // 2) Deploy do proxy (chama initialize())
  const instance = await upgrades.deployProxy(
    AnimalTracking,
    [],                 // sem args no initialize()
    { initializer: "initialize" }
  );

  // 3) Aguarda o contrato estar de fato implantado
  await instance.waitForDeployment();

  // 4) Obtém o endereço já resolvido
  const proxyAddress = await instance.getAddress();

  console.log("DEPLOYED_ADDRESS=", proxyAddress);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Deployment failed:", error);
    process.exit(1);
  });
