import pytest
from moneypoly.dice import Dice

def test_dice_roll_bounds():
    dice = Dice()
    seen_faces = set()
    
    for _ in range(1000):
        dice.roll()
        seen_faces.add(dice.die1)
        seen_faces.add(dice.die2)
        
        assert 1 <= dice.die1 <= 6
        assert 1 <= dice.die2 <= 6
        
    assert 6 in seen_faces

def test_dice_doubles_streak():
    dice = Dice()
    
    dice.die1 = 3
    dice.die2 = 3
    assert dice.is_doubles() is True
    
    dice.die1 = 3
    dice.die2 = 4
    assert dice.is_doubles() is False

def test_dice_reset():
    dice = Dice()
    dice.die1 = 3
    dice.die2 = 3
    dice.doubles_streak = 1
    
    dice.reset()
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0

def test_dice_total():
    dice = Dice()
    dice.die1 = 3
    dice.die2 = 4
    assert dice.total() == 7

def test_dice_describe():
    dice = Dice()
    dice.die1 = 3
    dice.die2 = 4
    desc = dice.describe()
    assert "3 + 4 = 7" in desc
    assert "DOUBLES" not in desc
    
    dice.die1 = 3
    dice.die2 = 3
    desc = dice.describe()
    assert "3 + 3 = 6 (DOUBLES)" in desc

def test_dice_roll_updates_streak(monkeypatch):
    dice = Dice()
    import random
    # Force the dice to roll two 3s
    monkeypatch.setattr(random, "randint", lambda a, b: 3)
    
    total = dice.roll()
    assert total == 6
    assert dice.doubles_streak == 1
    
    dice.roll()
    assert dice.doubles_streak == 2
    
    # Force the dice to alternate missing doubles (e.g. 4 and 3)
    counts = {"val": 3}
    def mock_randint(a, b):
        counts["val"] = 7 - counts["val"] 
        return counts["val"]
        
    monkeypatch.setattr(random, "randint", mock_randint)
    dice.roll()
    assert dice.doubles_streak == 0

def test_dice_repr():
    dice = Dice()
    assert "Dice" in repr(dice)

