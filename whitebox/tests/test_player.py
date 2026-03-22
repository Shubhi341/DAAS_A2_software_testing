import pytest
from moneypoly.player import Player
from moneypoly.config import STARTING_BALANCE, BOARD_SIZE, GO_SALARY, JAIL_POSITION

class MockProperty:
    def __init__(self, name):
        self.name = name

def test_player_initialization():
    p = Player("Alice")
    assert p.name == "Alice"
    assert p.balance == STARTING_BALANCE
    assert p.position == 0
    assert p.properties == []
    assert not p.in_jail

def test_add_money():
    p = Player("Alice", 100)
    p.add_money(50)
    assert p.balance == 150
    with pytest.raises(ValueError, match="negative amount"):
        p.add_money(-10)

def test_deduct_money():
    p = Player("Alice", 100)
    p.deduct_money(50)
    assert p.balance == 50
    with pytest.raises(ValueError, match="negative amount"):
        p.deduct_money(-10)

def test_is_bankrupt():
    p = Player("Alice", 100)
    assert not p.is_bankrupt()
    p.deduct_money(100)
    assert p.is_bankrupt()

def test_net_worth():
    p = Player("Alice", 100)
    assert p.net_worth() == 100

def test_move_normal():
    p = Player("Alice", 100)
    p.move(5)
    assert p.position == 5
    assert p.balance == 100

def test_move_pass_go():
    p = Player("Alice", 100)
    # Put them right before GO
    p.position = BOARD_SIZE - 2
    # Move them past GO
    p.move(5)
    assert p.position == 3
    # Check if they got the $200 GO salary!
    assert p.balance == 100 + GO_SALARY

def test_go_to_jail():
    p = Player("Alice")
    p.go_to_jail()
    assert p.position == JAIL_POSITION
    assert p.in_jail
    assert p.jail_turns == 0

def test_add_remove_property():
    p = Player("Alice")
    prop = MockProperty("Park Place")
    p.add_property(prop)
    assert prop in p.properties
    p.add_property(prop) # duplicate add attempt
    assert len(p.properties) == 1
    
    assert p.count_properties() == 1
    
    p.remove_property(prop)
    assert prop not in p.properties
    p.remove_property(prop) # remove non-existent attempt
    assert len(p.properties) == 0

def test_status_line():
    p = Player("Alice", 100)
    status = p.status_line()
    assert "Alice: $100" in status
    assert "pos=0" in status
    p.go_to_jail()
    status = p.status_line()
    assert "[JAILED]" in status

def test_repr():
    p = Player("Alice", 100)
    assert repr(p) == "Player('Alice', balance=100, pos=0)"
