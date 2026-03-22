from inventory import InventoryModule

class SponsorshipModule:
    """Manages brand sponsorships that provide passive cash bonuses after races."""
    
    def __init__(self, inventory_module: InventoryModule):
        self.inventory = inventory_module
        self.reputation_points = 0
        self.active_sponsor = None
        
        self.AVAILABLE_SPONSORS = {
            "Local Garage": {"req_rep": 10, "bonus_cash": 100},
            "Tuner Mag": {"req_rep": 50, "bonus_cash": 300},
            "Energy Drink Co": {"req_rep": 100, "bonus_cash": 1000}
        }
        
    def add_reputation(self, amount: int):
        self.reputation_points += amount
        print(f"Reputation increased! Current Rep: {self.reputation_points}")
        
    def sign_sponsor(self, sponsor_name: str) -> bool:
        """Attempts to sign a sponsor based on current reputation."""
        sponsor = self.AVAILABLE_SPONSORS.get(sponsor_name)
        
        if not sponsor:
            raise ValueError(f"Sponsor '{sponsor_name}' does not exist.")
            
        if self.reputation_points >= sponsor["req_rep"]:
            self.active_sponsor = sponsor_name
            print(f"Successfully signed with {sponsor_name}!")
            return True
        else:
            print(f"Not enough reputation for {sponsor_name}. Need {sponsor['req_rep']}.")
            return False
            
    def apply_sponsor_bonus(self):
        """Deposits bonus cash into the inventory if a sponsor is active."""
        if self.active_sponsor:
            bonus = self.AVAILABLE_SPONSORS[self.active_sponsor]["bonus_cash"]
            
            # Integration Check: Deposits passive bonus cash directly into Inventory!
            self.inventory.add_cash(bonus)
            print(f"Sponsor {self.active_sponsor} paid a bonus of ${bonus}!")
            return bonus
        return 0
