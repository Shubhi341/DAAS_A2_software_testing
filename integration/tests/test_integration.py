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
    manager.reg.register_member("Dom", 35, "Toretto")
    manager.crew.assign_role("Toretto", "Driver")
    
    # cross-module validation
    assert manager.reg.is_registered("Toretto") is True
    assert manager.crew.get_role("Toretto") == "Driver"
    
    manager.inv.add_cash(1000)
    manager.inv.add_car("Dodge Charger")

    assert manager.race.schedule_race("Midnight Run", entry_fee=200, prize=5000) is True
    assert manager.inv.cash == 800 
    
    result = manager.results.resolve_race("Midnight Run", "Toretto")
    assert result["position"] in [1, 2, 3, 4]
    
    if result["position"] == 1:
        assert manager.inv.cash == 800 + 5000

def test_race_without_registration(manager):
    """Missing Case 1: unregistered driver in race"""
    manager.inv.add_cash(500)
    manager.inv.add_car("Supra")
    
    # No driver registered in the Crew module!
    assert manager.race.schedule_race("Illegal Run", 100, 1000) is False

def test_race_without_car(manager):
    """Missing Case 2: race without car"""
    manager.reg.register_member("Brian", 28, "Buster")
    manager.crew.assign_role("Buster", "Driver")
    manager.inv.add_cash(500)
    
    # driver exists, cash exists, but explicitly no car in inventory
    assert manager.race.schedule_race("Sprint", 100, 1000) is False

def test_mission_validation_integration(manager):
    """Scenario 2 & Missing Case 3: Testing Registration -> Crew -> Mission dependency path."""
    manager.reg.register_member("Brian", 28, "Buster")
    manager.reg.register_member("Tej", 32, "Tej")
    
    manager.crew.assign_role("Buster", "Driver")
    manager.crew.assign_role("Tej", "Mechanic")
    
    # cross-module validation
    assert "Tej" in manager.crew.role_assignments
    
    # driver tries a mechanic mission - should fail
    assert manager.mission.attempt_mission("Garage Engine Swap", "Buster") is False
    
    # mechanic does the mechanic mission - should succeed
    assert manager.mission.attempt_mission("Garage Engine Swap", "Tej") is True

def test_results_without_race(manager):
    """Missing Case 4: results without race"""
    # attempting to resolve a race that was never scheduled in race module
    with pytest.raises(ValueError, match="is not scheduled."):
        manager.results.resolve_race("Fake Race", "Nobody")

def test_custom_modules_integration(manager):
    """Scenario 3: Testing Custom Modules (Heat & Sponsor) interacting with Inventory."""
    manager.inv.add_cash(200) 
    
    manager.heat.add_heat(100)
    assert manager.heat.can_safely_race() is False
    
    assert manager.heat.pay_bribe(500) is False
    
    manager.sponsor.add_reputation(20)
    assert manager.sponsor.sign_sponsor("Local Garage") is True
    
    manager.sponsor.apply_sponsor_bonus()
    assert manager.inv.cash == 300 
