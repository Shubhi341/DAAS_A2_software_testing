from moneypoly.dice import Dice

def test_dice_roll_bounds():
    dice = Dice()
    seen_faces = set()
    
    # Roll 1000 times to statistically guarantee we see all possible faces
    for _ in range(1000):
        dice.roll()
        seen_faces.add(dice.die1)
        seen_faces.add(dice.die2)
        
        # Dice faces must be exactly between 1 and 6
        assert 1 <= dice.die1 <= 6
        assert 1 <= dice.die2 <= 6
        
    # A standard Monopoly die MUST physically be able to roll a 6!
    assert 6 in seen_faces, "Logical Error: The dice never rolled a 6!"

def test_dice_doubles_streak():
    dice = Dice()
    # Manually force the dice to match to test the boolean logic
    dice.die1 = 3
    dice.die2 = 3
    assert dice.is_doubles() is True
