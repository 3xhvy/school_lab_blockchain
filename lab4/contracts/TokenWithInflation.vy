# @version ^0.4.3

balances: public(HashMap[address, uint256])
owner: public(address)

@deploy
def __init__():
    self.owner = msg.sender
    self.balances[msg.sender] = 1000
@external
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.balances[msg.sender] >= _amount
    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount
    return True

@external
def mint(_new_supply: uint256):
    assert msg.sender == self.owner
    self.balances[self.owner] = _new_supply



