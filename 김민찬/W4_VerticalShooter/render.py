import pygame

def renderFrame(window, background, bullets, bullet_image, enemies, enemy_image, explosions, explosion_image, user_image, user_x, user_y, bullet_speed):
    # Background
    window.blit(background, (0, 0))

    # Bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        window.blit(bullet_image, (bullet[0], bullet[1]))
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Enemies
    for enemy in enemies:
        window.blit(enemy_image, (enemy[0], enemy[1]))

    # Explosions
    for explosion in explosions[:]:
        elapsed_time = pygame.time.get_ticks() - explosion[2]

        # Calculate size based on elapsed time (e.g., grow from 50 to 150 pixels)
        scale = 50 + (elapsed_time / 500) * 100  # Scale grows from 50 to 150 over 500ms
        scaled_image = pygame.transform.scale(explosion_image, (int(scale), int(scale)))

        # Adjust position to center the growing explosion
        scaled_rect = scaled_image.get_rect(center=(explosion[0] + explosion_image.get_width() // 2,
                                                    explosion[1] + explosion_image.get_height() // 2))

        window.blit(scaled_image, scaled_rect.topleft)

        # Remove explosion after 500 ms
        if elapsed_time > 500:  # Explosion lasts 500 ms
            explosions.remove(explosion)

    # Player
    window.blit(user_image, (user_x, user_y))
    pygame.display.flip()

def game_over(window, background, object_image, explosion_image, width, height, object_x, object_y, death_type):
    death_image = pygame.image.load('death.png')
    for alpha in range(0, 256, 5):  # Gradually increase alpha value = 투명도(0부터 255까지 5씩 증가)
        death_image.set_alpha(alpha)
        window.blit(background, (0, 0))  # Redraw background
        if death_type == "enemy collision":
            window.blit(explosion_image, (object_x, object_y))
        else:
            window.blit(object_image, (object_x, object_y))

        window.blit(death_image, (width // 2 - 264, height // 2 - 264))
        pygame.display.flip()
        pygame.time.delay(30)  # Delay to control fade-in speed
