class RegistrationModule:
    """Handles registering new crew members into the StreetRace network."""
    
    def __init__(self):
        # Database of registered members: { "alias": { "name": str, "age": int } }
        self.members = {}

    def register_member(self, name: str, age: int, alias: str) -> bool:
        """Registers a new member into the system. Returns True if successful."""
        if not name or not alias:
            raise ValueError("Name and Alias cannot be empty.")
        if age < 18:
            raise ValueError("Members must be at least 18 years old to join the underground.")
        
        if alias in self.members:
            return False # Alias is already taken
            
        self.members[alias] = {
            "name": name,
            "age": age
        }
        return True

    def get_member(self, alias: str) -> dict:
        """Retrieves member details by alias, or None if not found."""
        return self.members.get(alias)

    def is_registered(self, alias: str) -> bool:
        """Checks if a specific alias is already registered."""
        return alias in self.members
