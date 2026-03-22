from crew import CrewManagementModule

class MissionPlanningModule:
    """Assigns side missions and validates required roles before allowing attempts."""
    
    def __init__(self, crew_module: CrewManagementModule):
        self.crew = crew_module
        self.available_missions = [
            {"name": "Midnight Delivery", "required_role": "Driver", "reward_cash": 500},
            {"name": "Garage Engine Swap", "required_role": "Mechanic", "reward_cash": 800},
            {"name": "Heist Route Planning", "required_role": "Strategist", "reward_cash": 1000}
        ]

    def get_missions(self):
        return self.available_missions

    def attempt_mission(self, mission_name: str, member_alias: str) -> bool:
        """Attempts a mission given an alias. Returns True if successful, False if invalid role."""
        
        mission = next((m for m in self.available_missions if m["name"] == mission_name), None)
        if not mission:
            raise ValueError(f"Mission '{mission_name}' does not exist.")
            
        member_role = self.crew.get_role(member_alias)
        
        # integration Check- validating required roles from crew module
        if member_role != mission["required_role"]:
            print(f"Mission Failed: {member_alias} is a {member_role}, but {mission['required_role']} is required!")
            return False
            
        print(f"Mission Success: {member_alias} completed {mission_name} and earned {mission['reward_cash']}!")
        # i will use the integration tests ahead to deposit this reward cash into inventory
        return True
