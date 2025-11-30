"""
Burn (destroy) an NFT
"""
from ape import accounts, project


def main():
    """Burn an NFT"""
    # Load account
    burner = accounts.load("dev")

    # Get contract address
    contract_address = input("Enter contract address: ")
    contract = project.MyCollectibleNFT.at(contract_address)

    # Get token ID
    token_id = int(input("Enter token ID to burn: "))

    # Verify ownership and get token info
    try:
        owner = contract.ownerOf(token_id)
        print(f"\nCurrent owner: {owner}")

        if owner.lower() != burner.address.lower():
            # Check if burner is approved
            approved = contract.getApproved(token_id)
            approved_for_all = contract.isApprovedForAll(owner, burner.address)

            if approved.lower() != burner.address.lower() and not approved_for_all:
                print(f"❌ Error: You are not authorized to burn this token!")
                print(f"Token owner: {owner}")
                print(f"Your address: {burner.address}")
                return
    except Exception as e:
        print(f"❌ Error: Token does not exist or error checking ownership: {e}")
        return

    # Get token metadata
    try:
        name = contract.characterName(token_id)
        description = contract.characterDescription(token_id)
        image_uri = contract.characterImageURI(token_id)

        print(f"\n🔥 Token to Burn:")
        print(f"Token ID: {token_id}")
        print(f"Name: {name}")
        print(f"Description: {description}")
        print(f"Image URI: {image_uri}")
    except:
        print(f"\n🔥 Token ID: {token_id}")

    # Get current stats
    total_supply = contract.totalSupply()
    owner_balance = contract.balanceOf(owner)

    print(f"\n📊 Current Stats:")
    print(f"Total Supply: {total_supply}")
    print(f"Owner Balance: {owner_balance}")

    # Confirm burn
    print(f"\n⚠️  WARNING: This action is irreversible!")
    confirm = input("Are you sure you want to burn this NFT? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Burn cancelled.")
        return

    # Execute burn
    print("\nBurning token...")
    try:
        tx = contract.burn(token_id, sender=burner)
        print(f"✅ Token burned successfully!")
        print(f"Transaction: {tx.txn_hash}")

        # Display updated stats
        print(f"\n📊 Updated Stats:")
        print(f"Total Supply: {contract.totalSupply()}")
        print(f"Owner Balance: {contract.balanceOf(owner)}")

        # Verify token is gone
        try:
            contract.ownerOf(token_id)
            print("⚠️  Warning: Token still exists (unexpected)")
        except:
            print("✅ Token successfully destroyed")
    except Exception as e:
        print(f"❌ Burn failed: {e}")
