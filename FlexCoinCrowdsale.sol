pragma solidity ^0.5.5;

import "./FlexCoin.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";


// Have the FlexCoinCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract FlexCoinCrowdsale is Crowdsale, MintedCrowdsale { // UPDATE THE CONTRACT SIGNATURE TO ADD INHERITANCE
    
    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint rate, 
        address payable wallet, // sale beneficiary
        FlexCoin token // the token itself that the FlexCoinCrowdsale will work with 
    ) public Crowdsale(rate, wallet, token) {
        // constructor can stay empty
    }
}

contract FlexCoinCrowdsaleDeployer {
    address public flex_token_address; 
    address public flex_crowdsale_address;
 
    constructor(
       string memory name, 
       string memory symbol, 
       address payable wallet
    ) public {
        // Create a new instance of the FlexCoin contract.
        FlexCoin token = new FlexCoin(name, symbol, 0);
        
        // Assign the token contract’s address to the `flex_token_address` variable.
        flex_token_address = address(token);

        // Create a new instance of the `FlexCoinCrowdsale` contract
        FlexCoinCrowdsale flex_crowdsale = new FlexCoinCrowdsale(1, wallet, token);
            
        // Assign the `FlexCoinCrowdsale` contract’s address to the `flex_crowdsale_address` variable.
        flex_crowdsale_address = address(flex_crowdsale);

        // Set the `FlexCoinCrowdsale` contract as a minter
        token.addMinter(flex_crowdsale_address);
        
        // Have the `FlexCoinCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}
