import os
import time
import shutil

def screenstart():
    terminal_size = shutil.get_terminal_size()
    frame_width = terminal_size.columns  # Set frame_width to the number of columns

    for i in range(3):
        time.sleep(0.5)
        os.system("cls")
        print("=" * frame_width + "\n")
        print(r"""
             _____ ___  _ ____  _  _      _____   _____ ____  _      _____
            /__ __\\  \///  __\/ \/ \  /|/  __/  /  __//  _ \/ \__/|/  __/
              / \   \  / |  \/|| || |\ ||| |  _  | |  _| / \|| |\/|||  \
              | |   / /  |  __/| || | \||| |_//  | |_//| |-||| |  |||  /_
              \_/  /_/   \_/   \_/\_/  \|\____\  \____\\_/ \|\_/  \|\____\
              
            """)
        print("=" * frame_width + "\n")
        time.sleep(0.5)
        os.system("cls")

        print("=" * frame_width + "\n\n\n\n\n\n\n\n\n\n"+"=" * frame_width)
