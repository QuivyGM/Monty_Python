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


    #점수판 출력
    elif (mode == '4'):  # Scoreboard - 점수판 출력
        screens.clear_area()
        time.sleep(0.1)
        print("\033[2;22HNumbers\033[2;38HWords\033[2;52HSentences")
        time.sleep(0.1)
        print("\033[3;22H" + "*"*40)
        time.sleep(0.1)


        # f = open 대신 with open()으로 파일 열기 -> 개별적으로 close()을 할 필요가 없음
        with open('scoreboard.txt', 'r') as file:   # 파일 열기
            scores = file.read().replace(',', '').split()   #파일 내용을 "," 단위로 나누어 저장
            for i in range(3):  #score 전체 출력 (각 mode 마다 top 3만)
                print(f"\033[{4+i};24H{scores[i*3]}\033[{4+i};40H{scores[i*3+1]}\033[{4+i};56H{scores[i*3+2]}")
                time.sleep(0.1)
        input("\033[0m\033[7;29H[[Press Enter to return]]")     # 엔터를 치면 메인 메뉴로


    # 게임 모드일때
    else:
        # highlight selected mode   -   선택된 모드 깜빡이
        screens.highlight_mode(mode)

        #다섯번의 라운드
        round = 1
        j=0
        average=0

        # 라운드 시작
        for j in range(round):

            # 시작 카운트 다운
            screens.clear_area()
            print("\033[3;35HRound: " + str(j+1) + "/" + str(round)) # 라운드 갯수 출력
            time.sleep(0.1)
            print("\033[5;34HStarting in")          # 시작 카운트다운 글자 출력
            time.sleep(0.5)

            # 경기 카운트다운 숫자 출력
            for i in range(3):
                print("\033[5;46H"+ str(3-i))
                time.sleep(0.5)
                print("\033[5;46H ")
                time.sleep(0.5)


            # 랜덤 스트링 표시
            start_time = time.time()        # 타이머 시작 (시작 시간 저장)
            screens.clear_area()

            # Numbers - 숫자 출력
            if (mode == '1'):
                # templ에 6자리 숫자 저장
                templ=random.randint(100000, 999999)

            # Words - 단어 출력
            elif (mode == '2'):
                # words.txt에서 단어를 불러와서 랜덤으로 선택
                with open('words.txt', 'r') as file:
                    words = file.read().replace(',', '').split()    # 파일에 있는 단어들을 리스트로 저장
                templ = random.choice(words)    # 리스트에 랜덤으로 하나 정해서 templ에 저장

            # Sentences - 문장 출력
            elif (mode == '3'):
                # sentences.txt에서 문장을 불러와서 랜덤으로 선택
                with open('sentences.txt', 'r') as file:
                    # 문장 구분 단위는 '.' 으로 구분??
                    #sentences = [sentence.strip() + end for sentence in file.read().split('.') for end in ['.', '?'] if sentence.endswith(end)]
                    sentences = [sentence.strip() for sentence in file.read().split('.') if sentence]
                templ = random.choice(sentences) + '.'


            # input - 입력 받기
            answer=""       # 정답 초기화

            # 정답이 나올때까지 반복
            while(str(answer) != str(templ)):
                # 게임 공간 빠르게 비우기
                for i in range(2, 7):
                    print(f"\033[{i};2H\033[K")


                # 문제 출력 + 입력 받기
                templ_pos=(80-len(str(templ)))//2       #문제 길이에 따른 위치 계산
                print(f"\033[3;{templ_pos}H\033[1m" + str(templ))   # 문제 출력
                answer = input(f"\033[0m\033[5;{templ_pos-1}H>")    # 입렫 받기

                # 정답 틀리면: 글씨 빨간색 깜빡이기
                if(str(answer) != str(templ)):
                    for i in range(3):
                        print(f"\033[3;{templ_pos}H\033[31m" + str(templ))
                        time.sleep(0.1)
                        print(f"\033[3;{templ_pos}H\033[39m" + str(templ))
                        time.sleep(0.1)


            # 정답 맞기: 축하 + 시간 출력
            end_time = time.time()  # 종료 시간 저장
            average += end_time - start_time    # 시간 축적
            time_pos = (80 - len(str( end_time - start_time ))) // 2
            screens.clear_area()
            time.sleep(0.2)
            print("\033[3;36HCorrect!")
            time.sleep(0.2)
            print("\033[5;35HTime: {:.2f}".format(end_time - start_time))
            time.sleep(0.2)
            input("\033[0m\033[7;29H[[Press Enter to return]]")

        # 라운드 종료

        average /= round    # 평균 시간 계산
        screens.clear_area()
        for i in range(2):
            time.sleep(0.5)
            print("\033[3;36H\033[K")
            time.sleep(0.5)
            print("\033[3;36HGood Game!")
        for i in range(2):
            time.sleep(0.5)
            print("\033[5;32H\033[K")
            time.sleep(0.5)
            print("\033[5;32HAverage time: {:.2f}".format(average))
        time.sleep(1)
        input("\033[0m\033[7;29H[[Press Enter to return]]")


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

    print("\033[10;37H")
    #debug use break
    # break;
