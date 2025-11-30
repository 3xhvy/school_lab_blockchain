# MyCollectibleNFT - Digital Character Collection

A complete ERC-721 NFT implementation in Vyper 0.4.3 for managing digital character collectibles.

## 📋 Project Overview

This project implements a fully functional NFT (Non-Fungible Token) contract that allows:
- Minting unique digital character NFTs
- Transferring NFTs between accounts
- Burning (destroying) NFTs
- Approving other addresses to manage NFTs
- Storing and retrieving character metadata

## 🏗️ Contract Features

### Core ERC-721 Functions
- `mint()` - Create new NFT characters (minter only)
- `burn()` - Destroy NFTs (owner or approved)
- `transferFrom()` - Transfer NFTs between addresses
- `safeTransferFrom()` - Safe transfer with receiver validation
- `approve()` - Approve address for single token
- `setApprovalForAll()` - Approve operator for all tokens
- `balanceOf()` - Get token balance of address
- `ownerOf()` - Get owner of specific token
- `tokenURI()` - Get JSON metadata for token

### Character Metadata
Each NFT stores:
- **Name**: Character name (max 100 chars)
- **Description**: Character description (max 500 chars)
- **Image URI**: Link to character image (max 200 chars)

### Access Control
- Only the contract deployer (minter) can mint new tokens
- Only token owners or approved addresses can transfer/burn tokens

## 📁 Project Structure

```
lab5/
├── contracts/
│   └── MyCollectibleNFT.vy      # Main NFT contract
├── scripts/
│   ├── deploy.py                # Deploy contract
│   ├── mint_nft.py              # Mint new NFTs
│   ├── transfer_nft.py          # Transfer NFTs
│   ├── burn_nft.py              # Burn NFTs
│   ├── approve_nft.py           # Approve addresses
│   └── query_nft.py             # Query contract info
├── tests/
│   └── test_MyCollectibleNFT.py # Comprehensive test suite
├── ape-config.yaml              # Ape configuration
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Ape framework
- Vyper 0.4.3

### Installation

1. Install dependencies:
```bash
pip install eth-ape ape-vyper
```

2. Install Vyper compiler:
```bash
ape plugins install vyper
```

3. Compile contracts:
```bash
ape compile
```

## 📝 Usage Guide

### 1. Deploy Contract

```bash
ape run deploy
```

This will:
- Deploy the NFT contract
- Set collection name: "Digital Character Collection"
- Set symbol: "DCC"
- Set base URI: "https://school.edu.vn/nft-assets/"
- Return the contract address (save this!)

### 2. Mint NFTs

```bash
ape run mint_nft
```

Pre-configured characters:
1. **Cyber Warrior** - Một chiến binh số có khả năng phá mã CRY128
2. **Data Wizard** - Pháp sư dữ liệu với khả năng phân tích siêu việt
3. **AI Explorer** - Nhà thám hiểm AI khám phá thế giới trí tuệ nhân tạo
4. **Blockchain Guardian** - Người bảo vệ blockchain với sức mạnh mã hóa

### 3. Transfer NFTs

```bash
ape run transfer_nft
```

Transfer tokens between addresses. You must own the token or be approved.

### 4. Burn NFTs

```bash
ape run burn_nft
```

Permanently destroy an NFT. This action is irreversible!

### 5. Approve Addresses

```bash
ape run approve_nft
```

Options:
- Approve single token
- Approve all tokens (operator)
- Revoke approval

### 6. Query Information

```bash
ape run query_nft
```

Query menu:
1. Contract Information
2. Token Information
3. Owner Information
4. Check Approvals
5. List All Tokens

## 🧪 Testing

Run the comprehensive test suite:

```bash
ape test
```

Run specific tests:
```bash
ape test -k test_mint
ape test -k test_transfer
ape test -k test_burn
```

Run with verbose output:
```bash
ape test -v
```

### Test Coverage

The test suite includes:
- ✅ Initialization tests
- ✅ Minting tests (single, multiple, authorization)
- ✅ Metadata tests (storage, retrieval, JSON format)
- ✅ Transfer tests (authorized, unauthorized, safe transfer)
- ✅ Approval tests (single token, all tokens, revocation)
- ✅ Burn tests (owner, approved, unauthorized)
- ✅ Integration tests (full workflows)

## 📊 Contract Information

### State Variables
- `name`: Collection name
- `symbol`: Collection symbol
- `baseURI`: Base URI for metadata
- `totalSupply`: Total number of minted tokens
- `minter`: Address that can mint new tokens
- `ownerOf`: Mapping of token ID to owner
- `balanceOf`: Mapping of address to token count
- `getApproved`: Mapping of token ID to approved address
- `isApprovedForAll`: Mapping of owner to operator approvals

### Events
- `Transfer`: Emitted on mint, transfer, and burn
- `Approval`: Emitted on single token approval
- `ApprovalForAll`: Emitted on operator approval
- `Minted`: Emitted on new token mint

## 🔒 Security Features

1. **Access Control**: Only minter can mint new tokens
2. **Ownership Verification**: All transfers verify ownership
3. **Zero Address Protection**: Cannot mint/transfer to zero address
4. **Duplicate Prevention**: Cannot mint duplicate token IDs
5. **Authorization Checks**: Transfers require ownership or approval

## 🎨 Character Examples

### Cyber Warrior (Token #1)
```json
{
  "name": "Cyber Warrior",
  "description": "Một chiến binh số có khả năng phá mã CRY128",
  "image": "https://school.edu.vn/nft-assets/1.png"
}
```

### Data Wizard (Token #2)
```json
{
  "name": "Data Wizard",
  "description": "Pháp sư dữ liệu với khả năng phân tích siêu việt",
  "image": "https://school.edu.vn/nft-assets/2.png"
}
```

## 🛠️ Development

### Vyper Version
This contract uses Vyper 0.4.3 with the following features:
- `@deploy` decorator for constructor
- `ethereum.ercs` imports (not `vyper.interfaces`)
- Keyword arguments for event logging
- No external function calls via `self`

### Key Changes from Older Vyper Versions
1. Import from `ethereum.ercs` instead of `vyper.interfaces`
2. Use `IERC721` instead of `ERC721`
3. Constructor requires `@deploy` decorator (not `@external`)
4. Events must use keyword arguments
5. Cannot call external functions via `self`

## 📚 Additional Resources

- [Vyper Documentation](https://docs.vyperlang.org/)
- [ERC-721 Standard](https://eips.ethereum.org/EIPS/eip-721)
- [Ape Framework](https://docs.apeworx.io/)

## 🤝 Contributing

This is an educational project for blockchain development learning.

## 📄 License

Educational use only.

## ✅ Requirements Checklist

- [x] Smart contract implementation (Vyper 0.4.3)
- [x] ERC-721 compliance
- [x] Mint functionality
- [x] Burn functionality
- [x] Transfer functionality
- [x] Approval system
- [x] Metadata storage
- [x] Deployment script
- [x] Interaction scripts
- [x] Comprehensive test suite
- [x] Documentation

## 🎯 Next Steps

1. Deploy to a test network (Sepolia, Goerli)
2. Verify contract on Etherscan
3. Create a frontend interface
4. Add more character types
5. Implement rarity system
6. Add marketplace functionality
