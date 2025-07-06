import os
import pygame

class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, position, enemy_type, direction=-1):
        super().__init__()
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, '..', 'asset', f'{enemy_type}shot.png')
            self.image = pygame.image.load(image_path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
            self.image.fill((255, 100, 100))

        self.rect = self.image.get_rect(center=position)
        self.speed = 400
        self.direction = direction
        self.enemy_type = enemy_type
        self.damage = 1

    def update(self, delta_time, camera_offset_x, screen_width):
        """
        Atualiza a posição do tiro e verifica se ele saiu da ÁREA VISÍVEL da câmera.
        """
        self.rect.x += self.speed * self.direction * delta_time

        if self.rect.right < camera_offset_x or self.rect.left > camera_offset_x + screen_width:
            self.kill()

    def draw(self, surface, camera_offset_x):
        screen_x = self.rect.x - camera_offset_x
        surface.blit(self.image, (screen_x, self.rect.y))