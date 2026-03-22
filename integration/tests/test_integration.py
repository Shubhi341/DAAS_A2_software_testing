import pytest
import sys
import os

# Adding code directory to Python path so that pytest can find modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))

from registration import RegistrationModule
from crew import CrewManagementModule
from inventory import InventoryModule
from heat import PoliceHeatModule
from sponsor import SponsorshipModule
from race import RaceManagementModule
from mission import MissionPlanningModule
from results import ResultsModule

@pytest.fixture
def manager():
    """Sets up the StreetRace Manager ecosystem mapping inter-module dependencies."""
    class StreetRaceManager:
        def __init__(self):
            # initialize all modules and connecting them wherever is needed
            self.reg = RegistrationModule()
            self.crew = CrewManagementModule(self.reg)
            self.inv = InventoryModule()
            self.heat = PoliceHeatModule(self.inv)
            self.sponsor = SponsorshipModule(self.inv)
            self.race = RaceManagementModule(self.crew, self.inv)
            self.results = ResultsModule(self.race, self.inv)
            self.mission = MissionPlanningModule(self.crew)
            
    return StreetRaceManager()

def test_full_race_lifecycle_integration(manager):
    """Scenario 1: Testing Registration -> Crew -> Inventory -> Race -> Results pipeline."""
    # 1. registering and assigning a driver
    manager.reg.register_member("Dom", 35, "Toretto")
    manager.crew.assign_role("Toretto", "Driver")
    
    # 2. adding car and cash to inventory
    manager.inv.add_cash(1000)
    manager.inv.add_car("Dodge Charger")

    # 3. Schedule the race (Requires Driver, Car, and Entry Fee)
    assert manager.race.schedule_race("Midnight Run", entry_fee=200, prize=5000) is True
    assert manager.inv.cash == 800 # 1000 - 200 entry fee
    
    # 4. Run the race and get the result
    result = manager.results.resolve_race("Midnight Run", "Toretto")
    assert result["position"] in [1, 2, 3, 4]
    
    # 5. if the player wins, prize money added to inventory
    if result["position"] == 1:
        assert manager.inv.cash == 800 + 5000

def test_mission_validation_integration(manager):
    """Scenario 2: Testing Registration -> Crew -> Mission dependency path."""
    manager.reg.register_member("Brian", 28, "Buster")
    manager.reg.register_member("Tej", 32, "Tej")
    
    manager.crew.assign_role("Buster", "Driver")
    manager.crew.assign_role("Tej", "Mechanic")
    
    # if driver tries a Mechanic mission - should fail
    assert manager.mission.attempt_mission("Garage Engine Swap", "Buster") is False
    
    # tej(mechanic) does the Mechanic mission should succeed
    assert manager.mission.attempt_mission("Garage Engine Swap", "Tej") is True

def test_custom_modules_integration(manager):
    """Scenario 3: Testing Custom Modules (Heat & Sponsor) interacting with Inventory."""
    manager.inv.add_cash(200) # giving some starting cash
    
    # 1. heat rises to max - so racing should become unsafe
    manager.heat.add_heat(100)
    assert manager.heat.can_safely_race() is False
    
    # 2. try to pay bribe (Need 500, only have 200)
    assert manager.heat.pay_bribe(500) is False
    
    # 3. gain reputation and sign a sponsor
    manager.sponsor.add_reputation(20)
    assert manager.sponsor.sign_sponsor("Local Garage") is True
    
    # 4. apply sponsor bonus - adds money directly to inventory
    manager.sponsor.apply_sponsor_bonus()
    assert manager.inv.cash == 300 # 200 + 100
