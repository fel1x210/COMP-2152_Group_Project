import random
from character import Character

class Monster(Character):
    def __init__(self):
        # Explicitly call parent constructor with random values
        super().__init__(
            combat_strength=random.randint(1, 12),
            health_points=random.randint(1, 20)
        )
        print(f"A monster appears with {self.m_combat_strength} combat strength and {self.m_health_points} health points!")
    
    def __del__(self):
        # First print Monster-specific message
        print("The Monster object is being destroyed by the garbage collector")
        # Call parent destructor
        super().__del__()
    
    # Property aliases for backward compatibility
    @property
    def m_combat_strength(self):
        return self.combat_strength
    
    @m_combat_strength.setter
    def m_combat_strength(self, value):
        self.combat_strength = value
    
    @property
    def m_health_points(self):
        return self.health_points
    
    @m_health_points.setter
    def m_health_points(self, value):
        self.health_points = value
    
    def monster_attacks(self):
        # Return the combat strength as the attack value
        attack_value = self.combat_strength
        print(f"The monster attacks with {attack_value} strength!")
        return attack_value