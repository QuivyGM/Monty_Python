import pygame
import random

pygame.init()

# ------------------------ 컨트롤러 init 및 입력 확인  ------------------------#
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")
    # ------------------------------------------------------------------------------------#

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move Object with Controller")

background = pygame.transform.scale(pygame.image.load('sky.webp'), (width, height))




# Set up object
object_color = (255, 0, 0)
object_size = 50
object_x, object_y = width // 2, height // 2
object_speed = 5

bullet_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('bullet.jpg'),(45,15)), 180)
bullet_speed = 10
bullets = []

last_shoot_time = 0
cooldown = 100
object_image = pygame.transform.scale(pygame.image.load('ultraman.png'), (object_size, object_size))

enemy_image = pygame.transform.scale(pygame.image.load('ultraman.png'), (50,50))
enemy_speed = 2
enemies = []
enemy_spawn_time = 2000
last_enemy_spawn = pygame.time.get_ticks()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ------------------------ 컨트롤러 입력으로 변경  ------------------------#
    # Controller input
    if pygame.joystick.get_count() > 0:  # Check if a joystick is connected
        # Get the axis values (-1 to 1)
        axis_x = joystick.get_axis(0)  # Left stick horizontal
        axis_y = joystick.get_axis(1)  # Left stick vertical

        # Move the object based on the joystick position
        if abs(axis_x) > 0.1:  # Dead zone to ignore small inputs
            object_x += int(axis_x * object_speed)
        if abs(axis_y) > 0.1:  # Dead zone
            object_y += int(axis_y * object_speed)
        if joystick.get_button(0):

            current_time = pygame.time.get_ticks()
            if current_time - last_shoot_time > cooldown:
                last_shoot_time = current_time

                bullet_x = object_x + object_image.get_width() // 2 - bullet_image.get_width() // 2
                bullet_y = object_y
                bullets.append([bullet_x, bullet_y])

    # Keep the object within the screen bounds
    object_x = max(0, min(width - object_size, object_x))
    object_y = max(0, min(height - object_size, object_y))
    # ------------------------------------------------------------------------------------#
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        last_enemy_spawn = current_time
        enemy_x = random.randint(0, width - enemy_image.get_width())
        enemy_y = -enemy_image.get_height()
        enemies.append([enemy_x, enemy_y])

    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > height:

            running = False


    for bullet in bullets[:]:
            for enemy in enemies[:]:

                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_image.get_width(), bullet_image.get_height())
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())

                if bullet_rect.colliderect(enemy_rect):
                    
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

    window.blit(background, (0,0))
    window.blit(object_image, (object_x, object_y))

    for bullet in bullets[:]:
        bullet[1] -= bullet_speed

        window.blit(bullet_image, (bullet[0],bullet[1]))

        if bullet[1] < 0:
            bullets.remove(bullet)

    for enemy in enemies:
        window.blit(enemy_image, (enemy[0], enemy[1]))
    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()