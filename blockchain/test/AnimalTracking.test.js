const { expect } = require("chai");
const { ethers } = require("hardhat");

// Define ZERO_HASH manualmente como 32 bytes de zero
const ZERO_HASH = "0x" + "00".repeat(32);

// Função auxiliar para converter uma string em bytes32 (similar ao antigo formatBytes32String)
function formatBytes32StringCustom(text) {
  const bytes = ethers.toUtf8Bytes(text);
  if (bytes.length > 32) {
    throw new Error("Texto muito longo");
  }
  const padded = new Uint8Array(32);
  padded.set(bytes);
  return ethers.hexlify(padded);
}

describe("AnimalTracking with Access Control", function () {
  let AnimalTracking, animalTracking;
  let deployer, registrar, unauthorized, otherAccount;

  beforeEach(async function () {
    [deployer, registrar, unauthorized, otherAccount] = await ethers.getSigners();
    AnimalTracking = await ethers.getContractFactory("AnimalTracking");
    animalTracking = await AnimalTracking.deploy();
    await animalTracking.waitForDeployment();

    // Autoriza o endereço 'registrar' para registrar eventos
    await animalTracking.addRegistrar(registrar.address);
  });

  describe("Access Control", function () {
    it("Deve permitir que um endereço autorizado registre um evento", async function () {
      const eventId = 1;
      const animalId = 101;
      const eventType = 1; // Ex.: vacinação
      const dataHash = "0x1234abcd";
      const userHash = formatBytes32StringCustom("RegistrarUser");

      // Conecte-se com o 'registrar' autorizado
      await expect(
        animalTracking.connect(registrar).registerEvent(eventId, animalId, eventType, dataHash, userHash)
      )
        .to.emit(animalTracking, "EventRegistered")
        .withArgs(animalId, eventId, eventType, dataHash, registrar.address, userHash);

      const count = await animalTracking.getNumberOfEvents(animalId);
      expect(count).to.equal(1);
    });

    it("Deve reverter se um endereço não autorizado tentar registrar um evento", async function () {
      const eventId = 2;
      const animalId = 202;
      const eventType = 2; // Ex.: medicação
      const dataHash = "0xdeadbeef";
      const userHash = formatBytes32StringCustom("UnauthorizedUser");

      await expect(
        animalTracking.connect(unauthorized).registerEvent(eventId, animalId, eventType, dataHash, userHash)
      ).to.be.revertedWith("Not authorized registrar");
    });
  });

  describe("Registro de Eventos", function () {
    it("Deve registrar um novo evento e emitir o evento EventRegistered", async function () {
      const eventId = 3;
      const animalId = 303;
      const eventType = 1; // Ex.: vacinação
      const dataHash = "0xabcdef01";
      const userHash = formatBytes32StringCustom("TestUser");

      await expect(
        animalTracking.registerEvent(eventId, animalId, eventType, dataHash, userHash)
      )
        .to.emit(animalTracking, "EventRegistered")
        .withArgs(animalId, eventId, eventType, dataHash, deployer.address, userHash);

      const count = await animalTracking.getNumberOfEvents(animalId);
      expect(count).to.equal(1);
    });

    it("Deve recuperar um evento registrado pelo índice", async function () {
      const eventId = 4;
      const animalId = 404;
      const eventType = 2; // Ex.: medicação
      const dataHash = "0xdeadbeef";
      const userHash = formatBytes32StringCustom("UserHashTest");

      await animalTracking.registerEvent(eventId, animalId, eventType, dataHash, userHash);

      const eventData = await animalTracking.getEventByIndex(animalId, 0);

      expect(eventData.eventId).to.equal(eventId);
      expect(eventData.animalId).to.equal(animalId);
      expect(eventData.eventType).to.equal(eventType);
      expect(eventData.dataHash).to.equal(dataHash);
      expect(eventData.registrant).to.equal(deployer.address);
      expect(eventData.userHash).to.equal(userHash);
      expect(eventData.timestamp).to.be.gt(0);
    });
  });

  describe("Casos de Borda", function () {
    it("Deve reverter ao tentar recuperar um evento com índice fora do intervalo", async function () {
      const animalId = 505;
      await expect(
        animalTracking.getEventByIndex(animalId, 0)
      ).to.be.revertedWith("Indice fora do intervalo");
    });

    it("Deve reverter ao tentar registrar um evento com dataHash vazio", async function () {
      const eventId = 5;
      const animalId = 606;
      const eventType = 0; // Ex.: nascimento
      const emptyDataHash = "";
      const userHash = formatBytes32StringCustom("Test");

      await expect(
        animalTracking.registerEvent(eventId, animalId, eventType, emptyDataHash, userHash)
      ).to.be.revertedWith("Data hash nao pode ser vazio");
    });

    it("Deve reverter ao tentar registrar um evento com userHash zero", async function () {
      const eventId = 6;
      const animalId = 707;
      const eventType = 0; // Ex.: nascimento
      const dataHash = "0xabcdef";

      await expect(
        animalTracking.registerEvent(eventId, animalId, eventType, dataHash, ZERO_HASH)
      ).to.be.revertedWith("User hash nao pode ser vazio");
    });
  });

  describe("Registro de Múltiplos Eventos para o Mesmo Animal", function () {
    it("Deve registrar vários eventos para um mesmo animal e manter a ordem de registro", async function () {
      const animalId = 8001;
      
      // Primeiro evento
      const eventId1 = 10;
      const eventType1 = 1; // Vacinação
      const dataHash1 = "0xaaa111";
      const userHash1 = formatBytes32StringCustom("User1");
      
      // Segundo evento
      const eventId2 = 11;
      const eventType2 = 2; // Medicação
      const dataHash2 = "0xbbb222";
      const userHash2 = formatBytes32StringCustom("User2");

      await animalTracking.registerEvent(eventId1, animalId, eventType1, dataHash1, userHash1);
      await animalTracking.registerEvent(eventId2, animalId, eventType2, dataHash2, userHash2);

      const count = await animalTracking.getNumberOfEvents(animalId);
      expect(count).to.equal(2);

      const firstEvent = await animalTracking.getEventByIndex(animalId, 0);
      const secondEvent = await animalTracking.getEventByIndex(animalId, 1);

      expect(firstEvent.eventId).to.equal(eventId1);
      expect(secondEvent.eventId).to.equal(eventId2);
    });
  });

  describe("Contagem de Eventos para Vários Animais", function () {
    it("Deve retornar a contagem correta de eventos para diferentes animais", async function () {
      await animalTracking.registerEvent(20, 2001, 1, "0xhash1", formatBytes32StringCustom("UserA"));
      await animalTracking.registerEvent(21, 2002, 2, "0xhash2", formatBytes32StringCustom("UserB"));
      await animalTracking.registerEvent(22, 2002, 3, "0xhash3", formatBytes32StringCustom("UserC"));
      
      const count2001 = await animalTracking.getNumberOfEvents(2001);
      const count2002 = await animalTracking.getNumberOfEvents(2002);
      const count2003 = await animalTracking.getNumberOfEvents(2003);

      expect(count2001).to.equal(1);
      expect(count2002).to.equal(2);
      expect(count2003).to.equal(0);
    });
  });

  describe("Emissão de Eventos (Logs)", function () {
    it("Deve emitir os eventos na ordem de registro", async function () {
      const animalId = 3001;
      
      // Primeiro evento
      const eventId1 = 30;
      const eventType1 = 1;
      const dataHash1 = "0xorder1";
      const userHash1 = formatBytes32StringCustom("OrderUser1");

      // Segundo evento
      const eventId2 = 31;
      const eventType2 = 2;
      const dataHash2 = "0xorder2";
      const userHash2 = formatBytes32StringCustom("OrderUser2");

      const tx1 = await animalTracking.registerEvent(eventId1, animalId, eventType1, dataHash1, userHash1);
      const receipt1 = await tx1.wait();

      const tx2 = await animalTracking.registerEvent(eventId2, animalId, eventType2, dataHash2, userHash2);
      const receipt2 = await tx2.wait();

      // Processa os logs usando o interface do contrato para fazer o parse
      const parsedLog1 = receipt1.logs
        .map((log) => {
          try {
            return animalTracking.interface.parseLog(log);
          } catch (err) {
            return null;
          }
        })
        .find((parsed) => parsed && parsed.name === "EventRegistered");

      const parsedLog2 = receipt2.logs
        .map((log) => {
          try {
            return animalTracking.interface.parseLog(log);
          } catch (err) {
            return null;
          }
        })
        .find((parsed) => parsed && parsed.name === "EventRegistered");

      expect(parsedLog1.args.eventId).to.equal(eventId1);
      expect(parsedLog2.args.eventId).to.equal(eventId2);
    });
  });
});
