import os
import random
import time
import shutil
import starting_screen

# clear file path from screen
print("load")
time.sleep(0.1)
os.system("cls")

#starting_screen.screenstart()

# start game loop
while True:
    os.system("cls")
    # Get the current terminal size
    terminal_size = shutil.get_terminal_size()
    frame_width = terminal_size.columns  # Set frame_width to the number of columns

    print("=" * frame_width+"\n")
    print(r"""
         _____ ___  _ ____  _  _      _____   _____ ____  _      _____
        /__ __\\  \///  __\/ \/ \  /|/  __/  /  __//  _ \/ \__/|/  __/
          / \   \  / |  \/|| || |\ ||| |  _  | |  _| / \|| |\/|||  \  
          | |   / /  |  __/| || | \||| |_//  | |_//| |-||| |  |||  /_ 
          \_/  /_/   \_/   \_/\_/  \|\____\  \____\\_/ \|\_/  \|\____\

        """)
    print("\t\t\t\t[[Choose Gamemode]]\n")

    print("\t\t\t    1. Numbers\t\t2. Words\t")
    print("\t\t\t    3. Sentences\t4. Scoreboard")
    print("\t5. Exit\n".center(frame_width))
    mode = input("\t\t\t\tEnter: ")

    #highlight selected mode
    for i in range(3):
        print("\n\n\033[A\t\t\t    Gamemode " + mode + " has been chosen!")
        time.sleep(0.5)
        print ("\033[A                                                       \033[A", end="")
        time.sleep(0.5)

    rounds = input("\n\t\t\t\t    How many rounds?\n\t\t\t\t\t\t")

    os.system("cls")
    time.sleep(1)

    for i in range(3):
        print("\n\n\033[A\t\t\t    Starting in " + str(3 - i))
        time.sleep(0.5)
        print ("\033[A\t\t\t    Starting in\033[A", end="")
        time.sleep(0.5)

    #if mode == 1:

    #
    #
