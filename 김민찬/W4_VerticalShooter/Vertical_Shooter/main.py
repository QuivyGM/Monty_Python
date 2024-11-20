import pygame
from settings import WINDOW, WIDTH, HEIGHT, ASSET_PATHS
from render import renderFrame, game_over
from game_objects import User, Bullet, Enemy, Explosion

def main():
    # Load assets
    background = pygame.transform.scale(
        pygame.image.load(ASSET_PATHS["background"]),
        (WIDTH, HEIGHT)
    )

    # Initialize objects
    user = User(WIDTH // 2, HEIGHT // 2, 10, ASSET_PATHS["spaceship"])
    bullets = []
    enemies = []
    explosions = []

    # Timing
    last_shot_time = 0
    cooldown = 500
    last_enemy_spawn = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    running = True

    # GAME LOOP
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        user.move(keys)
        user.restrict_bounds(WIDTH, HEIGHT)

        # Bullet firing
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > cooldown:
                last_shot_time = current_time
                bullets.append(
                    Bullet(
                        user.x + user.image.get_width() // 2 - 45 // 2,
                        user.y,
                        10,
                        ASSET_PATHS["bullet"],
                    )
                )

        # Enemy spawning
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn > 1000:
            enemies.append(Enemy.spawn(WIDTH, ASSET_PATHS["enemy"]))
            last_enemy_spawn = current_time

        # Collision detection
        for enemy in enemies[:]:
            enemy.move()
            if enemy.y > HEIGHT:
                running = False

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.image.get_width(), bullet.image.get_height())
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())

                if bullet_rect.colliderect(enemy_rect):
                    explosions.append(Explosion(enemy.x, enemy.y, current_time, ASSET_PATHS["explosion"]))
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        renderFrame(WINDOW, background, bullets, enemies, explosions, user)
        clock.tick(60)

    game_over(WINDOW, background, user, ASSET_PATHS["explosion"], "enemy collision")
    pygame.quit()

if __name__ == "__main__":
    main()
