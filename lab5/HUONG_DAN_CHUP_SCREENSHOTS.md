# HƯỚNG DẪN CHỤP SCREENSHOTS CHO BÀI TẬP

## 📸 Các screenshots cần chụp

### 1. Compile Contract
```bash
ape compile
```
**Chụp**: Output hiển thị "SUCCESS: 'local project' compiled."

---

### 2. Run Tests
```bash
ape test -v
```
**Chụp**:
- Tổng số tests: 23 passed
- Danh sách tất cả test cases với dấu ✓
- Thời gian chạy

---

### 3. Deploy Contract
```bash
ape run deploy --network ethereum:local:node
```
**Chụp**:
- Contract address
- Contract name, symbol, baseURI
- Minter address
- Total Supply = 0

---

### 4. Query Contract Info
```bash
ape run query_nft --network ethereum:local:node
```
Nhập contract address, chọn option 1

**Chụp**:
- Address
- Name: Digital Character Collection
- Symbol: DCC
- Base URI
- Minter
- Total Supply
- Supports ERC-721: True

---

### 5. Mint NFT - Single Character
```bash
ape run mint_nft --network ethereum:local:node
```
Chọn character số 1 (Cyber Warrior)

**Chụp**:
- Transaction hash
- "✅ Minted token #1: Cyber Warrior"
- Total Supply: 1
- Recipient Balance: 1

---

### 6. Mint All Characters
```bash
ape run mint_nft --network ethereum:local:node
```
Chọn 'all'

**Chụp**:
- Tất cả 4 characters được mint
- Total Supply: 4

---

### 7. Query Token Metadata
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 2, nhập token ID: 1

**Chụp**:
- Owner address
- Name: Cyber Warrior
- Description: Một chiến binh số có khả năng phá mã CRY128
- Image URI
- JSON metadata

---

### 8. Query Owner Info
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 3, nhập minter address

**Chụp**:
- Address
- Token Balance: 4
- Is Minter: True

---

### 9. Approve Address
```bash
ape run approve_nft --network ethereum:local:node
```
Chọn option 1 (approve single token)
- Token ID: 1
- Approved address: [địa chỉ khác]

**Chụp**:
- "✅ Approval successful!"
- Transaction hash
- Message xác nhận

---

### 10. Transfer NFT
```bash
ape run transfer_nft --network ethereum:local:node
```
- Token ID: 1
- Recipient: [địa chỉ mới]

**Chụp**:
- Current owner
- Token info (name, description)
- "✅ Transfer successful!"
- Updated balances
- New owner

---

### 11. Query After Transfer
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 2, token ID: 1

**Chụp**:
- Owner đã thay đổi
- Metadata vẫn giữ nguyên

---

### 12. Burn NFT
```bash
ape run burn_nft --network ethereum:local:node
```
Token ID: 2

**Chụp**:
- Token info trước khi burn
- Current stats
- "✅ Token burned successfully!"
- Updated stats (Total Supply giảm)
- "✅ Token successfully destroyed"

---

### 13. Query Burned Token (Error)
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 2, token ID: 2 (đã burn)

**Chụp**:
- Error message: "Token does not exist"

---

### 14. List All Tokens by Owner
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 5, nhập owner address

**Chụp**:
- Balance
- Danh sách tokens owned
- Token IDs và names

---

### 15. Check Approvals
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 4, sub-option 1
- Token ID: 1

**Chụp**:
- Owner
- Approved address
- Status

---

### 16. Set Approval For All
```bash
ape run approve_nft --network ethereum:local:node
```
Chọn option 2
- Operator address: [địa chỉ]

**Chụp**:
- "✅ Approval successful!"
- Message xác nhận operator

---

### 17. Check Approval For All
```bash
ape run query_nft --network ethereum:local:node
```
Chọn option 4, sub-option 2
- Owner: [địa chỉ của bạn]
- Operator: [địa chỉ đã approve]

**Chụp**:
- Approved for All: True

---

### 18. Code - Smart Contract
**Chụp các phần quan trọng**:
- State variables
- Hàm `mint()`
- Hàm `burn()`
- Hàm `tokenURI()`
- Hàm `transferFrom()`
- Hàm `approve()`

---

### 19. Code - Test File
**Chụp**:
- Import statements
- Fixtures
- Test mint
- Test transfer
- Test burn
- Test metadata

---

### 20. Project Structure
```bash
tree -L 2
```
hoặc
```bash
ls -la
ls -la contracts/
ls -la scripts/
ls -la tests/
```

**Chụp**: Cấu trúc thư mục dự án

---

## 📝 Tips chụp screenshots

1. **Sử dụng terminal có màu sắc** để dễ nhìn
2. **Zoom in** để chữ rõ ràng
3. **Crop** bỏ phần không cần thiết
4. **Đánh số** screenshots theo thứ tự
5. **Ghi chú** mỗi screenshot làm gì

## 📁 Tổ chức screenshots

Tạo folder `screenshots/` và đặt tên file theo format:
```
01_compile_success.png
02_test_all_passed.png
03_deploy_contract.png
04_query_contract_info.png
05_mint_single_character.png
06_mint_all_characters.png
07_query_token_metadata.png
08_transfer_nft.png
09_burn_nft.png
10_code_mint_function.png
11_code_burn_function.png
12_code_tokenURI_function.png
13_test_mint.png
14_test_transfer.png
15_test_burn.png
```

## ✅ Checklist

- [ ] Compile success
- [ ] All tests passed (23/23)
- [ ] Deploy contract
- [ ] Contract info
- [ ] Mint character
- [ ] Query metadata
- [ ] Transfer NFT
- [ ] Approve address
- [ ] Burn NFT
- [ ] Code screenshots
- [ ] Test screenshots
- [ ] Project structure

---

**Lưu ý**: Đảm bảo tất cả screenshots rõ ràng, có đủ thông tin cần thiết để chứng minh chức năng hoạt động đúng!
