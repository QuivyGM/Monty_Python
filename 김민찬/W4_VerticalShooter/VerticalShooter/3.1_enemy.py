import pygame
import random

pygame.init()
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")

# Set up display
width, height = 1000, 600
window = pygame.display.set_mode((width, height))
background = pygame.transform.scale(pygame.image.load('pixel_sky.png'), (width, height))
pygame.display.set_caption("Move Object with Controller")

# Set up object
spaceship_image = pygame.image.load('spaceship.png')
scale_factor = 0.3
object_image = pygame.transform.scale(spaceship_image, (spaceship_image.get_width() * scale_factor, spaceship_image.get_height() * scale_factor))
object_x, object_y = width // 2, height // 2
object_speed = 5

# Bullet properties
bullet_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('missile.png'), (45, 15)), 90)  # 총알 이미지
bullet_speed = 10                       # 총알 속도
bullets = []                            # 실행 중인 총알 리스트

# Cooldown properties
last_shot_time = 0  # Initialize the last shot time
cooldown = 500  # Cooldown time in milliseconds - tick은

#-------------------------- enemy setting --------------------------#
# Enemy properties
enemy_image = pygame.transform.scale(pygame.image.load('enemy.png'), (50, 50))  # Load and scale enemy image
enemy_speed = 2
enemies = []  # List to store active enemies
enemy_spawn_time = 2000  # Time between spawns in milliseconds
last_enemy_spawn = pygame.time.get_ticks()
#------------------------------------------------------------------------------------#

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controller input
    if pygame.joystick.get_count() > 0:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        # Move the object based on the joystick position
        if abs(axis_x) > 0.1:
            object_x += int(axis_x * object_speed)
        if abs(axis_y) > 0.1:
            object_y += int(axis_y * object_speed)

        # Shooting with button 5
        if joystick.get_button(5):
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > cooldown:
                last_shot_time = current_time
                bullet_x = object_x + object_image.get_width() // 2 - bullet_image.get_width() // 2
                bullet_y = object_y
                bullets.append([bullet_x, bullet_y])  # Add the bullet to the list

    object_x = max(0, min(width - object_image.get_width(), object_x))
    object_y = max(0, min(height - object_image.get_height(), object_y))

    # -------------------------- enemy rendering --------------------------#
    # Enemy spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        last_enemy_spawn = current_time
        enemy_x = random.randint(0, width - enemy_image.get_width())  # Random x position
        enemy_y = -enemy_image.get_height()  # Start above the screen
        enemies.append([enemy_x, enemy_y])  # Add new enemy to the list
    # -------------------------- enemy move --------------------------#
    # Move enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed  # Move enemy downward
        if enemy[1] > height:  # Remove enemy if it goes off the screen
            enemies.remove(enemy)
    # ----------------------------------------------------------------------#

    # Render background and object
    window.blit(background, (0, 0))

    # Render bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        window.blit(bullet_image, (bullet[0], bullet[1]))
        if bullet[1] < 0:
            bullets.remove(bullet)
    window.blit(object_image, (object_x, object_y))

    #-------------------------- enemy rendering --------------------------#
    # Render enemies
    for enemy in enemies:
        window.blit(enemy_image, (enemy[0], enemy[1]))
    #----------------------------------------------------------------------#

    window.blit(object_image, (object_x, object_y))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()