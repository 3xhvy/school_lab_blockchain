# @version ^0.4.3
from ethereum.ercs import IERC20
from ethereum.ercs import IERC20Detailed

implements: IERC20
implements: IERC20Detailed

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Payment:
    buyer: indexed(address)
    value: uint256

name: public(String[32])
symbol: public(String[32])
decimals: public(uint8)

balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
totalSupply: public(uint256)

ethBalances: public(HashMap[address, uint256])

beneficiary: public(address)
minFundingGoal: public(uint256)
maxFundingGoal: public(uint256)
amountRaised: public(uint256)
deadline: public(uint256)
price: public(uint256)
fundingGoalReached: public(bool)
crowdsaleClosed: public(bool)

@deploy
def __init__(_name: String[32], _symbol: String[32], _decimals: uint8, _supply: uint256):
    init_supply: uint256 = _supply * 10 ** convert(_decimals, uint256)
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.balanceOf[msg.sender] = init_supply
    self.totalSupply = init_supply
    log Transfer(sender=empty(address), receiver=msg.sender, value=init_supply)

    self.beneficiary = msg.sender
    self.minFundingGoal = as_wei_value(30, "ether")
    self.maxFundingGoal = as_wei_value(50, "ether")
    self.deadline = block.timestamp + 3600 * 24 * 100 # 100 days
    self.price = as_wei_value(1, "ether") // 100
    self.fundingGoalReached = False
    self.crowdsaleClosed = False

@external
@payable
def __default__():
    assert msg.sender != self.beneficiary
    assert self.crowdsaleClosed == False
    assert self.amountRaised + msg.value <= self.maxFundingGoal
    assert msg.value >= as_wei_value(0.01, "ether")

    # Update ETH balances and amount raised
    self.ethBalances[msg.sender] += msg.value
    self.amountRaised += msg.value

    # Calculate tokens to give (1 ETH = 100 tokens, so token_amount = msg.value // price)
    token_amount: uint256 = msg.value // self.price

    # Transfer tokens from beneficiary to buyer
    assert self.balanceOf[self.beneficiary] >= token_amount
    self.balanceOf[self.beneficiary] -= token_amount
    self.balanceOf[msg.sender] += token_amount

    # Log events
    log Transfer(sender=self.beneficiary, receiver=msg.sender, value=token_amount)
    log Payment(buyer=msg.sender, value=msg.value)

@external
def checkGoalReached():
    assert block.timestamp > self.deadline
    if self.amountRaised >= self.minFundingGoal:
        self.fundingGoalReached = True
    self.crowdsaleClosed = True

@external
def safeWithdrawal():
    assert self.crowdsaleClosed == True

    if self.fundingGoalReached:
        # If funding goal reached, beneficiary can withdraw all ETH
        if msg.sender == self.beneficiary:
            amount: uint256 = self.balance
            send(self.beneficiary, amount)
    else:
        # If funding goal not reached, buyers can get refund
        amount: uint256 = self.ethBalances[msg.sender]
        assert amount > 0
        self.ethBalances[msg.sender] = 0

        # Return tokens back to beneficiary
        token_amount: uint256 = amount // self.price
        self.balanceOf[msg.sender] -= token_amount
        self.balanceOf[self.beneficiary] += token_amount

        # Refund ETH to buyer
        send(msg.sender, amount)
        log Transfer(sender=msg.sender, receiver=self.beneficiary, value=token_amount)

@external
def transfer(_to : address, _value : uint256) -> bool:
    """
    @dev Transfer token for a specified address
    @param _to The address to transfer to.
    @param _value The amount to be transferred.
    """
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(sender=msg.sender, receiver=_to, value=_value)
    return True


@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    """
     @dev Transfer tokens from one address to another.
     @param _from address The address which you want to send tokens from
     @param _to address The address which you want to transfer to
     @param _value uint256 the amount of tokens to be transferred
    """
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender] -= _value
    log Transfer(sender=_from, receiver=_to, value=_value)
    return True


@external
def approve(_spender : address, _value : uint256) -> bool:
    """
    @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
         Beware that changing an allowance with this method brings the risk that someone may use both the old
         and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
         race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
         https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
    @param _spender The address which will spend the funds.
    @param _value The amount of tokens to be spent.
    """
    self.allowance[msg.sender][_spender] = _value
    log Approval(owner=msg.sender, spender=_spender, value=_value)
    return True
