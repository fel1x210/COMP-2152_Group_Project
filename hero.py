import random
from character import Character

class Hero(Character):
    def __init__(self):
        # Explicitly call parent constructor with random values
        super().__init__(
            combat_strength=random.choice(range(1, 7)),
            health_points=random.choice(range(1, 21))
        )

    def __del__(self):
        # First print Hero-specific message
        print("The Hero object is being destroyed by the garbage collector")
        # Call parent destructor
        super().__del__()

    def hero_attacks(self, m_health_points):
        print("    |    Player's weapon (" + str(self.combat_strength) + ") ---> Monster (" + str(m_health_points) + ")")
        if self.combat_strength >= m_health_points:
            m_health_points = 0
            print("    |    You have killed the monster")
        else:
            m_health_points -= self.combat_strength
            print("    |    You have reduced the monster's health to: " + str(m_health_points))
        return m_health_points
