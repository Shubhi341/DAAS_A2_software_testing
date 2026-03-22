import random
from race import RaceManagementModule
from inventory import InventoryModule

class ResultsModule:
    """Calculates race outcomes, records times, and updates rankings."""
    
    def __init__(self, race_module: RaceManagementModule, inventory_module: InventoryModule):
        self.race_module = race_module
        self.inventory = inventory_module
        self.race_history = []
        self.rankings = {}

    def resolve_race(self, race_name: str, driver_alias: str):
        """Simulates the race outcome."""
        
        # it ensure race actually exists and is scheduled
        scheduled_races = self.race_module.get_scheduled_races()
        race = next((r for r in scheduled_races if r["name"] == race_name), None)
        
        if not race:
            raise ValueError(f"Race '{race_name}' is not scheduled.")
            
        # it simulate race time and finish position
        time_seconds = random.randint(120, 300) 
        position = random.randint(1, 4) 
        
        # it calculates prize (1st place gets full, 2nd gets half)
        won_prize = 0
        if position == 1:
            won_prize = race["prize"]
        elif position == 2:
            won_prize = race["prize"] // 2
            
        race["status"] = "completed"
        
        # integration check- provide prize money directly to inventory
        if won_prize > 0:
            self.inventory.add_cash(won_prize)
            
        result = {
            "race_name": race_name,
            "driver": driver_alias,
            "position": position,
            "time_seconds": time_seconds,
            "prize_won": won_prize
        }
        self.race_history.append(result)
        
        # this updates leaderboard rankings
        points = {1: 10, 2: 5, 3: 2}.get(position, 0)
        self.rankings[driver_alias] = self.rankings.get(driver_alias, 0) + points
        
        return result

    def get_leaderboard(self):
        """Returns drivers sorted by ranking points."""
        return sorted(self.rankings.items(), key=lambda x: x[1], reverse=True)
