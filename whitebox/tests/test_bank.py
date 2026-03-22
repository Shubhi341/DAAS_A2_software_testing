import pytest
from moneypoly.bank import Bank

# We use a Mock Player just to test the bank in isolation
class MockPlayer:
    def __init__(self, name):
        self.name = name
        self.balance = 0
    def add_money(self, amount):
        self.balance += amount

def test_bank_initialization():
    bank = Bank()
    assert bank.get_balance() > 0
    assert bank.loan_count() == 0

def test_bank_collect():
    bank = Bank()
    initial = bank.get_balance()
    bank.collect(500)
    assert bank.get_balance() == initial + 500

def test_bank_pay_out_success():
    bank = Bank()
    initial = bank.get_balance()
    paid = bank.pay_out(500)
    assert paid == 500
    assert bank.get_balance() == initial - 500

def test_bank_pay_out_zero_or_negative():
    bank = Bank()
    assert bank.pay_out(0) == 0
    assert bank.pay_out(-100) == 0

def test_bank_pay_out_insufficient_funds():
    bank = Bank()
    with pytest.raises(ValueError):
        bank.pay_out(bank.get_balance() + 100)

def test_bank_give_loan():
    bank = Bank()
    player = MockPlayer("TestPlayer")
    initial_funds = bank.get_balance()
    
    bank.give_loan(player, 1000)
    
    # Player should receive the money
    assert player.balance == 1000
    # Bank should officially record the loan
    assert bank.loan_count() == 1
    assert bank.total_loans_issued() == 1000
    
    # CRITICAL: Bank funds MUST decrease when issuing a loan from reserves!
    assert bank.get_balance() == initial_funds - 1000
