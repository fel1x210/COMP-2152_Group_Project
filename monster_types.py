import random
from monster import Monster
from functions import print_header, print_section, print_game_text, print_important

# Base class for different monster types
class TypedMonster(Monster):
    def __init__(self, monster_type="Base"):
        super().__init__()
        self.score = 1
        self.monster_type = monster_type
        self.strengths = []  # what weapons this monster type is strong against
        self.weaknesses = [] # what weapons this monster type is weak against
        self.environments = []  # environments where this monster gets bonuses
        self.adaptive = False  # whether monster adapts to attacks
        self.secondary_attributes = {}  # additional monster attributes

        # Initialize secondary attributes at the end of initialization
        self._initialize_secondary_attributes()

    def get_score(self, player_health):
        """Calculate score based on monster type and player's health"""
        base_score = self.score  # Each monster type has a predefined score
        health_factor = max(1, 20 - player_health)  # Players with lower health get more points
        return base_score * health_factor

    def _initialize_secondary_attributes(self):
        """Initialize random secondary attributes"""
        # Base implementation - overridden by subclasses
        pass

    # Method to apply type-based damage modifier
    def calculate_damage_modifier(self, weapon_type):
        # Apply weakness (take more damage)
        if weapon_type in self.weaknesses:
            return 1.5  # 50% more damage
        # Apply strength (take less damage)
        elif weapon_type in self.strengths:
            return 0.5  # 50% less damage
        # No modifier
        return 1.0

    def environment_bonus(self, environment):
        """Calculate environment-based bonus"""
        if environment in self.environments:
            return 2  # +2 to combat strength in favorable environment
        return 0

    def adapt_to_attack(self, weapon_type):
        """Adapt to repeated attacks of the same type"""
        if self.adaptive and weapon_type in self.weaknesses:
            # Remove from weaknesses after being hit
            self.weaknesses.remove(weapon_type)
            print_important(f"The {self.monster_type} adapts to {weapon_type} attacks!")
            return True
        return False

    def special_ability(self):
        """Use monster's special ability based on type"""
        # Base implementation returns combat value modifier
        return 0

    def get_description(self):
        """Get a description of the monster"""
        desc = f"A {self.monster_type} with {self.combat_strength} combat strength and {self.health_points} health."
        if self.strengths:
            desc += f" Resistant to {', '.join(self.strengths)}."
        if self.weaknesses:
            desc += f" Vulnerable to {', '.join(self.weaknesses)}."
        if self.environments:
            desc += f" Thrives in {', '.join(self.environments)} environments."
        if self.adaptive:
            desc += f" Can adapt to repeated attacks."
        return desc

# Specific monster type implementations
class ElementalMonster(TypedMonster):
    def __init__(self, element_type=None):
        # game score value
        self.score = 25
        # List of possible elemental types
        elements = ["Fire", "Water", "Earth", "Air"]
        # Select random element if none provided
        self.element = element_type if element_type else random.choice(elements)

        # Call parent constructor with the proper monster type name
        super().__init__(f"{self.element} Elemental")

        # Set adaptive behavior for elementals
        self.adaptive = random.choice([True, False])

        # Define strengths and weaknesses based on element type
        if self.element == "Fire":
            self.strengths = ["Club", "Fist"]
            self.weaknesses = ["Bomb", "Nuclear Bomb"]
            self.environments = ["Forest", "Desert"]
        elif self.element == "Water":
            self.strengths = ["Bomb", "Gun"]
            self.weaknesses = ["Club", "Knife"]
            self.environments = ["Lake", "Cave"]
        elif self.element == "Earth":
            self.strengths = ["Knife", "Gun"]
            self.weaknesses = ["Fist", "Nuclear Bomb"]
            self.environments = ["Mountain", "Forest"]
        elif self.element == "Air":
            self.strengths = ["Nuclear Bomb", "Fist"]
            self.weaknesses = ["Gun", "Knife"]
            self.environments = ["Mountain", "Plains"]

        # Initialize secondary attributes after setting the element
        self._initialize_secondary_attributes()

    def _initialize_secondary_attributes(self):
        """Initialize elemental-specific attributes"""
        if self.element == "Fire":
            self.secondary_attributes["burn_damage"] = random.randint(1, 3)
        elif self.element == "Water":
            self.secondary_attributes["slow_effect"] = random.randint(1, 2)
        elif self.element == "Earth":
            self.secondary_attributes["armor"] = random.randint(1, 3)
        elif self.element == "Air":
            self.secondary_attributes["evasion"] = random.randint(10, 30)

    def special_ability(self):
        """Elemental special ability"""
        ability_power = 0
        if self.element == "Fire" and "burn_damage" in self.secondary_attributes:
            ability_power = self.secondary_attributes["burn_damage"]
            print_game_text(f"The {self.monster_type} burns you for {ability_power} damage!")
        elif self.element == "Water" and "slow_effect" in self.secondary_attributes:
            ability_power = self.secondary_attributes["slow_effect"]
            print_game_text(f"The {self.monster_type} slows you, reducing your combat strength by {ability_power}!")
        elif self.element == "Earth" and "armor" in self.secondary_attributes:
            ability_power = -self.secondary_attributes["armor"]  # negative because it reduces damage
            print_game_text(f"The {self.monster_type} hardens its skin, reducing damage by {-ability_power}!")
        elif self.element == "Air" and "evasion" in self.secondary_attributes:
            if random.randint(1, 100) <= self.secondary_attributes["evasion"]:
                ability_power = -999  # special value to indicate complete evasion
                print_important(f"The {self.monster_type} dodges your attack completely!")
        return ability_power

class UndeadMonster(TypedMonster):
    def __init__(self, undead_type=None):
        # game score value
        self.score = 20
        # List of possible undead types
        undead_types = ["Zombie", "Skeleton", "Ghost", "Vampire"]
        # Select random undead type if none provided
        self.undead_type = undead_type if undead_type else random.choice(undead_types)

        # Call parent constructor
        super().__init__(f"{self.undead_type}")

        # Set adaptive for some undead types
        self.adaptive = self.undead_type in ["Vampire", "Ghost"]

        # Define strengths and weaknesses based on undead type
        if self.undead_type == "Zombie":
            self.strengths = ["Fist", "Knife"]
            self.weaknesses = ["Bomb", "Club"]
            self.environments = ["Graveyard", "Ruins"]
        elif self.undead_type == "Skeleton":
            self.strengths = ["Gun", "Bomb"]
            self.weaknesses = ["Club", "Fist"]
            self.environments = ["Dungeon", "Crypt"]
        elif self.undead_type == "Ghost":
            self.strengths = ["Club", "Knife", "Fist"]
            self.weaknesses = ["Nuclear Bomb"]
            self.environments = ["Ruins", "Mansion"]
        elif self.undead_type == "Vampire":
            self.strengths = ["Gun", "Bomb"]
            self.weaknesses = ["Knife"]
            self.environments = ["Castle", "Cave"]

        # Initialize secondary attributes
        self._initialize_secondary_attributes()

    def _initialize_secondary_attributes(self):
        """Initialize undead-specific attributes"""
        if self.undead_type == "Zombie":
            self.secondary_attributes["infection_chance"] = random.randint(10, 30)
        elif self.undead_type == "Skeleton":
            self.secondary_attributes["bone_armor"] = random.randint(1, 2)
        elif self.undead_type == "Ghost":
            self.secondary_attributes["phase_chance"] = random.randint(20, 40)
        elif self.undead_type == "Vampire":
            self.secondary_attributes["life_drain"] = random.randint(1, 3)

    def special_ability(self):
        """Undead special ability"""
        ability_power = 0
        if self.undead_type == "Zombie" and "infection_chance" in self.secondary_attributes:
            if random.randint(1, 100) <= self.secondary_attributes["infection_chance"]:
                ability_power = 2
                print_game_text(f"The {self.monster_type} infects you, causing {ability_power} damage!")
        elif self.undead_type == "Skeleton" and "bone_armor" in self.secondary_attributes:
            ability_power = -self.secondary_attributes["bone_armor"]
            print_game_text(f"The {self.monster_type}'s bone armor reduces damage by {-ability_power}!")
        elif self.undead_type == "Ghost" and "phase_chance" in self.secondary_attributes:
            if random.randint(1, 100) <= self.secondary_attributes["phase_chance"]:
                ability_power = -999  # special value for complete dodge
                print_important(f"The {self.monster_type} phases through your attack!")
        elif self.undead_type == "Vampire" and "life_drain" in self.secondary_attributes:
            ability_power = self.secondary_attributes["life_drain"]
            print_game_text(f"The {self.monster_type} drains your life force for {ability_power} damage and heals itself!")
            # Heal the vampire
            self.health_points = min(20, self.health_points + ability_power)
        return ability_power

class MechanicalMonster(TypedMonster):
    def __init__(self, mech_type=None):
        # game score value
        self.score = 30
        # List of possible mechanical types
        mech_types = ["Robot", "Golem", "Automaton", "Drone"]
        # Select random mechanical type if none provided
        self.mech_type = mech_type if mech_type else random.choice(mech_types)

        # Call parent constructor
        super().__init__(f"{self.mech_type}")

        # Mechanical types are not adaptive by default
        self.adaptive = False

        # Define strengths and weaknesses based on mechanical type
        if self.mech_type == "Robot":
            self.strengths = ["Fist", "Club"]
            self.weaknesses = ["Bomb", "Nuclear Bomb"]
            self.environments = ["Laboratory", "Factory"]
        elif self.mech_type == "Golem":
            self.strengths = ["Knife", "Gun"]
            self.weaknesses = ["Nuclear Bomb"]
            self.environments = ["Cave", "Ruins"]
        elif self.mech_type == "Automaton":
            self.strengths = ["Knife", "Fist"]
            self.weaknesses = ["Club", "Bomb"]
            self.environments = ["Castle", "Factory"]
        elif self.mech_type == "Drone":
            self.strengths = ["Club", "Fist"]
            self.weaknesses = ["Gun", "Nuclear Bomb"]
            self.environments = ["Laboratory", "Plains"]

        # Initialize secondary attributes
        self._initialize_secondary_attributes()

    def _initialize_secondary_attributes(self):
        """Initialize mechanical-specific attributes"""
        if self.mech_type == "Robot":
            self.secondary_attributes["targeting_system"] = random.randint(1, 3)
        elif self.mech_type == "Golem":
            self.secondary_attributes["stone_body"] = random.randint(2, 4)
        elif self.mech_type == "Automaton":
            self.secondary_attributes["clockwork_precision"] = random.randint(1, 3)
        elif self.mech_type == "Drone":
            self.secondary_attributes["evasion"] = random.randint(20, 40)

    def special_ability(self):
        """Mechanical special ability"""
        ability_power = 0
        if self.mech_type == "Robot" and "targeting_system" in self.secondary_attributes:
            ability_power = self.secondary_attributes["targeting_system"]
            print_game_text(f"The {self.monster_type}'s targeting system deals {ability_power} precise damage!")
        elif self.mech_type == "Golem" and "stone_body" in self.secondary_attributes:
            ability_power = -self.secondary_attributes["stone_body"]
            print_game_text(f"The {self.monster_type}'s stone body reduces damage by {-ability_power}!")
        elif self.mech_type == "Automaton" and "clockwork_precision" in self.secondary_attributes:
            ability_power = self.secondary_attributes["clockwork_precision"]
            print_game_text(f"The {self.monster_type}'s clockwork precision deals {ability_power} extra damage!")
        elif self.mech_type == "Drone" and "evasion" in self.secondary_attributes:
            if random.randint(1, 100) <= self.secondary_attributes["evasion"]:
                ability_power = -999  # special value for complete dodge
                print_important(f"The {self.monster_type} quickly flies out of the way of your attack!")
        return ability_power

# New Mythical monster type with unique abilities
class MythicalMonster(TypedMonster):
    def __init__(self, mythical_type=None):
        # game score value
        self.score = 50
        # List of possible mythical types
        mythical_types = ["Dragon", "Phoenix", "Minotaur", "Hydra"]
        # Select random mythical type if none provided
        self.mythical_type = mythical_type if mythical_type else random.choice(mythical_types)

        # Call parent constructor
        super().__init__(f"{self.mythical_type}")

        # Mythical monsters are highly adaptive
        self.adaptive = True

        # Define strengths and weaknesses based on mythical type
        if self.mythical_type == "Dragon":
            self.strengths = ["Knife", "Fist", "Club"]
            self.weaknesses = ["Nuclear Bomb"]
            self.environments = ["Mountain", "Cave"]
        elif self.mythical_type == "Phoenix":
            self.strengths = ["Bomb", "Nuclear Bomb"]
            self.weaknesses = ["Gun"]
            self.environments = ["Desert", "Mountain"]
        elif self.mythical_type == "Minotaur":
            self.strengths = ["Gun", "Bomb"]
            self.weaknesses = ["Club"]
            self.environments = ["Labyrinth", "Ruins"]
        elif self.mythical_type == "Hydra":
            self.strengths = ["Knife", "Fist"]
            self.weaknesses = ["Bomb", "Nuclear Bomb"]
            self.environments = ["Swamp", "Lake"]

        # Initialize secondary attributes
        self._initialize_secondary_attributes()

    def _initialize_secondary_attributes(self):
        """Initialize mythical-specific attributes"""
        if self.mythical_type == "Dragon":
            self.secondary_attributes["breath_attack"] = random.randint(3, 5)
        elif self.mythical_type == "Phoenix":
            self.secondary_attributes["rebirth_chance"] = random.randint(20, 40)
        elif self.mythical_type == "Minotaur":
            self.secondary_attributes["charge_damage"] = random.randint(2, 4)
        elif self.mythical_type == "Hydra":
            self.secondary_attributes["multiple_heads"] = random.randint(2, 4)

    def special_ability(self):
        """Mythical monster special ability"""
        ability_power = 0
        if self.mythical_type == "Dragon" and "breath_attack" in self.secondary_attributes:
            ability_power = self.secondary_attributes["breath_attack"]
            print_important(f"The {self.monster_type} breathes fire, dealing {ability_power} massive damage!")
        elif self.mythical_type == "Phoenix" and "rebirth_chance" in self.secondary_attributes:
            if self.health_points < 5 and random.randint(1, 100) <= self.secondary_attributes["rebirth_chance"]:
                self.health_points = 10
                print_important(f"The {self.monster_type} bursts into flames and is reborn with 10 health!")
        elif self.mythical_type == "Minotaur" and "charge_damage" in self.secondary_attributes:
            ability_power = self.secondary_attributes["charge_damage"]
            print_game_text(f"The {self.monster_type} charges at you, dealing {ability_power} damage!")
        elif self.mythical_type == "Hydra" and "multiple_heads" in self.secondary_attributes:
            heads = self.secondary_attributes["multiple_heads"]
            ability_power = heads
            print_important(f"The {self.monster_type}'s {heads} heads attack simultaneously for {ability_power} damage!")
        return ability_power

# Generator function that uses list comprehension to create monsters
def generate_monster_types(environment=None):
    # Define all possible monster categories
    monster_categories = ["Elemental", "Undead", "Mechanical", "Mythical"]

    # Adjust probabilities based on environment
    if environment:
        # Create adjusted weights based on environment
        weights = [
            3 if environment in ["Forest", "Desert", "Mountain", "Lake", "Cave", "Plains"] else 1,  # Elemental
            3 if environment in ["Graveyard", "Dungeon", "Ruins", "Crypt", "Castle", "Mansion"] else 1,  # Undead
            3 if environment in ["Laboratory", "Factory", "Castle"] else 1,  # Mechanical
            1  # Mythical (always rare)
        ]

        # Use weighted choice
        category = random.choices(monster_categories, weights=weights, k=1)[0]

        # Use list comprehension with nested conditionals to create the appropriate monster
        monster = (
            ElementalMonster() if category == "Elemental"
            else UndeadMonster() if category == "Undead"
            else MechanicalMonster() if category == "Mechanical"
            else MythicalMonster() if category == "Mythical"
            else TypedMonster()
        )

        # Apply environment bonus if applicable
        if environment in monster.environments:
            monster.combat_strength += 2
            print_game_text(f"The {monster.monster_type} is stronger in this {environment} environment!")

        return monster
    else:
        # Use list comprehension to generate a list of possible monster types
        monster_types = [
            ElementalMonster() if category == "Elemental"
            else UndeadMonster() if category == "Undead"
            else MechanicalMonster() if category == "Mechanical"
            else MythicalMonster() if category == "Mythical"
            else TypedMonster()
            for category in monster_categories
        ]

        # Randomly select a monster type from the generated list
        return random.choice(monster_types)

# Function to get a list of all possible environments
def get_all_environments():
    # Use list comprehension to extract environments from monster types
    elemental_environments = ["Forest", "Desert", "Mountain", "Lake", "Cave", "Plains"]
    undead_environments = ["Graveyard", "Dungeon", "Ruins", "Crypt", "Castle", "Mansion"]
    mechanical_environments = ["Laboratory", "Factory", "Castle"]
    mythical_environments = ["Mountain", "Cave", "Desert", "Labyrinth", "Swamp", "Lake"]

    # Combine all environments and remove duplicates using set comprehension
    all_environments = list({env for envs in [elemental_environments, undead_environments, mechanical_environments, mythical_environments] for env in envs})

    return all_environments