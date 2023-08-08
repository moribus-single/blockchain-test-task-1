// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LongevityToken is ERC20 {
    /// @dev The reward amount is invalid.
    error InvalidReward();

    /// @dev The message sender is invalid.
    error InvalidSender();


    /// @dev Emitted when reward amount is changed to the `newReward`.
    event SetReward(uint256 newReward);

    /// @dev Emitted when reward granted to the `user` address.
    event GrantReward(address user);

    /// @dev Emitted when old provider address is changed to the `newProvider` address.
    event ChangeProvider(address newProvider);

    /// @dev Emitted when `amount` amount of tokens minted to the `user` address with using mint function.
    event Mint(address user, uint256 amount);


    /// @dev Reward amount
    uint256 public reward;

    /// @dev Provider address
    address public provider;

    /// @dev User rewards granted by owner.
    mapping(address => uint256) public userRewards;


    /// @dev Modifier to check if a sender is provider
    modifier onlyProvider() {
        if (msg.sender != provider) {
            revert InvalidSender();
        }

        _;
    }

    constructor(
        string memory name, 
        string memory symbol,
        address sender
    ) ERC20(name, symbol) {
        provider = sender;
    }

    /**
     * @dev Claim granted rewards
     * @param amount Amount to claim
     */
    function claimReward(uint256 amount) external {
        if (amount > userRewards[msg.sender]) {
            revert InvalidReward();
        }

        userRewards[msg.sender] -= amount;
        _transfer(address(this), msg.sender, amount);
        
        emit GrantReward(msg.sender);
    }

    /**
     * @dev Set basic reward value
     * @param newReward Reward amount
     */
    function setReward(uint256 newReward) external onlyProvider {
        reward = newReward;
        emit SetReward(newReward);
    }

    /**
     * @dev Grant reward amount to the user
     * @param user Address of the user
     */
    function grantReward(address user) public onlyProvider {
        userRewards[user] += reward;
        emit GrantReward(user);
    }

    /**
     * @dev Grant rewards to the users
     * @param users Array of adresses
     */
    function grantRewards(address[] memory users) external onlyProvider {
        for (uint256 i; i < users.length; i++) {
            grantReward(users[i]);
        }
    }

    /**
     * @dev Set new provider address
     * @param newProvider Address of the new provider
     */
    function changeProvider(address newProvider) external onlyProvider {
        provider = newProvider;
        emit ChangeProvider(newProvider);
    }

    /**
     * @dev Mint tokens to the address
     * @param user Address to mint to
     * @param amount Amount to mint to the address
     */
    function mint(address user, uint256 amount) external onlyProvider {
        _mint(user, amount);
        emit Mint(user, amount);
    }
}
