const { expect } = require("chai");
const { ethers, upgrades } = require("hardhat");

describe("AnimalTracking (Upgradeable + Pausable + UUPS)", function () {
  let AnimalTracking, animalTracking;
  let owner, registrar, unauthorized, another;

  // ZERO_HASH em Ethers v6
  const ZERO_HASH = ethers.ZeroHash;

  // formata string para bytes32 em Ethers v6
  function formatBytes32(text) {
    return ethers.encodeBytes32String(text);
  }

  beforeEach(async () => {
    [owner, registrar, unauthorized, another] = await ethers.getSigners();
    AnimalTracking = await ethers.getContractFactory("AnimalTracking");
    // deploy do proxy
    animalTracking = await upgrades.deployProxy(
      AnimalTracking,
      [], 
      { initializer: "initialize" }
    );
    // aguarda deploy
    await animalTracking.waitForDeployment();
  });

  describe("Deployment & Inicialização", () => {
    it("Deployer é owner e registrador autorizado", async () => {
      // obtém endereço do proxy
      const proxyAddr = await animalTracking.getAddress();
      expect(await animalTracking.owner()).to.equal(owner.address);

      // owner deve conseguir registrar um evento
      await expect(
        animalTracking.registerEvent(1, 1, 1, "0x01", formatBytes32("U"))
      )
        .to.emit(animalTracking, "EventRegistered")
        .withArgs(1, 1, 1, "0x01", owner.address, formatBytes32("U"));
    });

    it("isActive() inicia como true", async () => {
      expect(await animalTracking.isActive()).to.equal(true);
    });
  });

  describe("Controle de Pausa", () => {
    it("Somente owner pode pause/unpause", async () => {
      await expect(
        animalTracking.connect(unauthorized).pause()
      ).to.be.revertedWith("Ownable: caller is not the owner");

      await expect(animalTracking.pause())
        .to.emit(animalTracking, "Paused")
        .withArgs(owner.address);

      expect(await animalTracking.isActive()).to.equal(false);

      await expect(
        animalTracking.registerEvent(2, 2, 1, "0x02", formatBytes32("X"))
      ).to.be.revertedWith("Pausable: paused");

      await expect(animalTracking.unpause())
        .to.emit(animalTracking, "Unpaused")
        .withArgs(owner.address);

      expect(await animalTracking.isActive()).to.equal(true);
    });
  });

  describe("Registradores (add/remove)", () => {
    it("Owner pode adicionar e remover registrador", async () => {
      // antes, registrar não está autorizado
      await expect(
        animalTracking.connect(registrar).registerEvent(3, 3, 1, "0x03", formatBytes32("A"))
      ).to.be.revertedWithCustomError(animalTracking, "NotAuthorizedRegistrar");

      // adiciona e testa
      await animalTracking.addRegistrar(registrar.address);
      await expect(
        animalTracking.connect(registrar).registerEvent(3, 3, 1, "0x03", formatBytes32("A"))
      ).to.emit(animalTracking, "EventRegistered");

      // remove e testa
      await animalTracking.removeRegistrar(registrar.address);
      await expect(
        animalTracking.connect(registrar).registerEvent(4, 3, 1, "0x04", formatBytes32("B"))
      ).to.be.revertedWithCustomError(animalTracking, "NotAuthorizedRegistrar");
    });
  });

  describe("Registro de Eventos", () => {
    beforeEach(async () => {
      // owner já está autorizado
      await animalTracking.addRegistrar(registrar.address);
    });

    it("Deve registrar um evento e emitir EventRegistered", async () => {
      await expect(
        animalTracking.connect(registrar)
          .registerEvent(10, 100, 2, "0xAA", formatBytes32("R"))
      )
        .to.emit(animalTracking, "EventRegistered")
        .withArgs(100, 10, 2, "0xAA", registrar.address, formatBytes32("R"));
      expect(await animalTracking.getNumberOfEvents(100)).to.equal(1);
    });

    it("Reverte se dataHash vazio", async () => {
      await expect(
        animalTracking.registerEvent(11, 101, 1, "", formatBytes32("U"))
      ).to.be.revertedWithCustomError(animalTracking, "DataHashEmpty");
    });

    it("Reverte se userHash zero", async () => {
      await expect(
        animalTracking.registerEvent(12, 102, 1, "0xBB", ZERO_HASH)
      ).to.be.revertedWithCustomError(animalTracking, "UserHashEmpty");
    });

    it("Mantém ordem de registro e lê corretamente via getEventByIndex", async () => {
      await animalTracking.registerEvent(20, 200, 1, "0xCC", formatBytes32("U1"));
      await animalTracking.registerEvent(21, 200, 2, "0xDD", formatBytes32("U2"));

      expect(await animalTracking.getNumberOfEvents(200)).to.equal(2);

      const ev0 = await animalTracking.getEventByIndex(200, 0);
      expect(ev0.eventId).to.equal(20);
      const ev1 = await animalTracking.getEventByIndex(200, 1);
      expect(ev1.eventId).to.equal(21);
    });

    it("Reverte getEventByIndex fora do intervalo", async () => {
      await expect(
        animalTracking.getEventByIndex(300, 0)
      ).to.be.revertedWithCustomError(animalTracking, "IndexOutOfRange");
    });

    it("getEventsByAnimal retorna array correto", async () => {
      await animalTracking.registerEvent(30, 300, 1, "0xEE", formatBytes32("X"));
      const list = await animalTracking.getEventsByAnimal(300);
      expect(list.length).to.equal(1);
      expect(list[0].eventId).to.equal(30);
    });
  });

  describe("Upgradeability (UUPS)", () => {
    it("Owner consegue upgrade para a mesma implementação", async () => {
      const proxyAddr = await animalTracking.getAddress();
      await expect(
        upgrades.upgradeProxy(proxyAddr, AnimalTracking)
      ).to.not.be.reverted;
    });
  
    it("Não-owner não pode upgrade", async () => {
      const proxyAddr = await animalTracking.getAddress();
      // Recupera o factory e conecta ao signer não-dono
      const ATFactory = await ethers.getContractFactory("AnimalTracking");
      const ATFactoryUnauthorized = ATFactory.connect(unauthorized);
  
      // Quando tentarmos o upgrade com esse factory, deve reverter
      await expect(
        upgrades.upgradeProxy(proxyAddr, ATFactoryUnauthorized)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });  
});
