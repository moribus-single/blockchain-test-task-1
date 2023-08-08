# Longevity token

## Description
Longevity token is **ERC20** token written with **Solidity** language and **OpenZeppelin** smart contracts library. <br>
You can find the contract in `contracts` folder. <br> <br>

There is a **provider role** to ensure appropriate access control for some functions:
-  `setReward(uint256 newReward)` - set reward basic value.
-  `grantReward(address user)` - grant reward to the user.
-  `changeProvider(address newProvider)` - change provder address.
-  `mint(address user, uint256 amount)` - mint some tokens to the address.

## Deploy
1. Set env variables in `.env` file according example in `.env.example`.
2. Compile contract <br>
`
npx hardhat compile
`
3. Check that deploy parameters set in `config.ts` file are correct.
4. Run deploy script (add `--network` flag to deploy in certain network, you should configure it first in `hardhat.config.ts`) <br>
`
npx hardhat run scripts/deploy.ts
` <br> <br>
Deploy script will deploy LONG token, set reward configured in `config.ts` and mint some tokens to the contract for rewards.

## Usage 
1. Set reward value.
2. Mint enough tokens for rewards.
3. Grant rewards to the users.
4. Granted users can claim tokens.


## Additional considerations
It is necessary to add function for minting tokens. Only provider can mint tokens. <br> <br>
For convenient rewards granting there is a `grantRewards(address[] users)` function. <br>
Provide array of addresses to grant rewards to. For each address `grantReward(address)` will be called.

## Example in Sepolia testnet
Address: 0xE865135FF79E45b4F5Da1b0581f54D1c530f57F5