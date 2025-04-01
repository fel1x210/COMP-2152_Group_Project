import random
from character import Character


class Monster(Character):
    def __init__(self):
        # Explicitly call parent constructor with random values
        super().__init__(
            combat_strength=random.randint(1, 12),
            health_points=random.randint(1, 20)
        )
        spell_type = ["Fire", "Ice", "Lightning", "Earth", "Water"]
        self.__spell_weakness = random.choice(spell_type)
        spell_type.remove(self.__spell_weakness)
        self.__spell_resistance = random.choice(spell_type)
        spell_type.remove(self.__spell_resistance)
        print(f"A monster appears with {self.m_combat_strength} combat strength and {self.m_health_points} health points! It is weak against {self.__spell_weakness} spells and resistant to {self.__spell_resistance} spells!")
    
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

    @property
    def spell_weakness(self):
        return self.__spell_weakness
    @spell_weakness.setter
    def spell_weakness(self, value):
        self.__spell_weakness = value

    @property
    def spell_resistance(self):
        return self.__spell_resistance
    
    @spell_resistance.setter
    def spell_resistance(self, value):
        self.__spell_resistance = value
    
    def monster_attacks(self):
        # Return the combat strength as the attack value
        attack_value = self.combat_strength
        print(f"The monster attacks with {attack_value} strength!")
        return attack_value