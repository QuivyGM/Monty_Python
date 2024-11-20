import pygame

# Initialize Pygame
# initializing = setting up/preparing the module for use
# reasons: resource efficiency (memory/processing power etc), modularity, error handling(detect and report)
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))   # set the width and height of the window as 800 pixels and 600 pixels
pygame.display.set_caption("Move Object with Keyboard") # set window title as "Move Object with Keyboard"

# Set up object
object_color = (255, 0, 0)  # tuple: set the color as RGB values (R, G, B)
# tuple: 바뀔수 없는 값들의 집합(읽기 전용), 저장 타입이 다를 수가 있음            ex) (1, 'apple', 3.14)    -> my_tuple[1] == 'apple'
# <-> list: 바뀔 수 있는 값들의 집합, 저장 타입 상관 없음                       ex) [1, 'banana', 2.5]    -> my_list[1] == 'banana'
# <-> set:  바뀔 수 있는 값들의 집합, 저장 타입 상관 없음, 중복을 허용하지 않음    ex) {1, 2, 3}       -> (set은 순서가 없음) -> set에서 인덱싱 불가능: list으로 변환(list = list(set)) 아니면 전체 순회
# <-> dictionary: key-value pair의 집합, key는 바뀔 수 없는 값, value는 바뀔 수 있는 값 ex) {first_fruit: 'apple', 2: 'banana'} -> my_dict[first_fruit] == 'apple'
# <-> array: 바뀔 수 있는 값들의 집합, 같은 타입 ex) array('i', [1, 2, 3]) (i: interger - data type)      -> my_array[1] == 2
# 각자 이용 상황: tuple - 함수의 리턴값, list - 데이터 추가/삭제가 빈번한 경우, set - 중복을 허용하지 않는 경우, dictionary - key-value pair가 필요한 경우, array - 같은 타입의 데이터를 다루는 경우
object_size = 50    # set the size of the object as 50 pixels
object_x, object_y = width // 2, height // 2 # set object position as object_x, object_t (center of the window)
object_speed = 5    # set the speed of the object as 5 (pixels)

# Main loop
# 계속해서 업데이트를 받아햐 하기 때문에 무한 루프를 돌아야 함
running = True
while running:
    # 이벤트 란: 사용자가 키보드나 마우스를 클릭하는 등의 동작등을 말함 (또 다른 예로는 윈도우 창을 닫는 동작, 화면 크기를 변경하는 동작 등)
    # pygame.event module: pygame에서 발생하는 이벤트를 처리하기 위한 클래스와 함수를 제공
    # pygame.event.get(): 이벤트를 가져오는
    for event in pygame.event.get():    # 반복문은 이벤트를 가져오는 것을 반복함

        # 제일 먼저 해야하는 것: 윈도우 창을 닫는 동작을 처리
        # 그 이유는: 윈도우 창을 닫는 동작은 다른 동작보다 먼저 처리되어야 하기 때문
        if event.type == pygame.QUIT:  # 이벤트의 종류가 QUIT(윈도우 창을 닫는 동작)이면
            running = False            # running을 False로 바꾸어서 루프를 빠져나옴

    # 키보드 입력 처리
    # pygame.key module: 키보드 입력을 처리하기 위한 클래스와 함수를 제공
    # pygame.key.get_pressed(): 눌려진 키를 가져오는
    keys = pygame.key.get_pressed()   # 눌려진 키를 가져옴

    # 종료 키 처리
    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_LEFT]:           # 만약 왼쪽 방향키가 눌렸다면
        object_x -= object_speed    # object_x를 object_speed만큼 감소시킴 (속도라고 표현을 하였지만 사실상 위치를 변경하는 것)
    if keys[pygame.K_RIGHT]:
        object_x += object_speed
    if keys[pygame.K_UP]:
        object_y -= object_speed
    if keys[pygame.K_DOWN]:
        object_y += object_speed
    # wasd로 하고 싶으면: pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s
    # if keys[pygame.K_a]:           # 만약 a 키가 눌렸다면
    #     object_x -= object_speed    # object_x를 object_speed만큼 감소시킴 (속도라고 표현을 하였지만 사실상 위치를 변경하는 것)
    # if keys[pygame.K_d]:
    #     object_x += object_speed
    # if keys[pygame.K_w]:
    #     object_y -= object_speed
    # if keys[pygame.K_s]:
    #     object_y += object_speed


    # 오브젝트가 화면을 벗어나지 않도록 처리
    object_x = max(0, min(width - object_size, object_x)) # min(width - object_size, object_x) 는 가로 길이에서 object_size를 뺀 값과 object_x 중 작은 값을 선택
    object_y = max(0, min(height - object_size, object_y)) # min(height - object_size, object_y) 는 세로 길이에서 object_size를 뺀 값과 object_y 중 작은 값을 선택



    # 윈도우를 검은색으로 채움
    # 안하면 이전에 그려진 것이 남아있음 = 이 용도는 이전 프레임을 지우는 것
    window.fill((0, 0, 0))

    # 오브젝트 그리기
    # pygame.draw module: 도형을 그리기 위한 클래스와 함수를 제공
    # pygame.draw.rect(): 사각형을 그리는
    # pygame.draw.rect(어디에 그릴지: window, 색깔: object_color, (x좌표, y좌표, 가로길이, 세로길이))
    pygame.draw.rect(window, object_color, (object_x, object_y, object_size, object_size))

    # 화면을 업데이트
    # 화면을 업데이트 하는 이유: 화면에 그려진 것을 보여주기 위함
    # pygame.display module: 화면을 업데이트 하기 위한 클래스와 함수를 제공
    # pygame.display.flip(): 화면을 업데이트 하는
    pygame.display.flip()

    # 프레임 설정
    # 없이는 컴퓨터가 제공하는대로 프레임이 나오기 때문에 설정을 해주어서 자원 낭비를 줄임
    # pygame.time module: 시간을 다루기 위한 클래스와 함수를 제공
    # pygame.time.Clock(): 시간을 다루기 위한 클래스
    # tick(60): tick을 최대 60으로 설정 = 60fps 설정
    # tick이란: 게임 스테이트 하고 렌더링 의 한 사이클을 의미
    pygame.time.Clock().tick(60)

pygame.quit()