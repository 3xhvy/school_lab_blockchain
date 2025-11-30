# @version ^0.4.3

balances: public(HashMap[address, uint256])

@deploy
def __init__():
    self.balances[msg.sender] = 1000
@external
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.balances[msg.sender] >= _amount
    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount
    return True


