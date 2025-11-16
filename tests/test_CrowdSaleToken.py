import pytest
from ape import accounts, project

@pytest.fixture
def crowd_sale_token(deployer):
    return deployer.deploy(project.CrowdSaleToken_22520542, "CrowdSale", "CS", 18, 1000)

def test_initial_setup(crowd_sale_token, deployer):
    """Test initial contract setup"""
    assert crowd_sale_token.name() == "CrowdSale"
    assert crowd_sale_token.symbol() == "CS"
    assert crowd_sale_token.decimals() == 18
    assert crowd_sale_token.beneficiary() == deployer.address
    assert crowd_sale_token.minFundingGoal() == 30 * 10**18  # 30 ETH
    assert crowd_sale_token.maxFundingGoal() == 50 * 10**18  # 50 ETH
    assert crowd_sale_token.price() == 10**16  # 0.01 ETH
    assert crowd_sale_token.fundingGoalReached() == False
    assert crowd_sale_token.crowdsaleClosed() == False

def test_token_purchase(crowd_sale_token, accounts):
    """Test buying tokens with ETH"""
    buyer = accounts[1]
    purchase_amount = 10**17  # 0.1 ETH

    # Buy tokens
    buyer.transfer(crowd_sale_token.address, purchase_amount)

    # Check balances
    expected_tokens = purchase_amount // crowd_sale_token.price()  # 10 tokens
    assert crowd_sale_token.balanceOf(buyer.address) == expected_tokens
    assert crowd_sale_token.ethBalances(buyer.address) == purchase_amount
    assert crowd_sale_token.amountRaised() == purchase_amount

def test_multiple_purchases(crowd_sale_token, accounts):
    """Test multiple token purchases"""
    buyer1 = accounts[1]
    buyer2 = accounts[2]

    # First purchase
    buyer1.transfer(crowd_sale_token.address, 10**17)  # 0.1 ETH

    # Second purchase
    buyer2.transfer(crowd_sale_token.address, 2 * 10**17)  # 0.2 ETH

    # Check total amount raised
    assert crowd_sale_token.amountRaised() == 3 * 10**17  # 0.3 ETH total

def test_purchase_restrictions(crowd_sale_token, deployer, accounts):
    """Test purchase restrictions"""
    buyer = accounts[1]

    # Test minimum purchase amount
    with pytest.raises(Exception):
        buyer.transfer(crowd_sale_token.address, 10**15)  # 0.001 ETH (too small)

    # Test beneficiary cannot buy
    with pytest.raises(Exception):
        deployer.transfer(crowd_sale_token.address, 10**17)

def test_funding_goal_reached(crowd_sale_token, accounts, chain):
    """Test funding goal reached scenario"""
    # Buy enough tokens to reach minimum funding goal
    for i in range(1, 4):  # accounts 1, 2, 3
        accounts[i].transfer(crowd_sale_token.address, 10 * 10**18)  # 10 ETH each

    # Fast forward time past deadline
    chain.pending_timestamp += 3600 * 24 * 101  # 101 days
    chain.mine()

    # Check goal reached
    crowd_sale_token.checkGoalReached(sender=accounts[0])
    assert crowd_sale_token.fundingGoalReached() == True
    assert crowd_sale_token.crowdsaleClosed() == True

def test_safe_withdrawal_success(crowd_sale_token, deployer, accounts, chain):
    """Test successful withdrawal by beneficiary"""
    # Buy tokens to reach funding goal
    for i in range(1, 4):
        accounts[i].transfer(crowd_sale_token.address, 10 * 10**18)

    # Fast forward and close crowdsale
    chain.pending_timestamp += 3600 * 24 * 101
    chain.mine()
    crowd_sale_token.checkGoalReached(sender=deployer)

    # Beneficiary withdraws
    initial_balance = deployer.balance
    crowd_sale_token.safeWithdrawal(sender=deployer)

    # Check withdrawal successful
    assert deployer.balance > initial_balance

def test_safe_withdrawal_refund(crowd_sale_token, accounts, chain):
    """Test refund when funding goal not reached"""
    buyer = accounts[1]
    purchase_amount = 10**18  # 1 ETH

    # Buy tokens (not enough to reach goal)
    buyer.transfer(crowd_sale_token.address, purchase_amount)

    # Fast forward and close crowdsale
    chain.pending_timestamp += 3600 * 24 * 101
    chain.mine()
    crowd_sale_token.checkGoalReached(sender=accounts[0])

    # Buyer gets refund
    initial_balance = buyer.balance
    crowd_sale_token.safeWithdrawal(sender=buyer)

    # Check refund received and tokens returned
    assert buyer.balance > initial_balance
    assert crowd_sale_token.balanceOf(buyer.address) == 0
    assert crowd_sale_token.ethBalances(buyer.address) == 0
