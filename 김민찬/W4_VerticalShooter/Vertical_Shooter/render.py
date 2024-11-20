import pygame

def renderFrame(window, background, bullets, enemies, explosions, user):
    # Background
    window.blit(background, (0, 0))

    # Bullets
    for bullet in bullets[:]:
        bullet.move()
        window.blit(bullet.image, (bullet.x, bullet.y))
        if bullet.is_off_screen(window.get_height()):
            bullets.remove(bullet)

    # Enemies
    for enemy in enemies:
        window.blit(enemy.image, (enemy.x, enemy.y))

    # Explosions
    for explosion in explosions[:]:
        elapsed_time = pygame.time.get_ticks() - explosion.start_time
        scale = 50 + (elapsed_time / 500) * 100
        scaled_image = pygame.transform.scale(explosion.image, (int(scale), int(scale)))
        scaled_rect = scaled_image.get_rect(center=(explosion.x + explosion.image.get_width() // 2,
                                                    explosion.y + explosion.image.get_height() // 2))
        window.blit(scaled_image, scaled_rect.topleft)
        if explosion.has_expired(pygame.time.get_ticks()):
            explosions.remove(explosion)

    # Player
    window.blit(user.image, (user.x, user.y))
    pygame.display.flip()


def game_over(window, background, user, explosion_image_path, death_type):
    death_image = pygame.image.load('texture/death.png')
    explosion_image = pygame.image.load(explosion_image_path)

    for alpha in range(0, 256, 5):
        death_image.set_alpha(alpha)
        window.blit(background, (0, 0))
        if death_type == "enemy collision":
            window.blit(explosion_image, (user.x, user.y))
        else:
            window.blit(user.image, (user.x, user.y))

        window.blit(death_image, (window.get_width() // 2 - 264, window.get_height() // 2 - 264))
        pygame.display.flip()
        pygame.time.delay(30)
