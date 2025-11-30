"""
Transfer NFT between accounts
"""
from ape import accounts, project


def main():
    """Transfer an NFT"""
    # Load sender account
    sender = accounts.load("dev")

    # Get contract address
    contract_address = input("Enter contract address: ")
    contract = project.MyCollectibleNFT.at(contract_address)

    # Get token ID
    token_id = int(input("Enter token ID to transfer: "))

    # Verify ownership
    try:
        owner = contract.ownerOf(token_id)
        print(f"\nCurrent owner: {owner}")

        if owner.lower() != sender.address.lower():
            print(f"❌ Error: You don't own this token!")
            print(f"Token owner: {owner}")
            print(f"Your address: {sender.address}")
            return
    except Exception as e:
        print(f"❌ Error: Token does not exist or error checking ownership: {e}")
        return

    # Get token metadata
    try:
        name = contract.characterName(token_id)
        description = contract.characterDescription(token_id)
        print(f"\nToken Info:")
        print(f"Name: {name}")
        print(f"Description: {description}")
    except:
        pass

    # Get recipient address
    recipient = input("\nEnter recipient address: ")

    # Confirm transfer
    print(f"\n📦 Transfer Details:")
    print(f"From: {sender.address}")
    print(f"To: {recipient}")
    print(f"Token ID: {token_id}")

    confirm = input("\nConfirm transfer? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Transfer cancelled.")
        return

    # Execute transfer
    print("\nTransferring...")
    try:
        tx = contract.transferFrom(
            sender.address,
            recipient,
            token_id,
            sender=sender
        )
        print(f"✅ Transfer successful!")
        print(f"Transaction: {tx.txn_hash}")

        # Display updated balances
        print(f"\n📊 Updated Balances:")
        print(f"Sender balance: {contract.balanceOf(sender.address)}")
        print(f"Recipient balance: {contract.balanceOf(recipient)}")
        print(f"New owner: {contract.ownerOf(token_id)}")
    except Exception as e:
        print(f"❌ Transfer failed: {e}")
