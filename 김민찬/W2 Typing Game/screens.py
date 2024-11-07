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
title_start=10
def load_title():
    os.system("cls")
    print("=" * frame_width)
    time.sleep(0.1)
    print(f"\033[2;{title_start}H _______   ______ ___ _   _  ____    ____    _    __  __ _____")
    time.sleep(0.1)
    print(f"\033[3;{title_start}H|_   _\\ \\ / /  _ \\_ _| \\ | |/ ___|  / ___|  / \\  |  \\/  | ____|")
    time.sleep(0.1)
    print(f"\033[4;{title_start}H  | |  \\ V /| |_) | ||  \\| | |  _  | |  _  / _ \\ | |\\/| |  _|")
    time.sleep(0.1)
    print(f"\033[5;{title_start}H  | |   | | |  __/| || |\\  | |_| | | |_| |/ ___ \\| |  | | |___")
    time.sleep(0.1)
    print(f"\033[6;{title_start}H  |_|   |_| |_|  |___|_| \\_|\\____|  \\____/_/   \\_\\_|  |_|_____|")
    time.sleep(0.1)
    print("")
    time.sleep(0.1)
    print("=" * frame_width)
    time.sleep(1)

# 메뉴 화면을 보여주는 함수
def load_menu():
    clear_area()
    time.sleep(0.5)
    print("\033[2;31H[[Choose Gamemode]]\n")
    time.sleep(0.1)
    print("\033[4;7H1. Numbers")
    time.sleep(0.1)
    print("\033[4;23H2. Words", end=" ")
    time.sleep(0.1)
    print("\033[4;35H3. Sentences", end=" ")
    time.sleep(0.1)
    print("\033[4;50H4. Scoreboard", end=" ")
    time.sleep(0.1)
    print("\033[4;68H5. Exit")

# 게임 시작 전 화면 - 선택된 게임 모드 표시
def highlight_mode(mode):
    clear_area()
    for i in range(2):
        print("\033[3;24H\033[K")
        time.sleep(0.5)
        print("\033[3;27HGamemode " + mode + " has been chosen!")
        time.sleep(0.5)

    mode_name = ["< Numbers >", "< Words >", "< Sentences >"]
    name_pos = (80 - len(str(mode_name[int(mode)-1]))) // 2
    for i in range(2):
        print("\033[5;1H\033[K")
        time.sleep(0.5)
        print(f"\033[5;{name_pos}H" + mode_name[int(mode)-1])
        time.sleep(0.5)



