# Import the random library to use for the dice later
import random
import os  # Import OS module for system information
import platform  # Import platform module for Python version information

# Put all the functions into another file and import them
import functions
from hero import Hero
from monster import Monster  # Import the Monster class

# Print Python version information
print("==================================================================")
print(f"Python Version: {platform.python_version()}")
print(f"Python Implementation: {platform.python_implementation()}")
print("==================================================================")

# Print operating system information
print("------------------------------------------------------------------")
print(f"Game running on operating system: {os.name}")
if os.name == 'nt':
    print("This is a Windows system")
elif os.name == 'posix':
    print("This is a Unix/Linux/Mac OS system")
else:
    print(f"This is an unknown operating system type: {os.name}")
print("------------------------------------------------------------------")

# Define two Dice
small_dice_options = list(range(1, 7))
big_dice_options = list(range(1, 21))

# Define the Weapons
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]

# Define the Loot
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
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

while input_invalid and i in range(5):
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    combat_strength_input = input("Enter your combat Strength (1-6): ")
    print("    |", end="    ")
    monster_strength_input = input("Enter the monster's combat Strength (1-6): ")

    # Validate input: Check if the string inputted is numeric
    if (not combat_strength_input.isnumeric()) or (not monster_strength_input.isnumeric()):
        # If one of the inputs are invalid, print error message and halt
        print("    |    One or more invalid inputs. Player needs to enter integer numbers for Combat Strength    |")
        i = i + 1
        continue

    # Note: Now safe to cast combat_strength to integer
    # Validate input: Check if the string inputted
    elif (int(combat_strength_input) not in range(1, 7)) or (int(monster_strength_input)) not in range(1, 7):
        print("    |    Enter a valid integer between 1 and 6 only")
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
    print("    |", end="    ")
    input("Roll the dice for your weapon (Press enter)")
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
    print("    |    The hero\'s weapon is " + str(weapons[weapon_roll - 1]))

    # Create hero and monster objects
    hero = Hero()
    hero.combat_strength = hero_strength
    
    monster = Monster()
    monster.combat_strength = monster_strength
    
    # Lab 06 - Question 5b
    functions.adjust_combat_strength(hero, monster)

    # Weapon Roll Analysis
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    input("Analyze the Weapon roll (Press enter)")
    print("    |", end="    ")
    if weapon_roll <= 2:
        print("--- You rolled a weak weapon, friend")
    elif weapon_roll <= 4:
        print("--- Your weapon is meh")
    else:
        print("--- Nice weapon, friend!")

    # If the weapon rolled is not a Fist, print out "Thank goodness you didn't roll the Fist..."
    if weapons[weapon_roll - 1] != "Fist":
        print("    |    --- Thank goodness you didn't roll the Fist...")

    # Hero's health points are set in the constructor
    print("    |", end="    ")
    input("Roll the dice for your health points (Press enter)")
    print("    |    Player rolled " + str(hero.health_points) + " health points")

    # Monster's health points are set in the constructor
    print("    |", end="    ")
    input("Roll the dice for the monster's health points (Press enter)")
    print("    |    Monster rolled " + str(monster.health_points) + " health points")

    # Collect Loot
    print("    ------------------------------------------------------------------")
    print("    |    !!You find a loot bag!! You look inside to find 2 items:")
    print("    |", end="    ")
    input("Roll for first item (enter)")

    # Collect Loot First time
    loot_options, belt = functions.collect_loot(loot_options, belt)
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    input("Roll for second item (Press enter)")

    # Collect Loot Second time
    loot_options, belt = functions.collect_loot(loot_options, belt)

    print("    |    You're super neat, so you organize your belt alphabetically:")
    belt.sort()
    print("    |    Your belt: ", belt)

    # Use Loot with hero object
    belt, hero_hp = functions.use_loot(belt, hero)
    hero.health_points = hero_hp

    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    input("Analyze the roll (Press enter)")
    # Compare Player vs Monster's strength
    print("    |    --- You are matched in strength: " + str(hero.combat_strength == monster.combat_strength))

    # Check the Player's overall strength and health
    print("    |    --- You have a strong player: " + str((hero.combat_strength + hero.health_points) >= 15))

    # Roll for the monster's power
    print("    |", end="    ")
    input("Roll for Monster's Magic Power (Press enter)")
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
    print(f"    |    The monster's combat strength is now {monster.combat_strength} using the {power_roll} magic power")

    # Lab Week 06 - Question 6
    num_dream_lvls = -1  # Initialize the number of dream levels
    while (num_dream_lvls < 0 or num_dream_lvls > 3):
        # Call Recursive function
        print("    |", end="    ")
        user_input = input("How many dream levels do you want to go down? (Enter a number 0-3)")
        
        try:
            # Try to convert the input to an integer
            num_dream_lvls = int(user_input)
            
            # Validate the integer is in range
            if num_dream_lvls < 0 or num_dream_lvls > 3:
                print("    |    Number entered must be a whole number between 0-3 inclusive, try again")
                num_dream_lvls = -1  # Reset to continue the loop
            elif num_dream_lvls != 0:
                # If valid and not 0, apply the dream levels
                hero.health_points -= 1
                crazy_level = functions.inception_dream(num_dream_lvls)
                hero.combat_strength += crazy_level
                print(f"    |    combat strength: {hero.combat_strength}")
                print(f"    |    health points: {hero.health_points}")
        except ValueError:
            # Handle the case where the input is not a valid number
            print("    |    Invalid input! Please enter a number between 0-3.")
            num_dream_lvls = -1  # Reset to continue the loop

    # Fight Sequence
    # Loop while the monster and the player are alive. Call fight sequence functions
    print("    ------------------------------------------------------------------")
    print("    |    You meet the monster. FIGHT!!")
    while monster.health_points > 0 and hero.health_points > 0:
        # Fight Sequence
        print("    |", end="    ")

        # Lab 5: Question 5:
        input("Roll to see who strikes first (Press Enter)")
        attack_roll = random.choice(small_dice_options)
        if not (attack_roll % 2 == 0):
            print("    |", end="    ")
            input("You strike (Press enter)")
            functions.hero_attacks(hero, monster)
            if monster.health_points == 0:
                num_stars = 3
            else:
                print("    |", end="    ")
                print("------------------------------------------------------------------")
                input("    |    The monster strikes (Press enter)!!!")
                functions.monster_attacks(monster, hero)
                
                if hero.health_points == 0:
                    num_stars = 1
                else:
                    num_stars = 2
        else:
            print("    |", end="    ")
            input("The Monster strikes (Press enter)")
            functions.monster_attacks(monster, hero)
            
            if hero.health_points == 0:
                num_stars = 1
            else:
                print("    |", end="    ")
                print("------------------------------------------------------------------")
                input("The hero strikes!! (Press enter)")
                functions.hero_attacks(hero, monster)
                if monster.health_points == 0:
                    num_stars = 3
                else:
                    num_stars = 2

    if(monster.health_points <= 0):
        winner = "Hero"
    else:
        winner = "Monster"

    # Final Score Display
    tries = 0
    input_invalid = True
    while input_invalid and tries in range(5):
        print("    |", end="    ")

        hero_name = input("Enter your Hero's name (in two words)")
        name = hero_name.split()
        if len(name) != 2:
            print("    |    Please enter a name with two parts (separated by a space)")
            tries += 1
        else:
            if not name[0].isalpha() or not name[1].isalpha():
                print("    |    Please enter an alphabetical name")
                tries += 1
            else:
                short_name = name[0][0:2:1] + name[1][0:1:1]
                print("    |    I'm going to call you " + short_name + " for short")
                input_invalid = False

    if not input_invalid:
        stars_display = "*" * num_stars
        print("    |    Hero " + short_name + " gets <" + stars_display + "> stars")

        functions.save_game(winner, hero_name=short_name, num_stars=num_stars)


