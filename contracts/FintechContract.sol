// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SmartPayment {

    address public owner;
    
    // Event to log payments
    event PaymentReceived(address indexed from, uint256 amount);
    
    // Event to log withdrawals
    event Withdrawal(address indexed to, uint256 amount);

    // Constructor to set the owner during contract deployment
    constructor() {
        owner = msg.sender;
    }

    // Modifier to restrict actions to only the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner");
        _;
    }

    // Payable function that allows anyone to send Ether to the contract
    function pay() external payable {
        require(msg.value > 0, "You need to send some Ether");
        emit PaymentReceived(msg.sender, msg.value);
    }

    // Withdraw function that allows the owner to withdraw funds
    function withdraw(uint256 amount) external onlyOwner {
        require(address(this).balance >= amount, "Insufficient balance");
        payable(owner).transfer(amount);
        emit Withdrawal(owner, amount);
    }

    // Get the balance of the contract
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
