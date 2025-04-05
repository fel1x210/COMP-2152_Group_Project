# Import the random library to use for the dice later
import random

# Define UI formatting helpers
def print_header(title):
    """Print a consistent header with a title"""
    print("\n" + "="*70)
    print(f"    {title}")
    print("="*70)

def print_section(title):
    """Print a section divider with title"""
    print("\n" + "-"*70)
    print(f"    {title}")
    print("-"*70)

def print_game_text(text):
    """Print game text with consistent indentation"""
    print(f"    | {text}")

def print_important(text):
    """Print important information with emphasis"""
    print(f"\n    | >>> {text} <<<\n")

# Will the line below print when you import function.py into main.py?
# print("Inside function.py")
spells = ["Fire", "Ice", "Lightning", "Earth", "Water", "None"]



def use_loot(belt, hero):
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]

    print_section("Using Items")
    print_game_text("You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0)
    if first_item in good_loot_options:
        hero.health_points = min(20, (hero.health_points + 2))
        print_game_text(f"You used {first_item} to up your health to {hero.health_points}")
    elif first_item in bad_loot_options:
        hero.health_points = max(0, (hero.health_points - 2))
        print_game_text(f"You used {first_item} to hurt your health to {hero.health_points}")
    else:
        print_game_text(f"You used {first_item} but it's not helpful")
    return belt, hero.health_points


def collect_loot(loot_options, belt):
    ascii_image3 = """
                      @@@ @@                
             *# ,        @              
           @           @                
                @@@@@@@@                
               @   @ @% @*              
            @     @   ,    &@           
          @                   @         
         @                     @        
        @                       @       
        @                       @       
        @*                     @        
          @                  @@         
              @@@@@@@@@@@@          
              """
    print(ascii_image3)
    loot_roll = random.choice(range(1, len(loot_options) + 1))
    loot = loot_options.pop(loot_roll - 1)
    belt.append(loot)
    print_game_text(f"You found: {loot}")
    print_game_text(f"Your belt: {belt}")
    return loot_options, belt


# Hero's Attack Function
def hero_attacks(hero, monster):
    ascii_image = """
                                @@   @@ 
                                @    @  
                                @   @   
               @@@@@@          @@  @    
            @@       @@        @ @@     
           @%         @     @@@ @       
            @        @@     @@@@@     
               @@@@@        @@       
               @    @@@@                
          @@@ @@                        
       @@     @                         
   @@*       @                          
   @        @@                          
           @@                                                    
         @   @@@@@@@                    
        @            @                  
      @              @                  

  """
    print("\n" + ascii_image)
    
    # Roll for spell cast
    print_section("Hero Attack")
    spell_roll = random.choice(spells)
    if spell_roll == "None":
        print_game_text("The hero used a normal attack.")
    else:
        print_important(f"Hero casted a {spell_roll} spell!")
    
    # Check if spell casted is strong or weak against monster
    spell_dmg_amp = False
    spell_dmg_damp = False
    
    if hasattr(monster, 'spell_weakness') and hasattr(monster, 'spell_resistance'):
        spell_dmg_amp = (spell_roll == monster.spell_weakness)
        spell_dmg_damp = (spell_roll == monster.spell_resistance)
    
    # Get the current weapon based on combat strength
    weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
    current_weapon = weapons[min(5, hero.combat_strength - 1)]
    
    # Check if the monster has type-based damage modifiers
    damage_modifier = 1.0
    if hasattr(monster, 'calculate_damage_modifier'):
        damage_modifier = monster.calculate_damage_modifier(current_weapon)
    
    # Apply spell effects to hero's combat strength
    combat_strength = hero.combat_strength
    if spell_dmg_amp:
        combat_strength += combat_strength/2
        print_important("Spell casted is effective against monster! Damage amplified by 50%!")
    elif spell_dmg_damp:
        combat_strength -= combat_strength/2
        print_important("Spell casted is not effective against monster! Damage reduced by 50%!")
    else:
        print_game_text("No damage change from spell effects.")
    
    # Calculate actual damage based on hero's combat strength, type modifiers, and spell effects
    actual_damage = int(combat_strength * damage_modifier)
    
    print_game_text(f"Player's weapon {current_weapon} ({actual_damage} damage) ---> Monster ({monster.health_points} HP)")
    
    # Check for monster's ability to dodge/reduce damage with special ability
    ability_effect = 0
    if hasattr(monster, 'special_ability'):
        ability_effect = monster.special_ability()
        
        # Handle complete dodge
        if ability_effect == -999:
            print_important("Your attack misses completely!")
            return monster.health_points
        
        # Apply damage reduction (negative ability effects reduce damage)
        if ability_effect < 0:
            actual_damage = max(1, actual_damage + ability_effect)  # Ensure at least 1 damage
    
    # Display type modifier information if applicable
    if hasattr(monster, 'monster_type'):
        print_game_text(f"Monster type: {monster.monster_type}")
        if damage_modifier > 1.0:
            print_important(f"{current_weapon} is EFFECTIVE against {monster.monster_type}! Damage increased to {actual_damage}!")
        elif damage_modifier < 1.0:
            print_important(f"{current_weapon} is WEAK against {monster.monster_type}! Damage reduced to {actual_damage}!")
    
    # Check if monster adapts to the attack
    if hasattr(monster, 'adapt_to_attack'):
        monster.adapt_to_attack(current_weapon)
    
    # Apply damage
    if actual_damage >= monster.health_points:
        # Player was strong enough to kill monster in one blow
        monster.health_points = 0
        print_important("You have killed the monster!")
    else:
        # Player only damaged the monster
        monster.health_points -= actual_damage
        print_game_text(f"You have reduced the monster's health to: {monster.health_points}")
        
        # Check for Phoenix rebirth ability
        if hasattr(monster, 'mythical_type') and monster.mythical_type == "Phoenix":
            if monster.health_points < 5 and "rebirth_chance" in monster.secondary_attributes:
                if random.randint(1, 100) <= monster.secondary_attributes["rebirth_chance"]:
                    monster.health_points = 10
                    print_important("The Phoenix bursts into flames and is reborn with 10 health!")
    
    return monster.health_points


# Monster's Attack Function
def monster_attacks(monster, hero):
    ascii_image2 = """                                                                 
           @@@@ @                           
      (     @*&@  ,                         
    @               %                       
     &#(@(@%@@@@@*   /                      
      @@@@@.                                
               @       /                    
                %         @                 
            ,(@(*/           %              
               @ (  .@#                 @   
                          @           .@@. @
                   @         ,              
                      @       @ .@          
                             @              
                          *(*  *      
             """
    print("\n" + ascii_image2)
    
    # Calculate base attack damage
    attack_value = monster.combat_strength
    
    # Add bonus from special ability if available
    ability_bonus = 0
    print_section("Monster Attack")
    if hasattr(monster, 'special_ability') and random.random() < 0.5:  # 50% chance to use special ability
        ability_bonus = monster.special_ability()
        if ability_bonus > 0:  # Only apply positive values (negative values are defensive)
            attack_value += ability_bonus
    
    print_game_text(f"Monster's Claw ({attack_value}) ---> Player ({hero.health_points})")
    
    # Apply monster type description if available
    if hasattr(monster, 'get_description'):
        print_game_text(f"{monster.get_description()}")
    
    if attack_value >= hero.health_points:
        # Monster was strong enough to kill player in one blow
        hero.health_points = 0
        print_important("Player is dead!")
    else:
        # Monster only damaged the player
        hero.health_points -= attack_value
        print_game_text(f"The monster has reduced Player's health to: {hero.health_points}")
    
    return hero.health_points

# Recursion
# You can choose to go crazy, but it will reduce your health points by 5
def inception_dream(num_dream_lvls):
    num_dream_lvls = int(num_dream_lvls)
    # Base Case
    if num_dream_lvls == 1:
        print_section("Dream Level 1")
        print_game_text("You are in the deepest dream level now")
        print("    |", end="    ")
        input("Start to go back to real life? (Press Enter)")
        print_game_text("You start to regress back through your dreams to real life.")
        return 2

    # Recursive Case
    else:
        # inception_dream(5)
        # 1 + inception_dream(4)
        # 1 + 1 + inception_dream(3)
        # 1 + 1 + 1 + inception_dream(2)
        # 1 + 1 + 1 + 1 + inception_dream(1)
        # 1 + 1 + 1 + 1 + 2
        print_section(f"Dream Level {num_dream_lvls}")
        print_game_text(f"Entering dream level {num_dream_lvls}...")
        return 1 + int(inception_dream(num_dream_lvls - 1))


# Lab 06 - Question 3 and 4
def save_game(winner, hero_name="", num_stars=0):
    with open("save.txt", "a") as file:
        if winner == "Hero":
            file.write(f"Hero {hero_name} has killed a monster and gained {num_stars} stars.\n")
        elif winner == "Monster":
            file.write("Monster has killed the hero previously\n")

# Lab 06 - Question 5a
def load_game():
    try:
        with open("save.txt", "r") as file:
            print_section("Game History")
            print_game_text("Loading from saved file ...")
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                print_game_text(last_line)
                return last_line
    except FileNotFoundError:
        print_game_text("No previous game found. Starting fresh.")
        return None

# Lab 06 - Question 5b
def adjust_combat_strength(hero, monster):
    # Lab Week 06 - Question 5 - Load the game
    last_game = load_game()
    if last_game:
        if "Hero" in last_game and "gained" in last_game:
            num_stars = int(last_game.split()[-2])
            if num_stars > 3:
                print_game_text("... Increasing the monster's combat strength since you won so easily last time")
                monster.combat_strength += 1
        elif "Monster has killed the hero" in last_game:
            hero.combat_strength += 1
            print_game_text("... Increasing the hero's combat strength since you lost last time")
        else:
            print_game_text("... Based on your previous game, neither the hero nor the monster's combat strength will be increased")

# New function to select a combat environment
def select_environment():
    from monster_types import get_all_environments
    
    # Get all possible environments
    all_environments = get_all_environments()
    
    # Randomly select an environment for the battle
    selected_environment = random.choice(all_environments)
    
    # Display environment information
    print_section("Combat Environment")
    print_important(f"Combat takes place in a {selected_environment} environment!")
    
    return selected_environment


