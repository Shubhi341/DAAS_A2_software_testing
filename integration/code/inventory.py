class InventoryModule:
    """Manages cars, spare parts, and cash for the underground racing crew."""
    
    def __init__(self):
        self.cash = 0
        self.cars = []
        self.spare_parts = 0
        
    def add_cash(self, amount: int):
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        self.cash += amount
        
    def spend_cash(self, amount: int) -> bool:
        """Returns True if successfully spent, False if insufficient funds."""
        if amount > self.cash:
            return False
        self.cash -= amount
        return True
        
    def add_car(self, car_model: str):
        if not car_model:
            raise ValueError("Car model cannot be empty.")
        self.cars.append(car_model)
        
    def remove_car(self, car_model: str) -> bool:
        if car_model in self.cars:
            self.cars.remove(car_model)
            return True
        return False
        
    def add_parts(self, count: int):
        if count < 0:
            raise ValueError("Count cannot be negative.")
        self.spare_parts += count
        
    def use_parts(self, count: int) -> bool:
        """Returns True if parts were successfully used, False if not enough."""
        if count > self.spare_parts:
            return False
        self.spare_parts -= count
        return True
