import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
require("dotenv").config();

// Ensure that we have all the environment variables we need.
let mnemonic: string;
if (!process.env.MNEMONIC) {
  throw new Error('Please set your MNEMONIC in the .env file')
} else {
  mnemonic = process.env.MNEMONIC
}

let sepolia_api_http: string;
if (!process.env.SEPOLIA_API_HTTP) {
  throw new Error('Please set SEPOLIA_API_HTTP url in the .env file')
} else {
  sepolia_api_http = process.env.SEPOLIA_API_HTTP;
}

let etherscan_api: string;
if (!process.env.ETHERSCAN_API) {
  throw new Error('Please set your ETHERSCAN_API key in the .env file')
} else {
  etherscan_api = process.env.ETHERSCAN_API
}

const config: HardhatUserConfig = {
  solidity: "0.8.19",

  networks: {
    sepolia: {
      url: sepolia_api_http,
      accounts: { mnemonic: mnemonic }
    },
  },

  etherscan: {
    apiKey: {
      sepolia: etherscan_api
    }
  }
};

export default config;
