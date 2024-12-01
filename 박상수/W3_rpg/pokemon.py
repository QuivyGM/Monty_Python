import os
import random
from threading import activeCount
from tkinter.font import names


class Character:
    def __init__(self, name:str, health:int) -> None:
        self.name = name
        self.health = health
        self.health_max = health

        self.Weapon = fists

hero = Character(name = "Hero", health = 100)
enemy = Character(name = "Enemy", health = 100)

def health_bar(entity,color) -> None:



class Weapon:
     def __init__(self, damage: int, counter: int):
        self.damage = damage
        self.counter = counter

fists = Weapon(damage = 1, counter = 1)
sword = Weapon(damage = 2, counter = 2)

colors = {"red": "\033[91m", "green"}

while True:
    os.system("cls")

    action = input("choose action\n 1. attack 2. parry:")
    if action == "1":
        action = input("choose weapon: 1. fists 2. sword:")
        if action == "1":
            enemy.health -= fists.damage
        else action == "2":
            enemy.health -= sword.damage