import pytest
from moneypoly.game import Game
from moneypoly.property import Property

def test_game_initialization():
    game = Game(["Alice", "Bob"])
    assert len(game.players) == 2
    assert game.players[0].name == "Alice"
    assert game.players[1].name == "Bob"
    assert game.current_index == 0
    assert game.turn_number == 0

def test_current_player_and_advance():
    game = Game(["Alice", "Bob"])
    assert game.current_player().name == "Alice"
    game.advance_turn()
    assert game.current_player().name == "Bob"
    assert game.turn_number == 1
    game.advance_turn()
    assert game.current_player().name == "Alice" # Wraps back to Alice

def test_find_winner():
    game = Game(["Alice", "Bob"])
    game.players[0].balance = 500
    game.players[1].balance = 1000
    
    winner = game.find_winner()
    assert winner.name == "Bob"
    
    game.players.clear()
    assert game.find_winner() is None

def test_check_bankruptcy():
    game = Game(["Alice", "Bob"])
    alice = game.players[0]
    
    prop = Property("Test", 1, 100, 10)
    prop.owner = alice
    alice.add_property(prop)
    
    alice.balance = 0 # Make Alice bankrupt
    game._check_bankruptcy(alice)
    
    assert alice not in game.players
    assert prop.owner is None # Property is immediately released back to the bank
    
def test_card_collect_from_all():
    game = Game(["Alice", "Bob", "Charlie"])
    alice = game.players[0]
    bob = game.players[1]
    charlie = game.players[2]
    
    alice.balance = 1500
    bob.balance = 1500
    charlie.balance = 10 # Charlie is too poor to pay 50
    
    # Alice draws a card saying Collect 50 from everyone
    game._card_collect_from_all(alice, 50)
    
    assert bob.balance == 1450 # Bob pays 50
    assert charlie.balance == 10 # Charlie gets skipped due to insufficient funds branch
    assert alice.balance == 1550 # Alice only collected 50 from Bob
    
def test_pay_rent():
    game = Game(["Alice", "Bob"])
    alice = game.players[0]
    bob = game.players[1]
    
    prop = Property("Boardwalk", 39, 400, 50)
    prop.owner = bob
    
    alice.balance = 1500
    bob.balance = 1500
    
    game.pay_rent(alice, prop)
    
    assert alice.balance == 1450 # Paid 50 to bob
    
    # Mortgaged property rent is 0
    prop.mortgage()
    game.pay_rent(alice, prop)
    assert alice.balance == 1450 # No change, rent avoided!

def test_trade():
    game = Game(["Alice", "Bob"])
    alice = game.players[0]
    bob = game.players[1]
    
    prop = Property("Test", 1, 100, 10)
    prop.owner = alice
    alice.add_property(prop)
    
    # Alice trades Test prop to Bob for $500
    assert game.trade(alice, bob, prop, 500) == True
    assert prop.owner == bob
    assert alice.balance == 1500 + 500
    assert bob.balance == 1500 - 500
    
    # Bob tries to buy another property but cannot afford it
    prop2 = Property("Test2", 2, 100, 10)
    prop2.owner = alice
    alice.add_property(prop2)
    bob.balance = 0
    assert game.trade(alice, bob, prop2, 500) == False
    
    # Bob tries to sell a property he doesn't own
    assert game.trade(bob, alice, prop2, 10) == False

def test_mortgage_unmortgage_property():
    game = Game(["Alice"])
    alice = game.players[0]
    prop = Property("Test", 1, 100, 10)
    
    assert game.mortgage_property(alice, prop) == False # doesn't own
    
    prop.owner = alice
    alice.add_property(prop)
    
    assert game.mortgage_property(alice, prop) == True
    assert alice.balance == 1500 + 50
    assert game.mortgage_property(alice, prop) == False # already mortgaged
    
    assert game.unmortgage_property(alice, prop) == True
    assert alice.balance == 1550 - 55
    assert game.unmortgage_property(alice, prop) == False # not mortgaged

def test_buy_property():
    game = Game(["Alice"])
    alice = game.players[0]
    prop = Property("Test", 1, 100, 10)
    
    assert game.buy_property(alice, prop) == True
    assert alice.balance == 1400
    assert prop.owner == alice
    
    # Cannot afford Expensive property branch
    prop2 = Property("Expensive", 2, 2000, 10)
    assert game.buy_property(alice, prop2) == False
