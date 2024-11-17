# ------------ imports ------------
import os
import random
import time
import keyboard  # to capture keyboard events for arrow keys


# ------------ weapon setup ------------

class Weapon:
    def __init__(self, damage: int, counter: int) -> None:
        self.damage = damage
        self.counter = counter


fists = Weapon(damage=1, counter=1)
sword = Weapon(damage=15, counter=15)
bow = Weapon(damage=10, counter=5)


# ------------ character setup ------------

class Character:
    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health
        self.health_max = health

        self.weapon = fists


hero = Character(name="Hero", health=100)
enemy = Character(name="Enemy", health=100)


# ------------ health print ------------

def health_bar(entity, color) -> None:
    colors = {"red": "\033[91m", "green": "\033[92m", "default": "\033[0m"}
    color_code = colors.get(color, colors["default"])

    remaining_bars = entity.health // 10
    lost_bars = (entity.health_max - entity.health) // 10

    print(f"{entity.name}'s HEALTH: {entity.health}/{entity.health_max}")
    print(f"|"
          f"{color_code}{'█' * remaining_bars}{colors['default']}"
          f"{'-' * lost_bars}"
          f"|")


# ------------ action selection using arrow keys ------------
def choose_action():
    options = ["attack", "counter"]
    selected_index = 0

    while True:
        print("\033[5;H\033[J", end="")  # Clear the console
        print("Choose action:\n")

        for i, option in enumerate(options):
            if i == selected_index:
                print(f"--> {option.capitalize()}")
            else:
                print(f"    {option.capitalize()}")

        key = keyboard.read_event()

        if key.event_type == keyboard.KEY_DOWN:
            if key.name == "down":
                selected_index = (selected_index + 1) % len(options)
            elif key.name == "up":
                selected_index = (selected_index - 1) % len(options)
            elif key.name == "enter":
                return options[selected_index]


# ------------ weapon selection using arrow keys ------------
def choose_weapon():
    weapons = ["sword", "bow", "fists"]
    selected_index = 0

    while True:
        print("\033[5;H\033[J", end="")  # Clear the console
        print("Choose weapon:\n")

        for i, weapon in enumerate(weapons):
            if i == selected_index:
                print(f"--> {weapon.capitalize()}")
            else:
                print(f"    {weapon.capitalize()}")

        key = keyboard.read_event()

        if key.event_type == keyboard.KEY_DOWN:
            if key.name == "down":
                selected_index = (selected_index + 1) % len(weapons)
            elif key.name == "up":
                selected_index = (selected_index - 1) % len(weapons)
            elif key.name == "enter":
                return weapons[selected_index]

def choose_fight_or_run():
    options = ["fight", "run"]
    selected_index = 0

    while True:
        print("\033[13;H\033[J", end="")  # Clear the console
        print("Choose action:\n")

        for i, option in enumerate(options):
            if i == selected_index:
                print(f"--> {option.capitalize()}")
            else:
                print(f"    {option.capitalize()}")

        key = keyboard.read_event()

        if key.event_type == keyboard.KEY_DOWN:
            if key.name == "down":
                selected_index = (selected_index + 1) % len(options)
            elif key.name == "up":
                selected_index = (selected_index - 1) % len(options)
            elif key.name == "enter":
                return options[selected_index]



ascii_art = r"""⠀⠀
                                      ⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                      ⢻⣿⡗⢶⣤ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠀⠀⣀⣠⣄
                                      ⠀⢻⣇⠈⠙⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀ ⠀⠀⠀⣀⣤⠶⠛⠋⣹⣿⡿
                                      ⠀⠀⠹⣆⠀⠀⠀⠀⠙⢷⣄⣀⣀⣀⣤⣤⣤⣄⣀⣴⠞⠋⠉⠀⠀⢀⣿⡟⠁
                                      ⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋
                                      ⠀⠀⠀⠀⠈⠻⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣠⡾⠋⠀
    \                                 ⠀⠀⠀⠀⠀⣼⠃⠀⢠⠒⣆⠀⠀⠀⠀⠀⠀⢠⢲⣄⠀⠀⠀⢻⣆
     \    O                           ⠀⠀⠀⠀⢰⡏⠀⠀⠈⠛⠋⠀⢀⣀⡀⠀⠀⠘⠛⠃⠀⠀⠀⠈⣿⡀
     _\|  |  }                           ⠀⣾⡟⠛⢳⠀⠀⠀⠀⠀⣉⣀⠀⠀⠀⠀⣰⢛⠙⣶⠀⢹⣇  
       M_/|\_|}                       ⠀⠀⠀⠀⢿⡗⠛⠋⠀⠀⠀⠀⣾⠋⠀⢱⠀⠀⠀⠘⠲⠗⠋⠀⠈⣿
          |  }                        ⠀⠀⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠈⠓⠒⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇
         / \                          ⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧ 
       _/   \_                             ⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁                               
"""

print(ascii_art)
choose_fight_or_run()

os.system("cls")
action = choose_fight_or_run()
if action == "fight":
    print(f"{hero.name} chose to fight!")
    fight=1
else:
    print(f"{hero.name} chose to run away!")
    fight = 0




time.sleep(3)


# ------------ game loop ------------
while fight==1:
    os.system("cls")

    health_bar(hero, "green")
    health_bar(enemy, "red")

    # Enemy action chosen
    enemy_action = random.choice(["counter", "sword", "bow"])
    if enemy_action == "sword":
        enemy_damage = sword.damage
        enemy_counter = sword.counter
    elif enemy_action == "bow":
        enemy_damage = bow.damage
        bow_counter = bow.counter

    # Hero's action using arrow keys
    action = choose_action()
    if action == "attack":  # Attack
        weapon_choice = choose_weapon()

        if enemy_action == "counter":  # If enemy counters
            print(f"{hero.name} attacked {enemy.name} with {weapon_choice}!")
            time.sleep(0.5)
            print(f"{enemy.name} countered!")
            time.sleep(0.5)
            if weapon_choice == "sword":
                print(f"{hero.name} took {sword.counter} damage!")
                hero.health -= sword.counter
            elif weapon_choice == "bow":
                print(f"{hero.name} took {bow.counter} damage!")
                hero.health -= bow.counter
            else:
                print(f"{hero.name} took {fists.counter} damage!")
                hero.health -= fists.counter

        else:  # No counters
            print(f"{hero.name} attacked {enemy.name} with {weapon_choice}!")
            time.sleep(0.5)
            if weapon_choice == "sword":
                print(f"{enemy.name} took {sword.damage} damage!")
                enemy.health -= sword.damage
            elif weapon_choice == "bow":
                print(f"{enemy.name} took {bow.damage} damage!")
                enemy.health -= bow.damage
            else:
                print(f"{enemy.name} took {fists.damage} damage!")
                enemy.health -= fists.damage

            time.sleep(0.5)
            print(f"{enemy.name} attacked {hero.name} with {enemy_action}!")
            time.sleep(0.5)
            print(f"{hero.name} took {enemy_damage} damage!")
            hero.health -= enemy_damage

    else:  # Hero counter
        print(f"{enemy.name} attacked {hero.name} with {enemy_action}!")
        time.sleep(0.5)
        print(f"{hero.name} countered!")
        time.sleep(0.5)
        if enemy_action == "sword":
            print(f"{enemy.name} took {sword.counter} damage!")
            enemy.health -= sword.counter
        elif enemy_action == "bow":
            print(f"{enemy.name} took {bow.counter} damage!")
            enemy.health -= bow.counter
        else:
            print(f"{enemy.name} took {fists.counter} damage!")
            enemy.health -= fists.counter

    time.sleep(3)
