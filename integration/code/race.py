from crew import CrewManagementModule
from inventory import InventoryModule

class RaceManagementModule:
    """Handles scheduling of races and verifying player requirements."""
    
    def __init__(self, crew_module: CrewManagementModule, inventory_module: InventoryModule):
        self.crew = crew_module
        self.inventory = inventory_module
        self.races = []

    def schedule_race(self, race_name: str, entry_fee: int, prize: int) -> bool:
        """Schedules a new race if the player meets all requirements."""
        
        # 1.integration check- must have a driver on crew
        if not self.crew.get_all_by_role("Driver"):
            print(f"Cannot schedule {race_name}: No Driver available in crew.")
            return False
            
        # 2.integration check- must have at least one car
        if not self.inventory.cars:
            print(f"Cannot schedule {race_name}: No cars available in inventory.")
            return False
            
        # 3.integration check- must be able to afford the entry fee
        if self.inventory.cash < entry_fee:
            print(f"Cannot schedule {race_name}: Insufficient funds for entry fee.")
            return False
            
        # all requirements met- deduct fee and formally schedule the race
        self.inventory.spend_cash(entry_fee)
        
        self.races.append({
            "name": race_name,
            "prize": prize,
            "status": "scheduled"
        })
        return True

    def get_scheduled_races(self) -> list:
        return [r for r in self.races if r["status"] == "scheduled"]
