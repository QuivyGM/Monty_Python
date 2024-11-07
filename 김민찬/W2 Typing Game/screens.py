import os
import time
# 화면 크기 구하는데 사용함
import shutil
os.system("")

terminal_size = shutil.get_terminal_size()
frame_width = terminal_size.columns  # Set frame_width to the number of columns

# 화면을 비우는 함수
def clear_area():
    for i in range(2, 8):
        print(f"\033[{i};1H\033[K")
        time.sleep(0.1)

# 시작화면을 출력하는 함수
def load_title():
    os.system("cls")
    print("=" * frame_width)
    time.sleep(0.1)
    print("\t _______   ______ ___ _   _  ____    ____    _    __  __ _____")
    time.sleep(0.1)
    print("\t|_   _\\ \\ / /  _ \\_ _| \\ | |/ ___|  / ___|  / \\  |  \\/  | ____|")
    time.sleep(0.1)
    print("\t  | |  \\ V /| |_) | ||  \\| | |  _  | |  _  / _ \\ | |\\/| |  _|")
    time.sleep(0.1)
    print("\t  | |   | | |  __/| || |\\  | |_| | | |_| |/ ___ \\| |  | | |___")
    time.sleep(0.1)
    print("\t  |_|   |_| |_|  |___|_| \\_|\\____|  \\____/_/   \\_\\_|  |_|_____|")
    time.sleep(0.1)
    print("")
    time.sleep(0.1)
    print("=" * frame_width)
    time.sleep(0.5)

# 메뉴 화면을 보여주는 함수
def load_menu():
    clear_area()
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

# 게임 시작 전 화면 - 선택된 게임 모드 표시
def highlight_mode(mode):
    clear_area()
    for i in range(2):
        print("\033[3;24H\033[K")
        time.sleep(0.5)
        print("\033[3;25HGamemode " + mode + " has been chosen!")
        time.sleep(0.5)
    for i in range(2):
        print("\033[4;1H\033[K")
        time.sleep(0.5)
        print("\033[4;35HFive Rounds")
        time.sleep(0.5)

