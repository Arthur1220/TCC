require("@nomicfoundation/hardhat-toolbox");
require("@openzeppelin/hardhat-upgrades");

/** @type import('hardhat/config').HardhatUserConfig */
require("dotenv").config();
module.exports = {
  solidity: "0.8.28",
  networks: {
    local: {
      url: process.env.RPC_URL,        // http://localhost:8545
      chainId: 31337,
      accounts: [process.env.WALLET_PRIVATE]
    }
  },
  paths: {
    artifacts: "./artifacts"
  }
};
