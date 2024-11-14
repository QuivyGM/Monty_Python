import pygame
import random

# Initialize pygame and controller
pygame.init()
pygame.joystick.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders with Controller Support")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Game variables
player_width, player_height = 60, 20
player_x, player_y = width // 2, height - player_height - 10
player_speed = 5

# Bullet variables
bullets = []
bullet_speed = 10
bullet_size = 5
bullet_timer = 0  # Timer for controlling shooting rate
shooting_cooldown = 10  # Frames between each shot while holding trigger

# Enemy variables
enemy_width, enemy_height = 40, 30
enemies = []
enemy_speed = 1
spawn_rate = 30  # Higher value means fewer spawns

# Score
score = 0
font = pygame.font.Font(None, 36)

# Controller check
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No controller found. Connect a controller and restart the game.")
    pygame.quit()
    quit()

# Game loop
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controller input for movement
    if joystick.get_numaxes() > 0:
        axis_x = joystick.get_axis(0)  # Left thumbstick horizontal movement
        player_x += int(axis_x * player_speed)

    # Keep player within screen bounds
    player_x = max(0, min(width - player_width, player_x))

    # Continuous shooting with right trigger (R2 button)
    if joystick.get_numaxes() > 5:  # Check if axis 5 is available
        right_trigger = joystick.get_axis(5)
        if right_trigger > 0.5:  # Pressed down halfway or more
            bullet_timer += 1
            if bullet_timer >= shooting_cooldown:
                bullets.append([player_x + player_width // 2, player_y])
                bullet_timer = 0
        else:
            bullet_timer = shooting_cooldown  # Reset timer if trigger is released

    # Move and draw bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        pygame.draw.circle(screen, white, (int(bullet[0]), int(bullet[1])), bullet_size)
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Enemy spawning
    if random.randint(1, spawn_rate) == 1:
        enemy_x = random.randint(0, width - enemy_width)
        enemies.append([enemy_x, 0])

    # Move enemies and check for collision with player bullets
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        pygame.draw.rect(screen, red, (enemy[0], enemy[1], enemy_width, enemy_height))

        # Check for collision with bullets
        for bullet in bullets[:]:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_width and
                    enemy[1] < bullet[1] < enemy[1] + enemy_height):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

        # Check if enemy reaches the bottom (game over scenario)
        if enemy[1] > height:
            running = False
            print("Game Over! Final Score:", score)

    # Draw player
    pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))

    # Display score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Update display and frame rate
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
