//contrat de paiement
pragma solidity ^0.8.0;

contract FintechContract {
    address public owner;//a solidity variable type reffers to Ethereum addresses

    event PaymentReceived(address from, uint256 amount);//event & emit //uint=> no negative integer value
    event Withdrawal(address to, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    function pay() public payable {
        emit PaymentReceived(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) public {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(amount);
        emit Withdrawal(owner, amount);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
