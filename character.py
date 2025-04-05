class Character:
    def __init__(self, combat_strength=1, health_points=1):
        # Initialize private properties
        self._combat_strength = combat_strength
        self._health_points = health_points
    
    def __del__(self):
        # Base destructor
        print("Character resources released")
    
    @property
    def combat_strength(self):
        return self._combat_strength
    
    @combat_strength.setter
    def combat_strength(self, value):
        if value < 0:
            print("Combat strength cannot be negative, setting to 0")
            self._combat_strength = 0
        else:
            self._combat_strength = value
    
    @property
    def health_points(self):
        return self._health_points
    
    @health_points.setter
    def health_points(self, value):
        if value < 0:
            self._health_points = 0
        else:
            self._health_points = value
