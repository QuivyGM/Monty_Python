# ------------------------------------
# Imports and Settings
# ------------------------------------
import pygame, sys, time

# Constants for window dimensions and framerate
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 504
FRAMERATE = 60

# ------------------------------------
# Sprites: Background, Ground, Plane
# ------------------------------------
class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('images/background.png').convert()

        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        ground_surf = pygame.image.load('images/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)

        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)


class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.gravity = 600
        self.direction = 0
        self.on_ground = False

        self.mask = pygame.mask.from_surface(self.image)

        self.jump_sound = pygame.mixer.Sound('images/jump.wav')
        self.jump_sound.set_volume(0.3)

    def import_frames(self, scale_factor):
        self.frames = []

        surf = pygame.image.load(f'images/flappy_bird.png').convert_alpha()
        scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * (scale_factor / 6))
        self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt

        # Prevent the plane from going below the ground
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.pos.y = WINDOW_HEIGHT - self.rect.height
            self.direction = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

# ------------------------------------
# Main Game Class
# ------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True

        self.all_sprites = pygame.sprite.Group()

        bg_height = pygame.image.load('images/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        self.font = pygame.font.Font('images/flappy-font.ttf', 30)
        self.score = 0
        self.start_offset = 0

        self.menu_surf = pygame.image.load('images/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.music = pygame.mixer.Sound('images/music.wav')
        self.music.play(loops=-1)

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if not self.active:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()

# ------------------------------------
# Entry Point
# ------------------------------------
if __name__ == '__main__':
    game = Game()
    game.run()
