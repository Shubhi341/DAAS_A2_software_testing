from registration import RegistrationModule

class CrewManagementModule:
    """Assigns and manages roles (Driver, Mechanic, Strategist) for registered members."""
    
    VALID_ROLES = ["Driver", "Mechanic", "Strategist"]

    def __init__(self, registration_module: RegistrationModule):
        # We need the registration module to verify people exist before hiring them!
        self.registration = registration_module
        
        # Dictionary tracking jobs: { "alias": "Role" }
        self.role_assignments = {}

    def assign_role(self, alias: str, role: str) -> bool:
        """Assigns a role to a registered member. Returns True if successful."""
        if not self.registration.is_registered(alias):
            raise ValueError(f"Cannot assign role: {alias} is not a registered member.")
            
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'. Must be one of: {', '.join(self.VALID_ROLES)}")
            
        self.role_assignments[alias] = role
        return True

    def get_role(self, alias: str) -> str:
        """Returns the role of the member, or None if no role is assigned."""
        return self.role_assignments.get(alias)

    def get_all_by_role(self, role: str) -> list:
        """Returns a list of aliases that have the specified role."""
        return [
            alias for alias, assigned_role in self.role_assignments.items() 
            if assigned_role == role
        ]
