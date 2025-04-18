# Import the random library to use for the dice later
import random
import os  # Import OS module for system information
import platform  # Import platform module for Python version information

# Put all the functions into another file and import them
import functions
from functions import print_header, print_section, print_game_text, print_important, print_grid
from hero import Hero
from monster import Monster  # Import the Monster class
# Import the monster type system
from monster_types import generate_monster_types, TypedMonster, ElementalMonster, UndeadMonster, MechanicalMonster, MythicalMonster

# Print Python version information
print_header("MONSTER COMBAT GAME")
print_game_text(f"Python Version: {platform.python_version()}")
print_game_text(f"Python Implementation: {platform.python_implementation()}")

# Print operating system information
print_section("System Information")
print_game_text(f"Game running on operating system: {os.name}")
if os.name == 'nt':
    print_game_text("This is a Windows system")
elif os.name == 'posix':
    print_game_text("This is a Unix/Linux/Mac OS system")
else:
    print_game_text(f"This is an unknown operating system type: {os.name}")

game_score = 0  # Initialize game score variable

# Define two Dice
small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21))

# Define the Weapons and Spells
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
spells = ["Fire", "Ice", "Lightning", "Earth", "Water"]

# Define the Loot
loot_options = ["Apple", "Bread", "Health Potion", "Broken Glass", "Poison Potion", "Secret Note", "Leather Boots","Flimsy Gloves"]
belt = []

# Define the Monster's Powers
monster_powers = {
    "Fire Magic": 2,
    "Freeze Time": 4,
    "Super Hearing": 6
}

# Define the number of stars to award the player
num_stars = 0

# Loop to get valid input for Hero and Monster's Combat Strength
i = 0
input_invalid = True

print_section("Character Setup")
while input_invalid and i in range(5):
    print("\n")
    print_game_text("Enter your combat Strength (1-6): ")
    combat_strength_input = input("    > ")
    print_game_text("Enter the monster's combat Strength (1-6): ")
    monster_strength_input = input("    > ")

    # Validate input: Check if the string inputted is numeric
    if (not combat_strength_input.isnumeric()) or (not monster_strength_input.isnumeric()):
        # If one of the inputs are invalid, print error message and halt
        print_important("One or more invalid inputs. Player needs to enter integer numbers for Combat Strength!")
        i = i + 1
        continue

    # Note: Now safe to cast combat_strength to integer
    # Validate input: Check if the string inputted
    elif (int(combat_strength_input) not in range(1, 7)) or (int(monster_strength_input)) not in range(1, 7):
        print_important("Enter a valid integer between 1 and 6 only!")
        i = i + 1
        continue

    else:
        input_invalid = False
        break

if not input_invalid:
    input_invalid = False
    hero_strength = int(combat_strength_input)
    monster_strength = int(monster_strength_input)

    # Roll for weapon
    print_section("Weapon Selection")
    print_game_text("Roll the dice for your weapon (Press enter)")
    input("    > ")
    ascii_image5 = """
              , %               .           
   *      @./  #         @  &.(         
  @        /@   (      ,    @       # @ 
  @        ..@#% @     @&*#@(         % 
   &   (  @    (   / /   *    @  .   /  
     @ % #         /   .       @ ( @    
                 %   .@*                
               #         .              
             /     # @   *              
                 ,     %                
            @&@           @&@
            """
    print(ascii_image5)
    weapon_roll = random.choice(small_dice_options)

    # Limit the combat strength to 6
    hero_strength = min(6, (hero_strength + weapon_roll))
    print_important(f"The hero's weapon is {weapons[weapon_roll - 1]}")

    # Create hero and monster objects
    hero = Hero()
    hero.combat_strength = hero_strength

    # Implementing map and hero movement inside the map including random encounter
    # map size
    map_rows, map_cols = 9, 9
    # hero location
    hero_x, hero_y = 3, 5
    # number of towns in the map
    num_towns = 5
    # locations of towns in the map
    town_positions = {(2, 2), (7, 8), (3, 6), (7, 0), (6, 5)}

    # Game loop
    while True:
        # Check if player is dead
        if hero.health_points <= 0:
            print_important("You have been defeated! Game Over!")
            functions.save_game("Monster")
            break
            
        print_grid(hero_x, hero_y, map_rows, map_cols, town_positions)

        move = input("Move (W/A/S/D, Q to quit): ").lower()
        # select a random number from 1-100
        hero.randEnc = random.choice(range(1, 101))

        if move == 'q':
            print("Goodbye!")
            break
        elif move == 'w' and hero_x > 0:
            hero_x -= 1
        elif move == 's' and hero_x < map_rows - 1:
            hero_x += 1
        elif move == 'a' and hero_y > 0:
            hero_y -= 1
        elif move == 'd' and hero_y < map_cols - 1:
            hero_y += 1
        else:
            print("Invalid move or boundary reached!")
            # sets random encounter to 0 when move is invalid or map boundary reached
            hero.randEnc = 0

        if (hero_x, hero_y) in town_positions:
            print("You are in a town!")
            # sets random encounter to 0 when in town
            hero.randEnc = 0

        print("\n" + "-" * 20 + "\n")

        if hero.randEnc > 50:
            # Random encounter 50% chance to have no encounter while roaming the map
            pass
        elif hero.randEnc > 15:
            # Random encounter 35% chance to find a monster while roaming the map
            # FEATURE DEMONSTRATION: MONSTER TYPE SYSTEM
            print_header("MONSTER TYPE SYSTEM FEATURE")
            print_important("Creating a monster with the Monster Type System...")
            
            # Use dynamic monster type system instead of basic Monster
            # Generate a monster using list comprehension (in monster_types module)
            monster = generate_monster_types()
            monster.combat_strength = monster_strength

            # Display monster type immediately after generation
            if hasattr(monster, 'monster_type'):
                print_header("MONSTER ENCOUNTER")
                print_important(f"A {monster.monster_type} appears before you!")
                print_game_text(f"{monster.get_description()}")
                # Display environment information if the monster has it
                if hasattr(monster, 'environments') and monster.environments:
                    print_important(f"This monster thrives in: {', '.join(monster.environments)}")
                    print_game_text("Be careful if you encounter it in those areas!")

            # Set random spell weakness and resistance for the monster
            monster.spell_weakness = random.choice(spells)
            monster.spell_resistance = random.choice([spell for spell in spells if spell != monster.spell_weakness])

            # Lab 06 - Question 5b
            functions.adjust_combat_strength(hero, monster)

            # Weapon Roll Analysis
            print_section("Weapon Analysis")
            print_game_text("Analyze the Weapon roll (Press enter)")
            input("    > ")
            if weapon_roll <= 2:
                print_game_text("--- You rolled a weak weapon, friend")
            elif weapon_roll <= 4:
                print_game_text("--- Your weapon is meh")
            else:
                print_game_text("--- Nice weapon, friend!")

            # If the weapon rolled is not a Fist, print out "Thank goodness you didn't roll the Fist..."
            if weapons[weapon_roll - 1] != "Fist":
                print_game_text("--- Thank goodness you didn't roll the Fist...")

            # Hero's health points are set in the constructor
            print_section("Health Points")
            print_game_text("Roll the dice for your health points (Press enter)")
            input("    > ")
            print_important(f"Player rolled {hero.health_points} health points")

            # Monster's health points are set in the constructor
            print_game_text("Roll the dice for the monster's health points (Press enter)")
            input("    > ")
            print_important(f"Monster rolled {monster.health_points} health points")

            # Show monster's spell weaknesses and resistances
            print_section("Monster Spell Properties")
            print_important(f"Monster is WEAK against {monster.spell_weakness} spells")
            print_important(f"Monster is RESISTANT to {monster.spell_resistance} spells")

            # Use Loot with hero object
            if belt:
                belt, hero_hp = functions.use_loot(belt, hero)
                hero.health_points = hero_hp
            else:
                print_game_text("Hero tried to reach for items in his belt but it is empty.")

            print_section("Character Status")
            print_game_text("Analyze the roll (Press enter)")
            input("    > ")
            # Compare Player vs Monster's strength
            print_game_text(f"--- You are matched in strength: {hero.combat_strength == monster.combat_strength}")

            # Check the Player's overall strength and health
            print_game_text(f"--- You have a strong player: {(hero.combat_strength + hero.health_points) >= 15}")

            # Roll for the monster's power
            print_section("Monster Magic")
            print_game_text("Roll for Monster's Magic Power (Press enter)")
            input("    > ")
            ascii_image4 = """
                        @%   @                      
                @     @                        
                    &                          
            @      .                          

            @       @                    @     
                    @                  @      
            @         @              @  @     
            @            ,@@@@@@@     @      
                @                     @        
                    @               @           
                        @@@@@@@                

                                            """
            print(ascii_image4)
            power_roll = random.choice(["Fire Magic", "Freeze Time", "Super Hearing"])

            # Increase the monster's combat strength by its power
            monster.combat_strength += min(6, monster_powers[power_roll])
            print_important(f"The monster's combat strength is now {monster.combat_strength} using the {power_roll} magic power")

            # FEATURE DEMONSTRATION: ENVIRONMENT SYSTEM
            print_header("ENVIRONMENT INTERACTION FEATURE")
            
            # Select a random environment for the battle
            combat_environment = functions.select_environment()
            
            # Instead of generating a new monster, apply environment effects to the existing monster
            print_header("ENVIRONMENT EFFECT ON MONSTER")
            
            # Check if the environment affects the monster
            if hasattr(monster, 'environments') and combat_environment in monster.environments:
                environment_bonus = monster.environment_bonus(combat_environment)
                monster.combat_strength += environment_bonus
                print_important(f"The {monster.monster_type} is in its natural habitat: {combat_environment}!")
                print_game_text(f"It gains {environment_bonus} additional combat strength!")
                print_important(f"Combat strength increased to {monster.combat_strength}!")
            else:
                print_important(f"The {monster.monster_type} is now in a {combat_environment} environment.")
                if hasattr(monster, 'environments') and monster.environments:
                    print_game_text(f"This is not its natural habitat. It prefers: {', '.join(monster.environments)}")
                else:
                    print_game_text("This monster has no environment preferences.")
            
            # Still show monster information for clarity
            print_game_text(f"{monster.get_description()}")
            
            # Show monster's spell weaknesses and resistances again
            print_section("Monster Spell Properties")
            print_important(f"Monster is WEAK against {monster.spell_weakness} spells")
            print_important(f"Monster is RESISTANT to {monster.spell_resistance} spells")
            
            # Show weapon effectiveness using list comprehension with nested conditionals
            if hasattr(monster, 'monster_type'):
                print_section("Weapon Effectiveness")
                weapon_effectiveness = [
                    f"{weapon} is " + 
                    ("EFFECTIVE against" if weapon in monster.weaknesses else 
                     "WEAK against" if weapon in monster.strengths else 
                     "NEUTRAL against") + 
                    f" this monster!"
                    for weapon in weapons
                ]
                
                # Print the effectiveness information for the player's weapon
                current_weapon = weapons[min(5, weapon_roll - 1)]
                print_important(f"Your weapon: {current_weapon}")
                for info in [info for info in weapon_effectiveness if current_weapon in info]:
                    print_game_text(info)

            # Apply environment bonus for monster if applicable
            if hasattr(monster, 'environment_bonus'):
                bonus = monster.environment_bonus(combat_environment)
                if bonus > 0:
                    monster.combat_strength += bonus
                    print_important(f"The {monster.monster_type} gains {bonus} combat strength in this {combat_environment}!")

            # Lab Week 06 - Question 6
            print_section("Dream Levels")
            num_dream_lvls = -1  # Initialize the number of dream levels
            while (num_dream_lvls < 0 or num_dream_lvls > 3):
                # Call Recursive function
                print_game_text("How many dream levels do you want to go down? (Enter a number 0-3)")
                user_input = input("    > ")

                try:
                    # Try to convert the input to an integer
                    num_dream_lvls = int(user_input)

                    # Validate the integer is in range
                    if num_dream_lvls < 0 or num_dream_lvls > 3:
                        print_important("Number entered must be a whole number between 0-3 inclusive, try again")
                        num_dream_lvls = -1  # Reset to continue the loop
                    elif num_dream_lvls != 0:
                        # If valid and not 0, apply the dream levels
                        hero.health_points -= 1
                        crazy_level = functions.inception_dream(num_dream_lvls)
                        hero.combat_strength += crazy_level
                        print_important(f"Combat strength: {hero.combat_strength}")
                        print_important(f"Health points: {hero.health_points}")
                except ValueError:
                    # Handle the case where the input is not a valid number
                    print_important("Invalid input! Please enter a number between 0-3.")
                    num_dream_lvls = -1  # Reset to continue the loop

            # FEATURE DEMONSTRATION: MONSTER COMBAT ABILITIES
            print_header("MONSTER COMBAT ABILITIES FEATURE")
            print_important("Starting combat to demonstrate monster abilities and adaptations!")
            
            # Fight Sequence
            # Loop while the monster and the player are alive. Call fight sequence functions
            print_header("COMBAT BEGINS")
            print_important("You meet the monster. FIGHT!!")

            # Track the number of times each weapon is used for monster adaptation
            weapon_usage = {}

            while monster.health_points > 0 and hero.health_points > 0:
                # Fight Sequence
                print_section("Initiative Roll")
                print_game_text("Roll to see who strikes first (Press Enter)")
                input("    > ")
                attack_roll = random.choice(small_dice_options)
                if not (attack_roll % 2 == 0):
                    print_important("You strike first!")
                    print_game_text("Press enter to attack")
                    input("    > ")

                    # Get current weapon and track usage for adaptation
                    current_weapon = weapons[min(5, hero.combat_strength - 1)]
                    weapon_usage[current_weapon] = weapon_usage.get(current_weapon, 0) + 1

                    # Show adaptation message if weapon has been used multiple times
                    if weapon_usage[current_weapon] > 1 and hasattr(monster, 'adaptive') and monster.adaptive:
                        print_important(f"The {monster.monster_type} seems to be studying your {current_weapon} attacks...")

                    functions.hero_attacks(hero, monster, belt)
                    if monster.health_points == 0:
                        score_gained = monster.get_score(hero.health_points)  # Calculate score based on player's health
                        game_score += score_gained  # Update total game score
                        print_important(f"You defeated {monster.monster_type}! You earned {score_gained} points.")  # Display score
                        num_stars = 3
                    else:
                        print_important("The monster strikes!")
                        print_game_text("Press enter to continue")
                        input("    > ")
                        functions.monster_attacks(monster, hero)

                        if hero.health_points == 0:
                            num_stars = 1
                            print_important("You have been defeated by the monster!")
                            # Check if score is high enough to continue
                            if game_score > 30:
                                # Reset hero's health to half of 30 for next encounters
                                hero.health_points = 15  # 30/2 health
                                print_important(f"Your score of {game_score} is high enough! You managed to escape and recover. Health restored to {hero.health_points}.")
                            else:
                                print_important(f"Your score of {game_score} is too low. You need more than 30 points to continue after defeat.")
                                print("Game Over!")
                                # Save the game with "Monster" as winner before exiting
                                functions.save_game("Monster")
                                break
                else:
                    print_important("The Monster strikes first!")
                    print_game_text("Press enter to continue")
                    input("    > ")
                    functions.monster_attacks(monster, hero)
                    if hero.health_points == 0:
                        num_stars = 1
                        print_important("You have been defeated by the monster!")
                        # Check if score is high enough to continue
                        if game_score > 30:
                            # Reset hero's health to half of 30 for next encounters
                            hero.health_points = 15  # 30/2 health
                            print_important(f"Your score of {game_score} is high enough! You managed to escape and recover. Health restored to {hero.health_points}.")
                        else:
                            print_important(f"Your score of {game_score} is too low. You need more than 30 points to continue after defeat.")
                            print("Game Over!")
                            # Save the game with "Monster" as winner before exiting
                            functions.save_game("Monster")
                            break
                    else:
                        print_important("Now you can strike back!")
                        print_game_text("Press enter to attack")
                        input("    > ")

                        # Get current weapon and track usage for adaptation
                        current_weapon = weapons[min(5, hero.combat_strength - 1)]
                        weapon_usage[current_weapon] = weapon_usage.get(current_weapon, 0) + 1

                        # Show adaptation message if weapon has been used multiple times
                        if weapon_usage[current_weapon] > 1 and hasattr(monster, 'adaptive') and monster.adaptive:
                            print_important(f"The {monster.monster_type} seems to be studying your {current_weapon} attacks...")

                        functions.hero_attacks(hero, monster, belt)
                        if monster.health_points == 0:
                            score_gained = monster.get_score(hero.health_points)  # Calculate score based on player's health
                            game_score += score_gained  # Update total game score
                            print_important(f"You defeated {monster.monster_type}! You earned {score_gained} points.")  # Display score
                            num_stars = 3

            if(monster.health_points <= 0):
                winner = "Hero"
                # Final Score Display
                print_header("GAME RESULTS")
                tries = 0
                input_invalid = True
                while input_invalid and tries in range(5):
                    print_game_text("Enter your Hero's name (in two words)")
                    hero_name = input("    > ")
                    name = hero_name.split()
                    if len(name) != 2:
                        print_important("Please enter a name with two parts (separated by a space)")
                        tries += 1
                    else:
                        if not name[0].isalpha() or not name[1].isalpha():
                            print_important("Please enter an alphabetical name")
                            tries += 1
                        else:
                            short_name = name[0][0:2:1] + name[1][0:1:1]
                            print_important(f"I'm going to call you {short_name} for short")
                            input_invalid = False

                if not input_invalid:
                    stars_display = "*" * num_stars
                    print_important(f"Hero {short_name} gets <{stars_display}> stars")

                    # **Final Score Display**
                    print_header("FINAL SCORE")
                    print_important(f"Total Score: {game_score}")

                    functions.save_game(winner, hero_name=short_name, num_stars=num_stars)
            else:
                # If monster won (player died), just save the game without asking for name
                winner = "Monster"
                functions.save_game(winner)
                # Score is already displayed when hero is revived, so no need to show it again

        elif hero.randEnc > 10:
            # Random encounter 5% chance to find a traveling merchant while roaming the map
            print("You found a traveling merchant!")
            print("Buy & Sell feature is Coming Soon!")
        elif hero.randEnc > 0:
            # Random encounter 10% chance to find a loot bag while roaming the map
            # Collect Loot
            print_section("Treasure Hunt")
            print_game_text("!!You find a loot bag!! You look inside to find 2 items:")
            print_game_text("Roll for first item (enter)")
            input("    > ")

            # Collect Loot First time
            loot_options, belt = functions.collect_loot(loot_options, belt)

            print_game_text("Roll for second item (Press enter)")
            input("    > ")

            # Collect Loot Second time
            loot_options, belt = functions.collect_loot(loot_options, belt)

            print_game_text("You're super neat, so you organize your belt alphabetically:")
            belt.sort()
            print_important(f"Your belt: {belt}")
        else:
            pass

