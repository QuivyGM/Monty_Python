# os module: 오퍼레이팅 시스템 연결 주는 모듄
import os
# random module: 난수 생성을 주는 모듈
import random
# time module: 시간 관련 시스템 연결
import time
# 커스텀 화면 출력 모듈
import screens
# 화면 출력 보조
os.system("")


# clear file path from screen - 화면 비우기 용도 //  사실상 의미 없음
print("loading")
time.sleep(0.5)             # 대기 명령어
os.system("cls && cls")     # 화면 모두 비우기

# 게임 타이틀 화면 로딩
screens.load_title()


# start game loop   -   게임 플레이 루프
while True:
    # 메뉴 표시
    screens.load_menu()
    time.sleep(0.1)

    # 게임 모드 입력 받기
    mode = input("\033[6;37HEnter: ")  # 입력 받기


    # 올바르지 않은 입력의 경우
        # mode.isdigit() 는 숫자로 이루어져있는지 확인을 한다
        # (1 <= int(mode) <= 5) 는 숫자가 1부터 5까지 안에 있는 숫자인지 확인을 한다
    if not mode.isdigit() or not (1 <= int(mode) <= 5):
        # 화면을 비우고 잘못됬다는 알림을 보여준다
        screens.clear_area()
        print("\033[4;26HInvalid mode. Please try again.")
        time.sleep(1)


    # Exit Condition    -   종료시에
    elif(mode=='5'):
        # ANSI escape code - 안시 이스케이프 코드는 터미널에서 커서의 위치를 욺길수 있음
        screens.clear_area()
        print("\033[4;37HByebye")
        time.sleep(1)
        exit()


    #
    elif (mode == '4'):  # Scoreboard - 점수판
        screens.clear_area()
        time.sleep(0.1)
        print("\033[2;22HNumbers\033[2;38HWords\033[2;52HSentences")
        time.sleep(0.1)
        print("\033[3;22H" + "*"*40)
        time.sleep(0.1)

        with open('scoreboard.txt', 'r') as file:
            scores = file.read().replace(',', '').split()
            for i in range(3):
                print(f"\033[{4+i};24H{scores[i*3]}\033[{4+i};40H{scores[i*3+1]}\033[{4+i};56H{scores[i*3+2]}")
                time.sleep(0.1)
        input("\033[0m\033[7;29H[[Press Enter to return]]")


    # 게임 모드일때
    else:
        # highlight selected mode   -   선택된 모드 깜빡이
        screens.highlight_mode(mode)

        #다섯번의 라운드
        j=0;
        average=0;
        for j in range(1):
            # starting timer - 시작 타이머
            screens.clear_area()
            print("\033[3;32HRound: " + str(j+1))
            time.sleep(0.1)
            print("\033[4;32HStarting in")
            time.sleep(0.5)
            for i in range(3):
                print("\033[4;43H " + str(3-i))
                time.sleep(0.5)
                print("\033[4;43H    ")
                time.sleep(0.5)

            screens.clear_area()
            start_time = time.time()
            print("\033[4;20H\033[K")
            if (mode == '1'):  # Numbers - 숫자 출력
                #난수 생성
                templ=random.randint(100000, 999999)
            elif (mode == '2'):  # Words - 단어 출력
                with open('words.txt', 'r') as file:
                    words = file.read().replace(',', '').split()
                templ = random.choice(words)
            elif (mode == '3'):  # Sentences - 문장 출력
                with open('sentences.txt', 'r') as file:
                    sentences = [sentence.strip() for sentence in file.read().replace('?', '.').split('.') if sentence]
                templ = random.choice(sentences) + '.'

            # input - 입력 받기
            answer=""
            while(str(answer) != str(templ)):
                # empty space
                for i in range(2, 7):
                    print(f"\033[{i};2H\033[K")

                # print template + input answer
                if(mode == '3'):
                    print("\033[3;15H\033[1m" + str(templ))
                    answer = input("\033[0m\033[6;15H>")
                else:
                    print("\033[3;37H\033[1m" + str(templ))
                    answer = input("\033[0m\033[6;37H>")

                # check answer
                if(str(answer) != str(templ)):
                    print("\033[3;37H\033[31m" + str(templ))
                    time.sleep(0.1)
                    print("\033[3;37H\033[39m" + str(templ))

            # print time
            end_time=time.time()
            average+=end_time - start_time
            print("\033[3;37HCorrect!\033[4;37HTime: {:.2f}".format(end_time-start_time))
            time.sleep(0.3)

        time.sleep(0.5)
        #average/=5;
        screens.clear_area()
        print("\033[3;32HGood Game!")
        print("\033[4;32HAverage time: {:.2f}".format(average))


        #open scoreboard.txt
        #check numbers of i in  range(0 to 2): mode+i*3
        #if numbers from scoreboard are bigger than average then swap number
        # repeat until end of range
        with open('scoreboard.txt', 'r+') as file:
            scores = file.read().replace(',', '').split()
            for i in range(3):
                index = (int(mode) - 1) + i * 3
                if float(scores[index]) > float(average):
                    formatted_average = "{:.2f}".format(average)
                    scores[index], formatted_average = formatted_average, scores[index]
                    average = float(formatted_average)

            file.seek(0)
            file.write(', '.join(scores[:3]) + '\n' + ', '.join(scores[3:6]) + '\n' + ', '.join(scores[6:]))
            file.truncate()
            time.sleep(1)

    print("\033[10;37H")
    #debug use break
    # break;
