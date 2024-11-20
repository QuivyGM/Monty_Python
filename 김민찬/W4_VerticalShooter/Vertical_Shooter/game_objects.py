import pygame
import random

class User:
    def __init__(self, x, y, speed, image_path):
        self.x = x
        self.y = y
        self.speed = speed
        raw_image = pygame.image.load(image_path)
        scale_factor = 0.3
        self.image = pygame.transform.scale(
            raw_image,
            (int(raw_image.get_width() * scale_factor), int(raw_image.get_height() * scale_factor))
        )

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def restrict_bounds(self, width, height):
        self.x = max(0, min(width - self.image.get_width(), self.x))
        self.y = max(0, min(height - self.image.get_height(), self.y))


class Bullet:
    def __init__(self, x, y, speed, image_path):
        raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.rotate(
            pygame.transform.scale(raw_image, (45, 15)), 90
        )
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y -= self.speed

    def is_off_screen(self, height):
        return self.y < 0


class Enemy:
    def __init__(self, x, y, speed, image_path):
        raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(raw_image, (100, 100))
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed

    @staticmethod
    def spawn(width, image_path):
        x = random.randint(0, width - 100)  # 50 = Enemy width
        y = -50  # Spawn just above the screen
        return Enemy(x, y, 1, image_path)


class Explosion:
    def __init__(self, x, y, start_time, image_path):
        raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(raw_image, (50, 50))
        self.x = x
        self.y = y
        self.start_time = start_time

    def has_expired(self, current_time, duration=500):
        return current_time - self.start_time > duration
