import pygame

pygame.init()
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")

# Set up display
width, height = 1000, 600
window = pygame.display.set_mode((width, height))
# background = pygame.image.load('pixel_sky.png')
background = pygame.transform.scale(pygame.image.load('pixel_sky.png'), (width, height))
pygame.display.set_caption("Move Object with Controller")

# Set up object
spaceship_image = pygame.image.load('spaceship.png')
scale_factor = 0.3
object_image = pygame.transform.scale(spaceship_image, (spaceship_image.get_width() * scale_factor, spaceship_image.get_height() * scale_factor))
object_x, object_y = width // 2, height // 2
object_speed = 5

# ------------------------ 마사일 발사에 텍스쳐 적용  ------------------------#
# Bullet properties
bullet_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('missile.png'), (45, 15)), 90)  # 총알 이미지
bullet_speed = 10                       # 총알 속도
bullets = []                            # 실행 중인 총알 리스트
# ------------------------------------------------------------------------------------#

# Cooldown properties
last_shot_time = 0  # Initialize the last shot time
cooldown = 500  # Cooldown time in milliseconds - tick은

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controller input
    if pygame.joystick.get_count() > 0:  # Check if a joystick is connected
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        # Move the object based on the joystick position
        if abs(axis_x) > 0.1:
            object_x += int(axis_x * object_speed)
        if abs(axis_y) > 0.1:
            object_y += int(axis_y * object_speed)

        # Shooting with button 5
        if joystick.get_button(5):  # Button 5 is pressed
            # ------------------------ 마사일 발사하는데 쿨타임 적용  ------------------------#
            current_time = pygame.time.get_ticks()  # time 모듈 대신 이용 -> pygame이 init한지 얼마나 되었는지를 밀리세컨드로 반환
            if current_time - last_shot_time > cooldown:  # 시간확인: 마지막 총알 발사 시간과 현재 시간을 비교하여 쿨타임을 확인
                last_shot_time = current_time  # 마지막으로 총알을 발사한 시간을 현재 시간으로 업데이트
                # ------------------------------------------------------------------------------------#
                bullet_x = object_x + object_image.get_width() // 2 - bullet_image.get_width() // 2  # width 대신 get_width()로 변경
                bullet_y = object_y
                bullets.append([bullet_x, bullet_y])  # Add the bullet to the list

    object_x = max(0, min(width - object_image.get_width(), object_x))
    object_y = max(0, min(height - object_image.get_height(), object_y))

    # Render background and object
    window.blit(background, (0, 0))


    # Render bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        #-------------------------- 총알 그리기 draw -> blit으로 변경 --------------------------#
        window.blit(bullet_image, (bullet[0], bullet[1]))  # 총알을 이미지로 그리기
        #------------------------------------------------------------------------------------#
        if bullet[1] < 0:
            bullets.remove(bullet)
    #------------------------ 오브젝트를 미사일 아래에 두도록 순서 변경  ------------------------#
    window.blit(object_image, (object_x, object_y))
    # ------------------------------------------------------------------------------------#



    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()