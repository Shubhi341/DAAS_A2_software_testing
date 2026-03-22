from inventory import InventoryModule

class PoliceHeatModule:
    """Tracks illegal street racing heat and enforces police bribes."""
    
    def __init__(self, inventory_module: InventoryModule):
        self.inventory = inventory_module
        self.heat_level = 0
        self.MAX_HEAT = 100
        
    def add_heat(self, amount: int):
        """Increases heat after illegal activities (like racing)."""
        self.heat_level = min(self.heat_level + amount, self.MAX_HEAT)
        print(f"Heat level increased to {self.heat_level}/{self.MAX_HEAT}.")
        
    def can_safely_race(self) -> bool:
        """Returns False if heat is too high, meaning police are cracking down."""
        if self.heat_level >= 80:
            print("WARNING: Heat is too high! The police are heavily patrolling the streets. You cannot race until you pay a bribe.")
            return False
        return True
        
    def pay_bribe(self, bribe_amount: int = 500) -> bool:
        """Pays off the cops from the inventory cash to drastically reduce heat."""
        
        # Integration Check: Spends money directly from the Inventory
        if self.inventory.spend_cash(bribe_amount):
            self.heat_level = max(0, self.heat_level - 50) # Drop heat by 50 points
            print(f"Bribe of ${bribe_amount} paid successfully! Heat dropped to {self.heat_level}.")
            return True
        else:
            print(f"Insufficient funds! You need ${bribe_amount} to pay the police bribe.")
            return False
