# ------------ imports ------------
import os
import random

# ------------ weapon setup ------------

class Weapon:
    def __init__(self, damage: int, counter: int) -> None:
        self.damage = damage
        self.counter = counter

fists = Weapon(damage=1, counter=1)
sword = Weapon(damage=20, counter=10)
bow = Weapon(damage=10, counter=20)

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

    # color "사전" 생성
    colors = {"red": "\033[91m", "green": "\033[92m", "default": "\033[0m"}
    # get을 이용해서 color에 해당하는 값이 없으면 default를 반환
    color_code = colors.get(color, colors["default"])


    remaining_bars = entity.health // 10
    lost_bars = (entity.health_max - entity.health) // 10

    print(f"{entity.name}'s HEALTH: {entity.health}/{entity.health_max}")
    print(f"|"
          f"{color_code}{'█' * remaining_bars}{colors['default']}"
          f"{'-' * lost_bars}"
          f"|")


# ------------ game loop ------------
while True:
    os.system("cls")

    health_bar(hero, "green")
    health_bar(enemy, "red")

    # 우리의 행동
    action = input("choose action\n 1. attack, 2. counter: ")
    if action == "attack":
        action = input("choose weapon: 1. sword, 2. bow: ")

        if action == "sword":
            enemy.health -= sword.damage
        elif action == "bow":
            enemy.health -= bow.damage
        else:
            enemy.health -= fists.damage

    # 적의 행동
    action = random.choice(["fists", "sword", "bow"])
    if action == "sword":
        hero.health -= sword.damage
    elif action == "bow":
        hero.health -= bow.damage
    else:
        hero.health -= fists.damage
