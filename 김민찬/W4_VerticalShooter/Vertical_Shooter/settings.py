import pygame

# Display settings
WIDTH, HEIGHT = 1000, 600
WINDOW_TITLE = "Shooter"

# Asset paths
ASSET_PATHS = {
    "background": "../texture/pixel_sky.png",
    "spaceship": "../texture/spaceship.png",
    "bullet": "../texture/missile.png",
    "enemy": "../texture/ufo.png",
    "explosion": "../texture/explosion.png",
    "death": "../texture/death.png"
}

# Initialize display
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
