import pygame
import random
import render

pygame.init()
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")

#-------------------------------------- object settings --------------------------------------#
# Set up display
width, height = 1000, 600
window = pygame.display.set_mode((width, height))
background = pygame.transform.scale(pygame.image.load('pixel_sky.png'), (width, height))
pygame.display.set_caption("Shooter")

# Set up User
spaceship_image = pygame.image.load('spaceship.png')
scale_factor = 0.3
user_image = pygame.transform.scale(spaceship_image, (spaceship_image.get_width() * scale_factor, spaceship_image.get_height() * scale_factor))
user_x, user_y = width // 2, height // 2
user_speed = 10
user_visible = True

# Set up Bullet
bullet_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('missile.png'), (45, 15)), 90)  # 총알 이미지
bullet_speed = 10                       # 총알 속도
bullets = []                            # 실행 중인 총알 리스트
# Bullet Cooldown
last_shot_time = 0  # Initialize the last shot time
cooldown = 500  # Cooldown time in milliseconds - tick은

# Enemy properties
enemy_image = pygame.transform.scale(pygame.image.load('enemy.png'), (50, 50))  # Load and scale enemy image
enemy_speed = 2
enemies = []  # List to store active enemies
enemy_spawn_time = 1000  # Time between spawns in milliseconds
last_enemy_spawn = pygame.time.get_ticks()

# Explosion properties
explosion_image = pygame.transform.scale(pygame.image.load('explosion.png'), (50, 50))
explosions = []  # List of active explosions

#------------------------------------ game loop --------------------------------------#

# Main loop
running = True
while running:
    #-------------------------------------- event handling(user data) --------------------------------------#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controller input
    if pygame.joystick.get_count() > 0:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        # Move the object based on the joystick position
        if abs(axis_x) > 0.1:
            user_x += int(axis_x * user_speed)
        if abs(axis_y) > 0.1:
            user_y += int(axis_y * user_speed)

        # Shooting with button 5
        if joystick.get_button(5):
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > cooldown:
                last_shot_time = current_time
                bullet_x = user_x + user_image.get_width() // 2 - bullet_image.get_width() // 2
                bullet_y = user_y
                bullets.append([bullet_x, bullet_y])  # Add the bullet to the list

    user_x = max(0, min(width - user_image.get_width(), user_x))
    user_y = max(0, min(height - user_image.get_height(), user_y))

    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemy_x = random.randint(0, width - enemy_image.get_width())
        enemy_y = -enemy_image.get_height()
        enemies.append([enemy_x, enemy_y])
        last_enemy_spawn = current_time

    # Move enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > height:
            death_type = "defense failure"
            running = False
            break

    # Check Enemy-Player Collisions
    player_rect = pygame.Rect(user_x, user_y, user_image.get_width(), user_image.get_height())
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())
        if player_rect.colliderect(enemy_rect):
            death_type = "enemy collision"
            running = False
            break

    # Check Bullet-Enemy Collisions
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_image.get_width(), bullet_image.get_height())
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())
            if bullet_rect.colliderect(enemy_rect):
                explosions.append([enemy[0], enemy[1], pygame.time.get_ticks()])
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Render everything using the imported function
    render.renderFrame(window, background, bullets, bullet_image, enemies, enemy_image, explosions, explosion_image, user_image, user_x, user_y, bullet_speed)

    if running == False:
        render.game_over(window, background, user_image, explosion_image, width, height, user_x, user_y, death_type)
        event = pygame.event.wait()  # Wait for user input to end

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()