import pytest
from moneypoly.board import Board
from moneypoly.config import JAIL_POSITION

class MockPlayer:
    def __init__(self, name):
        self.name = name

def test_board_initialization():
    board = Board()
    assert len(board.properties) == 22
    assert len(board.groups) == 8

def test_get_property_at():
    board = Board()
    prop = board.get_property_at(39) # Boardwalk
    assert prop is not None
    assert prop.name == "Boardwalk"
    assert board.get_property_at(0) is None # Go tile

def test_get_tile_type():
    board = Board()
    assert board.get_tile_type(0) == "go"
    assert board.get_tile_type(JAIL_POSITION) == "jail"
    assert board.get_tile_type(2) == "community_chest"
    assert board.get_tile_type(39) == "property"
    assert board.get_tile_type(1) == "property" # Mediterranean Avenue
    assert board.get_tile_type(999) == "blank"

def test_is_purchasable():
    board = Board()
    assert not board.is_purchasable(0) # Special tile
    assert board.is_purchasable(39) # Boardwalk is purchasable
    
    prop = board.get_property_at(39)
    prop.mortgage()
    assert not board.is_purchasable(39) # Not purchasable if mortgaged
    
    prop.unmortgage()
    prop.owner = MockPlayer("Alice")
    assert not board.is_purchasable(39) # Not purchasable if owned

def test_is_special_tile():
    board = Board()
    assert board.is_special_tile(0)
    assert not board.is_special_tile(39)

def test_unowned_and_owned_properties():
    board = Board()
    initial_unowned = len(board.unowned_properties())
    assert initial_unowned == 22
    
    player = MockPlayer("Alice")
    assert len(board.properties_owned_by(player)) == 0
    
    prop = board.get_property_at(39)
    prop.owner = player
    
    assert len(board.unowned_properties()) == 21
    assert len(board.properties_owned_by(player)) == 1
    assert board.properties_owned_by(player)[0].name == "Boardwalk"

def test_board_repr():
    board = Board()
    assert "Board(22 properties, 0 owned)" in repr(board)
    board.get_property_at(39).owner = MockPlayer("Alice")
    assert "Board(22 properties, 1 owned)" in repr(board)
