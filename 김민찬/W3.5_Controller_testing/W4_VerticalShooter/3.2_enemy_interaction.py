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

# Enemy properties
enemy_image = pygame.transform.scale(pygame.image.load('enemy.png'), (50, 50))  # Load and scale enemy image
enemy_speed = 2
enemies = []  # List to store active enemies
enemy_spawn_time = 2000  # Time between spawns in milliseconds
last_enemy_spawn = pygame.time.get_ticks()

#-------------------------- explosion setting --------------------------#
# Explosion properties
explosion_image = pygame.transform.scale(pygame.image.load('explosion.png'), (50, 50))
explosions = []  # List of active explosions
#-----------------------------------------------------------------------#

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

    # Enemy spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        last_enemy_spawn = current_time
        enemy_x = random.randint(0, width - enemy_image.get_width())  # Random x position
        enemy_y = -enemy_image.get_height()  # Start above the screen
        enemies.append([enemy_x, enemy_y])  # Add new enemy to the list

    # Move enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed  # Move enemy downward
        if enemy[1] > height:  # Remove enemy if it goes off the screen
            #----------------------------- game over -----------------------------#
            # font = pygame.font.Font(None, 74)
            # game_over_text = font.render("Game Over", True, (255, 0, 0))
            # window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
            #----------------------------- game over -----------------------------#
            render.game_over(window, background, object_image, width, height, object_x, object_y)
            event = pygame.event.wait()  # Wait for user input to end
            running = False
            #---------------------------------------------------------------------#

    #-------------------------- bullet-enemy check --------------------------#
    # Check for bullet-enemy collisions
    for bullet in bullets[:]:       # 모든 총알에 대해 순회
        for enemy in enemies[:]:    # 모든 적에 대해 순회
            # 사각형을 그리는 이유는 충돌을 확인하기 위함
            # 총알과 적의 사각형을 만들어서 충돌을 확인
            # = hit box
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_image.get_width(), bullet_image.get_height())
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())
            # 충돌 확인
            if bullet_rect.colliderect(enemy_rect):  # Check collision
                explosions.append([enemy[0], enemy[1], pygame.time.get_ticks()])  # Add explosion
                bullets.remove(bullet)
                enemies.remove(enemy)
                break
    #---------------------------------------------------------------------#
    player_rect = pygame.Rect(object_x, object_y, object_image.get_width(), object_image.get_height())
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())
        if player_rect.colliderect(enemy_rect):  # Collision detected
            render.game_over(window, background, object_image, width, height, object_x, object_y)
            event = pygame.event.wait()  # Wait for user input to end
            running = False
    #-------------------------- enemy-player check --------------------------#

    # ---------------------------------------------------------------------#

    # Render background and object
    window.blit(background, (0, 0))

    # Render bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        window.blit(bullet_image, (bullet[0], bullet[1]))
        if bullet[1] < 0:
            bullets.remove(bullet)
    window.blit(object_image, (object_x, object_y))

    # Render enemies
    for enemy in enemies:
        window.blit(enemy_image, (enemy[0], enemy[1]))

    #-------------------------- explosion rendering --------------------------#
    # Render explosions
    for explosion in explosions[:]:
        window.blit(explosion_image, (explosion[0], explosion[1]))
        # Remove explosion after a short time
        if pygame.time.get_ticks() - explosion[2] > 500:  # Explosion lasts 500 ms
            explosions.remove(explosion)
    #--------------------------------------------------------------------------#

    window.blit(object_image, (object_x, object_y))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()