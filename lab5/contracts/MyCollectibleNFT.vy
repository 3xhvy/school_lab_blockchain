# @version ^0.4.3

# Events
event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _tokenId: indexed(uint256)

event Approval:
    _owner: indexed(address)
    _approved: indexed(address)
    _tokenId: indexed(uint256)

event ApprovalForAll:
    _owner: indexed(address)
    _operator: indexed(address)
    _approved: bool

event Minted:
    _to: indexed(address)
    _tokenId: indexed(uint256)
    _name: String[100]

# State variables
name: public(String[100])
symbol: public(String[100])
baseURI: public(String[200])

# Token ownership and balances
_ownerOf: HashMap[uint256, address]
balanceOf: public(HashMap[address, uint256])
totalSupply: public(uint256)

# Approvals
getApproved: public(HashMap[uint256, address])
isApprovedForAll: public(HashMap[address, HashMap[address, bool]])

# Metadata storage for each character
characterName: public(HashMap[uint256, String[100]])
characterDescription: public(HashMap[uint256, String[500]])
characterImageURI: public(HashMap[uint256, String[200]])

# Access control
minter: public(address)


@deploy
def __init__(_name: String[100], _symbol: String[100], _baseURI: String[200]):
    """
    @notice Initialize the NFT contract
    @param _name Name of the NFT collection
    @param _symbol Symbol of the NFT collection
    @param _baseURI Base URI for token metadata
    """
    self.name = _name
    self.symbol = _symbol
    self.baseURI = _baseURI
    self.minter = msg.sender
    self.totalSupply = 0


@view
@external
def ownerOf(_tokenId: uint256) -> address:
    """
    @notice Get the owner of a token
    @param _tokenId The token ID
    @return The owner address
    """
    owner: address = self._ownerOf[_tokenId]
    assert owner != empty(address), "Token does not exist"
    return owner


@view
@external
def supportsInterface(_interfaceId: bytes4) -> bool:
    """
    @notice Check if contract supports an interface (ERC-165)
    @param _interfaceId Interface identifier
    @return True if interface is supported
    """
    return _interfaceId == 0x01ffc9a7 or _interfaceId == 0x80ac58cd or _interfaceId == 0x5b5e139f


@view
@external
def tokenURI(_tokenId: uint256) -> String[850]:
    """
    @notice Returns the metadata URI for a given token ID as JSON metadata string
    @param _tokenId The token ID to query
    @return JSON metadata string
    """
    assert self._ownerOf[_tokenId] != empty(address), "Token does not exist"

    # Build JSON metadata
    name_str: String[100] = self.characterName[_tokenId]
    desc_str: String[500] = self.characterDescription[_tokenId]
    image_str: String[200] = self.characterImageURI[_tokenId]

    # Construct JSON string
    # Format: {"name": "...", "description": "...", "image": "..."}
    json: String[850] = concat(
        '{"name":"',
        name_str,
        '","description":"',
        desc_str,
        '","image":"',
        image_str,
        '"}'
    )
    return json


@external
def mint(_to: address, _tokenId: uint256, _name: String[100], _description: String[500], _imageURI: String[200]):
    """
    @notice Mint a new NFT character (only minter can mint)
    @param _to Address to receive the NFT
    @param _tokenId Unique token ID for the character
    @param _name Name of the character
    @param _description Description of the character
    @param _imageURI Image URL for the character
    """
    assert msg.sender == self.minter, "Only minter can mint"
    assert self._ownerOf[_tokenId] == empty(address), "Token already exists"
    assert _to != empty(address), "Cannot mint to zero address"

    # Set ownership
    self._ownerOf[_tokenId] = _to
    self.balanceOf[_to] += 1
    self.totalSupply += 1

    # Store character metadata
    self.characterName[_tokenId] = _name
    self.characterDescription[_tokenId] = _description
    self.characterImageURI[_tokenId] = _imageURI

    # Emit events
    log Transfer(_from=empty(address), _to=_to, _tokenId=_tokenId)
    log Minted(_to=_to, _tokenId=_tokenId, _name=_name)


@external
def burn(_tokenId: uint256):
    """
    @notice Burn (destroy) an NFT (only owner can burn)
    @param _tokenId Token ID to burn
    """
    owner: address = self._ownerOf[_tokenId]
    assert owner != empty(address), "Token does not exist"
    assert owner == msg.sender or self.getApproved[_tokenId] == msg.sender or self.isApprovedForAll[owner][msg.sender], "Not authorized"

    # Clear approvals
    if self.getApproved[_tokenId] != empty(address):
        self.getApproved[_tokenId] = empty(address)

    # Update balances
    self.balanceOf[owner] -= 1
    self._ownerOf[_tokenId] = empty(address)
    self.totalSupply -= 1

    # Clear metadata
    self.characterName[_tokenId] = ""
    self.characterDescription[_tokenId] = ""
    self.characterImageURI[_tokenId] = ""

    # Emit Transfer event to zero address (ERC-721 standard for burn)
    log Transfer(_from=owner, _to=empty(address), _tokenId=_tokenId)


@external
def approve(approved: address, tokenId: uint256):
    """
    @notice Approve an address to transfer a specific token
    @param approved Address to approve
    @param tokenId Token ID to approve
    """
    owner: address = self._ownerOf[tokenId]
    assert owner != empty(address), "Token does not exist"
    assert owner == msg.sender or self.isApprovedForAll[owner][msg.sender], "Not authorized"

    self.getApproved[tokenId] = approved
    log Approval(_owner=owner, _approved=approved, _tokenId=tokenId)


@external
def setApprovalForAll(_operator: address, _approved: bool):
    """
    @notice Approve or revoke approval for all tokens
    @param _operator Address to approve/revoke
    @param _approved True to approve, False to revoke
    """
    self.isApprovedForAll[msg.sender][_operator] = _approved
    log ApprovalForAll(_owner=msg.sender, _operator=_operator, _approved=_approved)


@external
def transferFrom(sender: address, receiver: address, tokenId: uint256):
    """
    @notice Transfer a token from one address to another
    @param sender Address to transfer from
    @param receiver Address to transfer to
    @param tokenId Token ID to transfer
    """
    assert self._ownerOf[tokenId] == sender, "Token not owned by from address"
    assert receiver != empty(address), "Cannot transfer to zero address"

    # Check authorization
    assert msg.sender == sender or \
           msg.sender == self.getApproved[tokenId] or \
           self.isApprovedForAll[sender][msg.sender], "Not authorized"

    # Clear approval for this token
    if self.getApproved[tokenId] != empty(address):
        self.getApproved[tokenId] = empty(address)

    # Update ownership
    self._ownerOf[tokenId] = receiver
    self.balanceOf[sender] -= 1
    self.balanceOf[receiver] += 1

    log Transfer(_from=sender, _to=receiver, _tokenId=tokenId)


@external
def safeTransferFrom(sender: address, receiver: address, tokenId: uint256, data: Bytes[1024]):
    """
    @notice Safely transfer a token (ERC-721 standard)
    @param sender Address to transfer from
    @param receiver Address to transfer to
    @param tokenId Token ID to transfer
    @param data Additional data
    """
    # Inline transfer logic instead of calling external function
    assert self._ownerOf[tokenId] == sender, "Token not owned by from address"
    assert receiver != empty(address), "Cannot transfer to zero address"

    # Check authorization
    assert msg.sender == sender or \
           msg.sender == self.getApproved[tokenId] or \
           self.isApprovedForAll[sender][msg.sender], "Not authorized"

    # Clear approval for this token
    if self.getApproved[tokenId] != empty(address):
        self.getApproved[tokenId] = empty(address)

    # Update ownership
    self._ownerOf[tokenId] = receiver
    self.balanceOf[sender] -= 1
    self.balanceOf[receiver] += 1

    log Transfer(_from=sender, _to=receiver, _tokenId=tokenId)
    # In a full implementation, we would check if receiver is a contract and call onERC721Received
    # For simplicity, we'll skip that check here

