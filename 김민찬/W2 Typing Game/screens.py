import os
import time
import shutil
os.system("")

terminal_size = shutil.get_terminal_size()
frame_width = terminal_size.columns  # Set frame_width to the number of columns

def starting_screen():
    os.system("cls")
    print("=" * frame_width + "\n\n\n\n\n\n\n" + "=" * frame_width)
    for i in range(3):
        time.sleep(0.5)
        os.system("cls")
        print("=" * frame_width + r"""
         _______   ______ ___ _   _  ____    ____    _    __  __ _____
        |_   _\ \ / /  _ \_ _| \ | |/ ___|  / ___|  / \  |  \/  | ____|
          | |  \ V /| |_) | ||  \| | |  _  | |  _  / _ \ | |\/| |  _|
          | |   | | |  __/| || |\  | |_| | | |_| |/ ___ \| |  | | |___
          |_|   |_| |_|  |___|_| \_|\____|  \____/_/   \_\_|  |_|_____|
          """+ "\n" + "=" * frame_width)
        time.sleep(0.5)
        print("\033[2;2H\033[K\033[3;2H\033[K\033[4;2H\033[K\033[5;2H\033[K\033[6;2H\033[K")



def menu_screen():
    #os.system("cls")
    print("=" * frame_width + "\n\n\n\n\n\n\n" + "=" * frame_width)
    time.sleep(0.5)
    print("\033[2;2H\t\t\t        [[Choose Gamemode]]\n")
    time.sleep(0.1)
    print("    1. Numbers", end=" ")
    time.sleep(0.1)
    print("    2. Words", end=" ")
    time.sleep(0.1)
    print("    3. Sentences", end=" ")
    time.sleep(0.1)
    print("    4. Scoreboard", end=" ")
    time.sleep(0.1)
    print("    5. Exit")