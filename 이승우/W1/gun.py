import pygame
import random
import render

pygame.init()

pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
background = pygame.transform.scale(pygame.image.load('우주.jpg'), (width, height))

pygame.display.set_caption("Move object with keyboard")
object_color = (255, 0, 0)
object_size = 50
object_image = pygame.transform.scale(pygame.image.load('jet.png'), (object_size, object_size))
object_x, object_y = width // 2, height // 2
object_speed = 10

bullet_image = pygame.transform.scale(pygame.image.load('bullet.png'), (60, 60))
bullet_speed = 20
bullets = []

boom_image = pygame.transform.scale(pygame.image.load('boom.png'), (50, 50))
booms = []

last_shot_time = 0
cooldown = 500

enemy_image = pygame.transform.scale(pygame.image.load('enemy.png'), (30, 30))
enemy_speed = 1
enemies = []
enemy_spawn_time = 2000
last_enemy_spawn = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if pygame.joystick.get_count() > 0:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if abs(axis_x) > 0.1:
            object_x += int(axis_x * object_speed)
        if abs(axis_y) > 0.1:
            object_y += int(axis_y * object_speed)
        if joystick.get_button(5):
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > cooldown:
                last_shot_time = current_time
                bullet_x = object_x + object_image.get_width() // 2 - bullet_image.get_width() // 2
                bullet_y = object_y
                bullets.append([bullet_x, bullet_y])

    if keys[pygame.K_LEFT]:
        object_x -= object_speed
    if keys[pygame.K_RIGHT]:
        object_x += object_speed
    if keys[pygame.K_UP]:
        object_y -= object_speed
    if keys[pygame.K_DOWN]:
        object_y += object_speed

    if keys[pygame.K_k]:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > cooldown:
            last_shot_time = current_time
            bullet_x = object_x + object_image.get_width() // 2 - bullet_image.get_width() // 2
            bullet_y = object_y
            bullets.append([bullet_x, bullet_y])

    object_x = max(0, min(width - object_size, object_x))
    object_y = max(0, min(height - object_size, object_y))

    window.blit(background, (0, 0))
    window.blit(object_image, (object_x, object_y))

    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        last_enemy_spawn = current_time
        enemy_x = random.randint(0, width - enemy_image.get_width())
        enemy_y = -enemy_image.get_height()
        enemies.append([enemy_x, enemy_y])

    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > height:
            enemies.remove(enemy)
            death_type = "defense failure"
            running = False

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_image.get_width(), bullet_image.get_height())
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())

            if bullet_rect.colliderect(enemy_rect):
                booms.append([enemy[0], enemy[1], pygame.time.get_ticks()])
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    player_rect = pygame.Rect(object_x, object_y, object_image.get_width(), object_image.get_height())
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())

        if player_rect.colliderect(enemy_rect):
            death_type = "enemy collision"
            running = False
            break

    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        window.blit(bullet_image, (bullet[0], bullet[1]))

        if bullet[1] < 0:
            bullets.remove(bullet)

    for enemy in enemies:
        window.blit(enemy_image, (enemy[0], enemy[1]))

    for boom in booms[:]:
        left_time = pygame.time.get_ticks() - boom[2]
        scale = 50 + (left_time / 500) * 100
        scaled_image = pygame.transform.scale(boom_image, (int(scale), int(scale)))
        scaled_rect = scaled_image.get_rect(
            center=(boom[0] + boom_image.get_width() // 2, boom[1] + boom_image.get_height() // 2))
        window.blit(scaled_image, scaled_rect.topleft)

        if left_time > 500:
            booms.remove(boom)

    if running == False:
        render.game_over(window, background, object_image, boom_image, width, height, object_x, object_y, death_type)
        event = pygame.event.wait()  # Wait for user input to end

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()