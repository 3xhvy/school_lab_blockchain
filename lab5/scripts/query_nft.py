"""
Query NFT information
"""
from ape import project, Contract
import json


def main():
    """Query NFT contract and token information"""
    # Get contract address
    contract_address = input("Enter contract address: ")

    try:
        contract = project.MyCollectibleNFT.at(contract_address)
    except Exception as e:
        print(f"❌ Error loading contract: {e}")
        return

    while True:
        print("\n" + "="*60)
        print("NFT Query Menu")
        print("="*60)
        print("1. Contract Information")
        print("2. Token Information")
        print("3. Owner Information")
        print("4. Check Approvals")
        print("5. List All Tokens (by owner)")
        print("6. Exit")
        print("="*60)

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            query_contract_info(contract)
        elif choice == "2":
            query_token_info(contract)
        elif choice == "3":
            query_owner_info(contract)
        elif choice == "4":
            query_approvals(contract)
        elif choice == "5":
            list_owner_tokens(contract)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


def query_contract_info(contract):
    """Display contract information"""
    print("\n📋 Contract Information:")
    print(f"Address: {contract.address}")
    print(f"Name: {contract.name()}")
    print(f"Symbol: {contract.symbol()}")
    print(f"Base URI: {contract.baseURI()}")
    print(f"Minter: {contract.minter()}")
    print(f"Total Supply: {contract.totalSupply()}")

    # Check ERC-165 support
    try:
        erc721_interface = bytes.fromhex("80ac58cd")
        supports_erc721 = contract.supportsInterface(erc721_interface)
        print(f"Supports ERC-721: {supports_erc721}")
    except:
        pass


def query_token_info(contract):
    """Display token information"""
    token_id = int(input("\nEnter token ID: "))

    try:
        owner = contract.ownerOf(token_id)
        name = contract.characterName(token_id)
        description = contract.characterDescription(token_id)
        image_uri = contract.characterImageURI(token_id)

        print(f"\n🎨 Token #{token_id} Information:")
        print(f"Owner: {owner}")
        print(f"Name: {name}")
        print(f"Description: {description}")
        print(f"Image URI: {image_uri}")

        # Get metadata JSON
        try:
            metadata_json = contract.tokenURI(token_id)
            print(f"\n📄 Metadata JSON:")
            # Try to pretty print if it's valid JSON
            try:
                metadata_dict = json.loads(metadata_json)
                print(json.dumps(metadata_dict, indent=2))
            except:
                print(metadata_json)
        except Exception as e:
            print(f"Could not retrieve metadata: {e}")

    except Exception as e:
        print(f"❌ Error: Token does not exist or error retrieving info: {e}")


def query_owner_info(contract):
    """Display owner information"""
    owner_address = input("\nEnter owner address: ")

    try:
        balance = contract.balanceOf(owner_address)
        print(f"\n👤 Owner Information:")
        print(f"Address: {owner_address}")
        print(f"Token Balance: {balance}")

        is_minter = contract.minter().lower() == owner_address.lower()
        print(f"Is Minter: {is_minter}")
    except Exception as e:
        print(f"❌ Error: {e}")


def query_approvals(contract):
    """Check approval status"""
    print("\nCheck Approval:")
    print("1. Check single token approval")
    print("2. Check operator approval (all tokens)")

    choice = input("Enter choice (1-2): ")

    if choice == "1":
        token_id = int(input("Enter token ID: "))
        try:
            approved = contract.getApproved(token_id)
            owner = contract.ownerOf(token_id)
            print(f"\n✅ Token #{token_id}:")
            print(f"Owner: {owner}")
            print(f"Approved: {approved}")
            if approved == "0x0000000000000000000000000000000000000000":
                print("Status: No approval set")
            else:
                print(f"Status: Approved for {approved}")
        except Exception as e:
            print(f"❌ Error: {e}")

    elif choice == "2":
        owner = input("Enter owner address: ")
        operator = input("Enter operator address: ")
        try:
            is_approved = contract.isApprovedForAll(owner, operator)
            print(f"\n✅ Approval Status:")
            print(f"Owner: {owner}")
            print(f"Operator: {operator}")
            print(f"Approved for All: {is_approved}")
        except Exception as e:
            print(f"❌ Error: {e}")


def list_owner_tokens(contract):
    """List all tokens owned by an address"""
    owner_address = input("\nEnter owner address: ")

    try:
        balance = contract.balanceOf(owner_address)
        total_supply = contract.totalSupply()

        print(f"\n📦 Tokens owned by {owner_address}:")
        print(f"Balance: {balance}")

        if balance == 0:
            print("No tokens owned.")
            return

        print("\nSearching for tokens...")
        owned_tokens = []

        # Search through possible token IDs (this is inefficient but works for small collections)
        # In production, you'd want to use events or maintain an index
        for token_id in range(1, 1000):  # Check first 1000 token IDs
            try:
                token_owner = contract.ownerOf(token_id)
                if token_owner.lower() == owner_address.lower():
                    name = contract.characterName(token_id)
                    owned_tokens.append((token_id, name))
            except:
                continue

        if owned_tokens:
            print(f"\nFound {len(owned_tokens)} token(s):")
            for token_id, name in owned_tokens:
                print(f"  • Token #{token_id}: {name}")
        else:
            print("No tokens found (search range may be insufficient)")

    except Exception as e:
        print(f"❌ Error: {e}")
