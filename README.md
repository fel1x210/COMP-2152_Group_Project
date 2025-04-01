# Dynamic Monster Type System

This project implements a turn-based combat game with a dynamic monster type system that features different monster categories and weapon interactions.

## Monster Type System

The monster type system generates different monster categories (elemental, undead, mechanical) using list comprehension, with each type having unique strengths and weaknesses determined by nested conditionals that affect combat interactions with the hero's weapons.

### Features

- **Dynamic Monster Generation**: Monsters are randomly generated from three main categories: Elemental, Undead, and Mechanical.
- **List Comprehension**: The system uses list comprehension to create and filter monster instances dynamically.
- **Nested Conditionals**: Weapon effectiveness is determined through nested conditional expressions that evaluate monster type against weapon type.
- **Damage Modifiers**: Each monster type has specific strengths and weaknesses against different weapons:
  - Weapons effective against a monster type deal 150% damage
  - Weapons that are weak against a monster type deal only 50% damage

### Monster Categories

1. **Elemental Monsters**
   - Types: Fire, Water, Earth, Air
   - Each element has unique strengths and weaknesses

2. **Undead Monsters**
   - Types: Zombie, Skeleton, Ghost, Vampire
   - Generally weak against specific weapons based on lore

3. **Mechanical Monsters**
   - Types: Robot, Golem, Automaton, Drone
   - Often resistant to physical attacks but vulnerable to explosives

## How to Run

1. Main game: `python main.py`
2. Monster Type Demo: `python monster_type_demo.py`

## Technical Implementation

- The system uses inheritance with a base `TypedMonster` class that extends the original `Monster` class
- Type-specific behavior is implemented in subclasses (`ElementalMonster`, `UndeadMonster`, `MechanicalMonster`)
- Combat calculations use the `calculate_damage_modifier` method to adjust damage based on weapon effectiveness
- List comprehension is used in monster generation and combat calculations

## Code Examples

### Monster Generation with List Comprehension

```python
monster_types = [
    ElementalMonster() if category == "Elemental" 
    else UndeadMonster() if category == "Undead"
    else MechanicalMonster() if category == "Mechanical" 
    else TypedMonster() 
    for category in monster_categories
]
```

### Nested Conditionals for Weapon Effectiveness

```python
weapon_effectiveness = [
    f"{weapon} is " + 
    ("EFFECTIVE against" if weapon in monster.weaknesses else 
     "WEAK against" if weapon in monster.strengths else 
     "NEUTRAL against") + 
    " this monster!"
    for weapon in weapons
]
``` 