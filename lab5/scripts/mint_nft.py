"""
Mint new NFT characters
"""
from ape import accounts, project


# Sample character data
CHARACTERS = [
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


def main():
    """Mint NFT characters"""
    # Load accounts
    minter = accounts.load("dev")

    # Get contract address (you need to update this after deployment)
    contract_address = input("Enter contract address: ")
    contract = project.MyCollectibleNFT.at(contract_address)

    # Get recipient address
    recipient = input("Enter recipient address (or press Enter to use minter): ")
    if not recipient:
        recipient = minter.address

    print(f"\nMinting from: {minter.address}")
    print(f"Minting to: {recipient}")

    # Choose which character to mint
    print("\nAvailable characters:")
    for i, char in enumerate(CHARACTERS):
        print(f"{i+1}. {char['name']} - {char['description']}")

    choice = input("\nEnter character number (or 'all' to mint all): ")

    if choice.lower() == 'all':
        # Mint all characters
        for char in CHARACTERS:
            print(f"\nMinting {char['name']}...")
            tx = contract.mint(
                recipient,
                char["tokenId"],
                char["name"],
                char["description"],
                char["imageURI"],
                sender=minter
            )
            print(f"✅ Minted token #{char['tokenId']}: {char['name']}")
            print(f"Transaction: {tx.txn_hash}")
    else:
        # Mint single character
        idx = int(choice) - 1
        if 0 <= idx < len(CHARACTERS):
            char = CHARACTERS[idx]
            print(f"\nMinting {char['name']}...")
            tx = contract.mint(
                recipient,
                char["tokenId"],
                char["name"],
                char["description"],
                char["imageURI"],
                sender=minter
            )
            print(f"✅ Minted token #{char['tokenId']}: {char['name']}")
            print(f"Transaction: {tx.txn_hash}")
        else:
            print("Invalid choice!")
            return

    # Display updated stats
    print(f"\n📊 Contract Stats:")
    print(f"Total Supply: {contract.totalSupply()}")
    print(f"Recipient Balance: {contract.balanceOf(recipient)}")
