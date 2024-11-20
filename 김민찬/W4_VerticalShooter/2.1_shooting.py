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
object_size = 100
object_image = pygame.transform.scale(pygame.image.load('spaceship.png'), (object_size, object_size))
object_x, object_y = width // 2, height // 2
object_speed = 5
# ------------------------ 총알 설정  ------------------------#
# Bullet properties
bullet_width, bullet_height = 10, 20    # 총알 크기
bullet_color = (255, 255, 0)            # 총알 색깔
bullet_speed = 10                       # 총알 속도
bullets = []                            # 실행 중인 총알 리스트
# ------------------------------------------------------------------------------------#

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

        # ------------------------ 총알 발사 버튼  ------------------------#
        # Shooting with button 5
        if joystick.get_button(5):  # Button 5 is pressed
            # Add a new bullet starting from the spaceship's position
            bullet_x = object_x + object_size // 2 - bullet_width // 2  # 총알의 x좌표를 중앙 맞품 (오브젝트의 좌표는 왼쪽 상단이기 때문)
            bullet_y = object_y
            bullets.append([bullet_x, bullet_y])    # 총알 리스트에 총알 추가 -> 총알은 [x좌표, y좌표]로 구성 = bullet[0]=x좌표, bullet[1]=y좌표
        # ------------------------------------------------------------------------------------#

        # Keep the object within the screen bounds
    object_x = max(0, min(width - object_size, object_x))
    object_y = max(0, min(height - object_size, object_y))

    # Render background and object
    window.blit(background, (0, 0))
    window.blit(object_image, (object_x, object_y))

    # ------------------------ 총알 그리기 연속해서  ------------------------#
    # Render bullets
    for bullet in bullets[:]:  # 총알 리스트를 복사해서 순회 - 이유는 총알을 삭제할 때 원본 리스트에 영향을 주지 않기 위함 - 영향을 주면 순회 중에 리스트가 변경되어 오류가 발생할 수 있음
        bullet[1] -= bullet_speed  # 총알의 y값 변경
        pygame.draw.rect(window, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))  # 총알을 그리기
        # 총알이 화면 밖으로 나가면 삭제
        if bullet[1] < 0:
            bullets.remove(bullet)
    # ------------------------------------------------------------------------------------#

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()