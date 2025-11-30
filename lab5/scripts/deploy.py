"""
Deploy MyCollectibleNFT contract
"""
from ape import accounts, project


def main():
    """Deploy the NFT contract"""
    # Get deployer account (will prompt for selection)
    deployer = accounts.load("dev")

    print(f"Deploying from account: {deployer.address}")
    print(f"Account balance: {deployer.balance / 1e18} ETH")

    # Deploy contract
    print("\nDeploying MyCollectibleNFT contract...")
    contract = deployer.deploy(
        project.MyCollectibleNFT,
        "Digital Character Collection",  # name
        "DCC",                           # symbol
        "https://school.edu.vn/nft-assets/"  # baseURI
    )

    print(f"\n✅ Contract deployed successfully!")
    print(f"Contract address: {contract.address}")
    print(f"Contract name: {contract.name()}")
    print(f"Contract symbol: {contract.symbol()}")
    print(f"Base URI: {contract.baseURI()}")
    print(f"Minter: {contract.minter()}")
    print(f"Total Supply: {contract.totalSupply()}")

    return contract
