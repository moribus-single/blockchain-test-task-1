import { ethers, run } from "hardhat";
import config from "../config";

function sleep(time: number) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

async function main() {
  // get params from the config.ts
  const name = config.token.name;
  const symbol = config.token.symbol;
  const provider = config.token.provider;
  const reward = config.reward;

  // deploy token
  const factory = await ethers.getContractFactory("LongevityToken");
  const token = await factory.deploy(name, symbol, provider);
  await token.waitForDeployment();

  try {
    // wait untill deploy fact will be propagated to the backend
    await sleep(30 * 1000);

    await run("verify:verify", {
        address: await token.getAddress(),
        constructorArguments: [
          name, 
          symbol, 
          provider
        ],
        contract: "contracts/LongevityToken.sol:LongevityToken",
    });
    console.log("verify success");
  } catch (e: any) {
    console.log(e);
  }

  const tokenAddr = await token.getAddress();

  // set the reward amount
  const rewardAmount = ethers.parseEther(reward.toString());
  await token.setReward(rewardAmount);

  // mint some tokens to the token contract
  await token.mint(tokenAddr, ethers.parseEther("100000"));

  console.log("Token address: ", tokenAddr);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
