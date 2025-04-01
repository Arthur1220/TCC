// test/AnimalTracking.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

// Função auxiliar para converter uma string em bytes32 (similar à antiga formatBytes32String)
function formatBytes32StringCustom(text) {
  const bytes = ethers.toUtf8Bytes(text); // Converte a string em Uint8Array
  if (bytes.length > 32) {
    throw new Error("Texto muito longo");
  }
  // Cria um array de 32 bytes, preenchido com zeros
  const padded = new Uint8Array(32);
  padded.set(bytes);
  return ethers.hexlify(padded);
}

// Definindo ZERO_HASH como 32 bytes de zero:
const ZERO_HASH = "0x" + "00".repeat(32);

describe("AnimalTracking", function () {
  let AnimalTracking, animalTracking;
  let deployer, otherAccount;

  // Antes de cada teste, faça o deploy do contrato
  beforeEach(async function () {
    [deployer, otherAccount] = await ethers.getSigners();
    AnimalTracking = await ethers.getContractFactory("AnimalTracking");
    animalTracking = await AnimalTracking.deploy();
    await animalTracking.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Deve implantar o contrato e estar ativo", async function () {
      // A função isActive() sempre retorna true, pois o contrato não pode ser pausado.
      expect(await animalTracking.isActive()).to.equal(true);
    });
  });

  describe("Registro de Eventos", function () {
    it("Deve registrar um novo evento e emitir o evento EventRegistered", async function () {
      // Parâmetros para o teste:
      // eventId: ID do evento no banco off-chain
      // animalId: ID do animal
      // eventType: número representando o tipo de evento (ex.: 1 para vacinação)
      // dataHash: string representando o hash dos dados (exemplo fictício)
      // userHash: hash (bytes32) representando os dados do usuário
      const eventId = 1;
      const animalId = 101;
      const eventType = 1; // Ex.: vacinação
      const dataHash = "0x1234abcd";
      // Utiliza formatBytes32StringCustom para gerar um bytes32 a partir de uma string
      const userHash = formatBytes32StringCustom("TestUser");

      await expect(
        animalTracking.registerEvent(eventId, animalId, eventType, dataHash, userHash)
      )
        .to.emit(animalTracking, "EventRegistered")
        .withArgs(animalId, eventId, eventType, dataHash, deployer.address, userHash);

      // Verifica se o número de eventos registrados para o animal é igual a 1
      const count = await animalTracking.getNumberOfEvents(animalId);
      expect(count).to.equal(1);
    });

    it("Deve recuperar um evento registrado pelo índice", async function () {
      // Registra um evento para um animal
      const eventId = 2;
      const animalId = 202;
      const eventType = 2; // Ex.: medicação
      const dataHash = "0xdeadbeef";
      const userHash = formatBytes32StringCustom("UserHashTest");

      await animalTracking.registerEvent(eventId, animalId, eventType, dataHash, userHash);

      // Recupera o evento pelo índice 0
      const eventData = await animalTracking.getEventByIndex(animalId, 0);

      // Verifica se os dados recuperados correspondem aos valores enviados
      expect(eventData.eventId).to.equal(eventId);
      expect(eventData.animalId).to.equal(animalId);
      expect(eventData.eventType).to.equal(eventType);
      expect(eventData.dataHash).to.equal(dataHash);
      expect(eventData.registrant).to.equal(deployer.address);
      expect(eventData.userHash).to.equal(userHash);
      expect(eventData.timestamp).to.be.gt(0); // Deve ser maior que zero
    });
  });

  describe("Casos de Borda", function () {
    it("Deve reverter ao tentar recuperar um evento com índice fora do intervalo", async function () {
      const animalId = 303;
      // Sem evento registrado para animal 303, tentar acessar o índice 0 deve reverter.
      await expect(
        animalTracking.getEventByIndex(animalId, 0)
      ).to.be.revertedWith("Indice fora do intervalo");
    });

    it("Deve reverter ao tentar registrar um evento com dataHash vazio", async function () {
      const eventId = 3;
      const animalId = 404;
      const eventType = 0; // Ex.: nascimento
      const emptyDataHash = "";
      const userHash = formatBytes32StringCustom("Test");

      await expect(
        animalTracking.registerEvent(eventId, animalId, eventType, emptyDataHash, userHash)
      ).to.be.revertedWith("Data hash nao pode ser vazio");
    });

    it("Deve reverter ao tentar registrar um evento com userHash zero", async function () {
      const eventId = 4;
      const animalId = 505;
      const eventType = 0; // Ex.: nascimento
      const dataHash = "0xabcdef";
      await expect(
        animalTracking.registerEvent(eventId, animalId, eventType, dataHash, ZERO_HASH)
      ).to.be.revertedWith("User hash nao pode ser vazio");
    });
  });
});