import pygame
import os
from . import const

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, '..', 'asset', 'playershot.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 15))
        except Exception as e:
            print(f"Erro ao carregar imagem do PlayerShot: {e}")
            self.image = pygame.Surface((30, 15), pygame.SRCALPHA)
            self.image.fill((255, 255, 0))  # amarelo como fallback

        self.rect = self.image.get_rect(center=position)
        self.speed = 300
        self.direction = direction
        self.damage = 25
        self.owner = "player"

    def update(self, delta_time):
        self.rect.x += self.speed * self.direction * delta_time
        if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH:
            self.kill()

    def draw(self, surface, camera_offset_x):
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))
