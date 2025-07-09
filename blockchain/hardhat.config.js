require("@nomicfoundation/hardhat-toolbox");
require("@openzeppelin/hardhat-upgrades");

/** @type import('hardhat/config').HardhatUserConfig */
require("dotenv").config();
module.exports = {
  solidity: "0.8.28",
  networks: {
    local: {
      url: 'http://127.0.0.1:8545',        // http://localhost:8545
      chainId: 31337,
      accounts: [process.env.WALLET_PRIVATE]
    }
  },
  paths: {
    artifacts: "./artifacts"
  }
};
