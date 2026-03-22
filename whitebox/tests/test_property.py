import pytest
from moneypoly.property import Property, PropertyGroup

class MockPlayer:
    def __init__(self, name):
        self.name = name

def test_property_initialization():
    prop = Property("Boardwalk", 39, 400, 50)
    assert prop.name == "Boardwalk"
    assert prop.mortgage_value == 200
    assert not prop.is_mortgaged

def test_property_rent_unmortgaged():
    prop = Property("Boardwalk", 39, 400, 50)
    assert prop.get_rent() == 50

def test_property_rent_mortgaged():
    prop = Property("Boardwalk", 39, 400, 50)
    prop.mortgage()
    assert prop.get_rent() == 0

def test_property_rent_full_group():
    group = PropertyGroup("Blue", "blue")
    prop1 = Property("Park Place", 37, 350, 35)
    prop2 = Property("Boardwalk", 39, 400, 50)
    group.add_property(prop1)
    group.add_property(prop2)
    
    player = MockPlayer("Alice")
    prop1.owner = player
    prop2.owner = player
    
    assert prop1.get_rent() == 35 * Property.FULL_GROUP_MULTIPLIER

def test_property_mortgage_unmortgage():
    prop = Property("Boardwalk", 39, 400, 50)
    assert prop.mortgage() == 200
    assert prop.is_mortgaged
    assert prop.mortgage() == 0 # Already mortgaged
    
    # Unmortgage cost is int(1.1 * mortgage_value)
    assert prop.unmortgage() == int(200 * 1.1)
    assert not prop.is_mortgaged
    assert prop.unmortgage() == 0 # Already unmortgaged

def test_property_is_available():
    prop = Property("Boardwalk", 39, 400, 50)
    assert prop.is_available()
    prop.mortgage()
    assert not prop.is_available()
    prop.unmortgage()
    prop.owner = MockPlayer("Alice")
    assert not prop.is_available()

def test_property_repr():
    prop = Property("Boardwalk", 39, 400, 50)
    assert "unowned" in repr(prop)
    prop.owner = MockPlayer("Alice")
    assert "Alice" in repr(prop)

def test_property_group():
    group = PropertyGroup("Blue", "blue")
    prop = Property("Boardwalk", 39, 400, 50)
    group.add_property(prop)
    group.add_property(prop) # Duplicate add attempt
    assert group.size() == 1
    
    assert not group.all_owned_by(None)
    
    player1 = MockPlayer("Alice")
    player2 = MockPlayer("Bob")
    prop.owner = player1
    
    assert group.all_owned_by(player1)
    assert not group.all_owned_by(player2)
    
    counts = group.get_owner_counts()
    assert counts[player1] == 1
    
    assert "PropertyGroup" in repr(group)
