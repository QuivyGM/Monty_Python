import os
import random
import time
import shutil
import screens
os.system("")

# clear file path from screen
print("load")
time.sleep(0.2)
os.system("cls")

#starting_screen.screenstart()

# start game loop
while True:
    # starting
    #screens.starting_screen()
    screens.menu_screen()
    time.sleep(0.1)
    mode = input("\n\t\t\t\t     Enter: ")

    # #highlight selected mode
    # for i in range(3):
    #     print("\033[A\t\t\t    Gamemode " + mode + " has been chosen!")
    #     time.sleep(0.5)
    #     print ("\t\t\t                    ", end="")
    #     time.sleep(0.5)

    # rounds = input("\n\t\t\t\t    How many rounds?\n\t\t\t\t\t\t")

    # os.system("cls")
    # time.sleep(1)

    # for i in range(3):
    #     print("\n\n\033[A\t\t\t    Starting in " + str(3 - i))
    #     time.sleep(0.5)
    #     print ("\033[A\t\t\t    Starting in\033[A", end="")
    #     time.sleep(0.5)

    #if mode == 1:

    #debug use break
    break
