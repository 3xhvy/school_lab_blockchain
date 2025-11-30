"""
Approve addresses to manage NFTs
"""
from ape import accounts, project


def main():
    """Approve an address to manage NFTs"""
    # Load account
    owner = accounts.load("dev")

    # Get contract address
    contract_address = input("Enter contract address: ")
    contract = project.MyCollectibleNFT.at(contract_address)

    print("\n" + "="*60)
    print("NFT Approval Menu")
    print("="*60)
    print("1. Approve single token")
    print("2. Approve all tokens (setApprovalForAll)")
    print("3. Revoke approval for all tokens")
    print("="*60)

    choice = input("\nEnter your choice (1-3): ")

    if choice == "1":
        approve_single_token(contract, owner)
    elif choice == "2":
        approve_all_tokens(contract, owner, True)
    elif choice == "3":
        approve_all_tokens(contract, owner, False)
    else:
        print("Invalid choice!")


def approve_single_token(contract, owner):
    """Approve an address for a single token"""
    token_id = int(input("\nEnter token ID: "))

    # Verify ownership
    try:
        token_owner = contract.ownerOf(token_id)
        if token_owner.lower() != owner.address.lower():
            print(f"❌ Error: You don't own this token!")
            print(f"Token owner: {token_owner}")
            print(f"Your address: {owner.address}")
            return
    except Exception as e:
        print(f"❌ Error: Token does not exist: {e}")
        return

    # Get token info
    try:
        name = contract.characterName(token_id)
        print(f"\nToken: {name} (#{token_id})")
    except:
        print(f"\nToken ID: {token_id}")

    # Get approved address
    approved_address = input("Enter address to approve: ")

    # Show current approval
    try:
        current_approved = contract.getApproved(token_id)
        print(f"\nCurrent approval: {current_approved}")
    except:
        pass

    # Confirm
    print(f"\n📋 Approval Details:")
    print(f"Token ID: {token_id}")
    print(f"Approving: {approved_address}")

    confirm = input("\nConfirm approval? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Approval cancelled.")
        return

    # Execute approval
    try:
        tx = contract.approve(approved_address, token_id, sender=owner)
        print(f"✅ Approval successful!")
        print(f"Transaction: {tx.txn_hash}")
        print(f"\n{approved_address} can now transfer token #{token_id}")
    except Exception as e:
        print(f"❌ Approval failed: {e}")


def approve_all_tokens(contract, owner, approved):
    """Set approval for all tokens"""
    operator_address = input("\nEnter operator address: ")

    # Show current status
    try:
        current_status = contract.isApprovedForAll(owner.address, operator_address)
        print(f"\nCurrent status: {'Approved' if current_status else 'Not approved'}")
    except:
        pass

    # Confirm
    action = "approve" if approved else "revoke approval for"
    print(f"\n📋 Approval Details:")
    print(f"Action: {action.capitalize()} all tokens")
    print(f"Operator: {operator_address}")
    print(f"Owner: {owner.address}")

    confirm = input(f"\nConfirm {action}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Action cancelled.")
        return

    # Execute
    try:
        tx = contract.setApprovalForAll(operator_address, approved, sender=owner)
        print(f"✅ {'Approval' if approved else 'Revocation'} successful!")
        print(f"Transaction: {tx.txn_hash}")

        if approved:
            print(f"\n{operator_address} can now manage all your tokens")
        else:
            print(f"\n{operator_address} can no longer manage your tokens")
    except Exception as e:
        print(f"❌ Action failed: {e}")
