"""
Comprehensive test suite for MyCollectibleNFT contract
Tests all functionality including mint, burn, transfer, approve, and metadata
"""

import pytest
from ape import accounts, project


@pytest.fixture
def deployer(accounts):
    """Deployer account (minter)"""
    return accounts[0]


@pytest.fixture
def user1(accounts):
    """First user account"""
    return accounts[1]


@pytest.fixture
def user2(accounts):
    """Second user account"""
    return accounts[2]


@pytest.fixture
def contract(deployer, project):
    """Deploy the MyCollectibleNFT contract"""
    return deployer.deploy(
        project.MyCollectibleNFT,
        "Digital Character Collection",
        "DCC",
        "https://school.edu.vn/nft-assets/"
    )


@pytest.fixture
def sample_characters():
    """Sample character data for testing"""
    return [
        {
            "tokenId": 1,
            "name": "Cyber Warrior",
            "description": "Một chiến binh số có khả năng phá mã CRY128",
            "imageURI": "https://school.edu.vn/nft-assets/1.png"
        },
        {
            "tokenId": 2,
            "name": "Data Wizard",
            "description": "Pháp sư dữ liệu với khả năng phân tích siêu việt",
            "imageURI": "https://school.edu.vn/nft-assets/2.png"
        },
        {
            "tokenId": 3,
            "name": "AI Explorer",
            "description": "Nhà thám hiểm AI khám phá thế giới trí tuệ nhân tạo",
            "imageURI": "https://school.edu.vn/nft-assets/3.png"
        },
        {
            "tokenId": 4,
            "name": "Blockchain Guardian",
            "description": "Người bảo vệ blockchain với sức mạnh mã hóa",
            "imageURI": "https://school.edu.vn/nft-assets/4.png"
        }
    ]


# ========== Initialization Tests ==========

def test_init(contract, deployer):
    """Test contract initialization"""
    assert contract.name() == "Digital Character Collection"
    assert contract.symbol() == "DCC"
    assert contract.baseURI() == "https://school.edu.vn/nft-assets/"
    assert contract.minter() == deployer
    assert contract.totalSupply() == 0


# ========== Minting Tests ==========

def test_mint_new_character(contract, deployer, user1, sample_characters):
    """Test minting a new character NFT"""
    char = sample_characters[0]

    # Mint the NFT
    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # Verify ownership
    assert contract.ownerOf(char["tokenId"]) == user1
    assert contract.balanceOf(user1) == 1
    assert contract.totalSupply() == 1

    # Verify metadata
    assert contract.characterName(char["tokenId"]) == char["name"]
    assert contract.characterDescription(char["tokenId"]) == char["description"]
    assert contract.characterImageURI(char["tokenId"]) == char["imageURI"]


def test_mint_multiple_characters(contract, deployer, user1, sample_characters):
    """Test minting multiple characters"""
    for char in sample_characters:
        contract.mint(
            user1,
            char["tokenId"],
            char["name"],
            char["description"],
            char["imageURI"],
            sender=deployer
        )

    assert contract.balanceOf(user1) == len(sample_characters)
    assert contract.totalSupply() == len(sample_characters)

    # Verify all characters are owned by user1
    for char in sample_characters:
        assert contract.ownerOf(char["tokenId"]) == user1


def test_mint_only_by_minter(contract, user1, sample_characters):
    """Test that only minter can mint"""
    char = sample_characters[0]

    with pytest.raises(Exception):
        contract.mint(
            user1,
            char["tokenId"],
            char["name"],
            char["description"],
            char["imageURI"],
            sender=user1  # Non-minter trying to mint
        )


def test_mint_duplicate_token_id(contract, deployer, user1, sample_characters):
    """Test that duplicate token IDs cannot be minted"""
    char = sample_characters[0]

    # Mint first time
    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # Try to mint again with same token ID
    with pytest.raises(Exception):
        contract.mint(
            user1,
            char["tokenId"],
            "Duplicate",
            "Duplicate description",
            "https://example.com/duplicate.png",
            sender=deployer
        )


def test_mint_to_zero_address(contract, deployer, sample_characters):
    """Test that minting to zero address fails"""
    char = sample_characters[0]
    zero_address = "0x0000000000000000000000000000000000000000"

    with pytest.raises(Exception):
        contract.mint(
            zero_address,
            char["tokenId"],
            char["name"],
            char["description"],
            char["imageURI"],
            sender=deployer
        )


# ========== Metadata Tests ==========

def test_tokenURI(contract, deployer, user1, sample_characters):
    """Test tokenURI returns correct JSON metadata"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    metadata = contract.tokenURI(char["tokenId"])

    # Verify JSON structure contains the character data
    assert char["name"] in metadata
    assert char["description"] in metadata
    assert char["imageURI"] in metadata
    assert '"name"' in metadata
    assert '"description"' in metadata
    assert '"image"' in metadata


def test_character_metadata_storage(contract, deployer, user1, sample_characters):
    """Test that character metadata is stored correctly"""
    for char in sample_characters:
        contract.mint(
            user1,
            char["tokenId"],
            char["name"],
            char["description"],
            char["imageURI"],
            sender=deployer
        )

        assert contract.characterName(char["tokenId"]) == char["name"]
        assert contract.characterDescription(char["tokenId"]) == char["description"]
        assert contract.characterImageURI(char["tokenId"]) == char["imageURI"]


def test_tokenURI_nonexistent_token(contract):
    """Test tokenURI for non-existent token fails"""
    with pytest.raises(Exception):
        contract.tokenURI(999)


# ========== Transfer Tests ==========

def test_transferFrom(contract, deployer, user1, user2, sample_characters):
    """Test transferring NFT from one user to another"""
    char = sample_characters[0]

    # Mint to user1
    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # Transfer from user1 to user2
    contract.transferFrom(user1, user2, char["tokenId"], sender=user1)

    # Verify ownership changed
    assert contract.ownerOf(char["tokenId"]) == user2
    assert contract.balanceOf(user1) == 0
    assert contract.balanceOf(user2) == 1


def test_transferFrom_unauthorized(contract, deployer, user1, user2, sample_characters):
    """Test that unauthorized transfer fails"""
    char = sample_characters[0]

    # Mint to user1
    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # Try to transfer without authorization
    with pytest.raises(Exception):
        contract.transferFrom(user1, user2, char["tokenId"], sender=user2)


def test_transferFrom_to_zero_address(contract, deployer, user1, sample_characters):
    """Test that transferring to zero address fails"""
    char = sample_characters[0]
    zero_address = "0x0000000000000000000000000000000000000000"

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    with pytest.raises(Exception):
        contract.transferFrom(user1, zero_address, char["tokenId"], sender=user1)


def test_safeTransferFrom(contract, deployer, user1, user2, sample_characters):
    """Test safeTransferFrom function"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    contract.safeTransferFrom(user1, user2, char["tokenId"], b"", sender=user1)

    assert contract.ownerOf(char["tokenId"]) == user2
    assert contract.balanceOf(user2) == 1


# ========== Approval Tests ==========

def test_approve(contract, deployer, user1, user2, sample_characters):
    """Test approving an address to transfer a token"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # User1 approves user2
    contract.approve(user2, char["tokenId"], sender=user1)

    assert contract.getApproved(char["tokenId"]) == user2

    # User2 can now transfer
    contract.transferFrom(user1, user2, char["tokenId"], sender=user2)
    assert contract.ownerOf(char["tokenId"]) == user2


def test_approve_unauthorized(contract, deployer, user1, user2, sample_characters):
    """Test that non-owner cannot approve"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # User2 tries to approve themselves (should fail)
    with pytest.raises(Exception):
        contract.approve(user2, char["tokenId"], sender=user2)


def test_setApprovalForAll(contract, deployer, user1, user2, sample_characters):
    """Test setting approval for all tokens"""
    # Mint multiple tokens to user1
    for char in sample_characters[:2]:
        contract.mint(
            user1,
            char["tokenId"],
            char["name"],
            char["description"],
            char["imageURI"],
            sender=deployer
        )

    # User1 approves user2 for all tokens
    contract.setApprovalForAll(user2, True, sender=user1)
    assert contract.isApprovedForAll(user1, user2) == True

    # User2 can transfer both tokens
    contract.transferFrom(user1, user2, sample_characters[0]["tokenId"], sender=user2)
    contract.transferFrom(user1, user2, sample_characters[1]["tokenId"], sender=user2)

    assert contract.ownerOf(sample_characters[0]["tokenId"]) == user2
    assert contract.ownerOf(sample_characters[1]["tokenId"]) == user2


def test_revoke_approvalForAll(contract, deployer, user1, user2, sample_characters):
    """Test revoking approval for all tokens"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # Approve
    contract.setApprovalForAll(user2, True, sender=user1)
    assert contract.isApprovedForAll(user1, user2) == True

    # Revoke
    contract.setApprovalForAll(user2, False, sender=user1)
    assert contract.isApprovedForAll(user1, user2) == False

    # Now user2 cannot transfer
    with pytest.raises(Exception):
        contract.transferFrom(user1, user2, char["tokenId"], sender=user2)


# ========== Burn Tests ==========

def test_burn(contract, deployer, user1, sample_characters):
    """Test burning an NFT"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    initial_balance = contract.balanceOf(user1)
    initial_supply = contract.totalSupply()

    # Burn the token
    contract.burn(char["tokenId"], sender=user1)

    # Verify token is burned
    assert contract.balanceOf(user1) == initial_balance - 1
    assert contract.totalSupply() == initial_supply - 1

    # Verify metadata is cleared
    assert contract.characterName(char["tokenId"]) == ""
    assert contract.characterDescription(char["tokenId"]) == ""
    assert contract.characterImageURI(char["tokenId"]) == ""

    # Verify token no longer exists
    with pytest.raises(Exception):
        contract.ownerOf(char["tokenId"])


def test_burn_unauthorized(contract, deployer, user1, user2, sample_characters):
    """Test that non-owner cannot burn"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # User2 tries to burn user1's token
    with pytest.raises(Exception):
        contract.burn(char["tokenId"], sender=user2)


def test_burn_with_approval(contract, deployer, user1, user2, sample_characters):
    """Test that approved address can burn"""
    char = sample_characters[0]

    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )

    # User1 approves user2
    contract.approve(user2, char["tokenId"], sender=user1)

    # User2 can burn
    contract.burn(char["tokenId"], sender=user2)

    # Verify token is burned
    with pytest.raises(Exception):
        contract.ownerOf(char["tokenId"])


def test_burn_nonexistent_token(contract, user1):
    """Test burning non-existent token fails"""
    with pytest.raises(Exception):
        contract.burn(999, sender=user1)


# ========== Integration Tests ==========

def test_full_workflow(contract, deployer, user1, user2, sample_characters):
    """Test complete workflow: mint -> transfer -> approve -> transfer -> burn"""
    char = sample_characters[0]

    # 1. Mint
    contract.mint(
        user1,
        char["tokenId"],
        char["name"],
        char["description"],
        char["imageURI"],
        sender=deployer
    )
    assert contract.ownerOf(char["tokenId"]) == user1

    # 2. Transfer
    contract.transferFrom(user1, user2, char["tokenId"], sender=user1)
    assert contract.ownerOf(char["tokenId"]) == user2

    # 3. Approve
    contract.approve(user1, char["tokenId"], sender=user2)
    assert contract.getApproved(char["tokenId"]) == user1

    # 4. Transfer back using approval
    contract.transferFrom(user2, user1, char["tokenId"], sender=user1)
    assert contract.ownerOf(char["tokenId"]) == user1

    # 5. Burn
    contract.burn(char["tokenId"], sender=user1)
    with pytest.raises(Exception):
        contract.ownerOf(char["tokenId"])


def test_multiple_characters_operations(contract, deployer, user1, user2, sample_characters):
    """Test operations with multiple characters"""
    # Mint all characters to user1
    for char in sample_characters:
        contract.mint(
            user1,
            char["tokenId"],
            char["name"],
            char["description"],
            char["imageURI"],
            sender=deployer
        )

    assert contract.balanceOf(user1) == len(sample_characters)

    # Transfer some to user2
    contract.transferFrom(user1, user2, sample_characters[0]["tokenId"], sender=user1)
    contract.transferFrom(user1, user2, sample_characters[1]["tokenId"], sender=user1)

    assert contract.balanceOf(user1) == 2
    assert contract.balanceOf(user2) == 2

    # Burn one from user1
    contract.burn(sample_characters[2]["tokenId"], sender=user1)
    assert contract.balanceOf(user1) == 1
    assert contract.totalSupply() == 3

