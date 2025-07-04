import pygame
import os
from . import const


class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, position, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type  # 'enemy1', 'enemy2' ou 'enemy3'

        # Configurações específicas para cada tipo de inimigo
        configs = {
            'enemy1': {
                'image_file': 'enemy1shot.png',
                'size': (25, 25),
                'speed': 350,
                'damage': 15,
                'color': (255, 100, 100)  # Vermelho claro
            },
            'enemy2': {
                'image_file': 'enemy2shot.png',
                'size': (20, 30),
                'speed': 400,
                'damage': 10,
                'color': (100, 255, 100)  # Verde claro
            },
            'enemy3': {
                'image_file': 'enemy3shot.png',
                'size': (35, 20),
                'speed': 300,
                'damage': 20,
                'color': (100, 100, 255)  # Azul claro
            }
        }

        cfg = configs[enemy_type]

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, '..', 'asset', cfg['image_file'])
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, cfg['size'])
        except:
            self.image = pygame.Surface(cfg['size'], pygame.SRCALPHA)
            self.image.fill(cfg['color'])

        self.rect = self.image.get_rect(center=position)
        self.speed = cfg['speed']
        self.damage = cfg['damage']
        self.owner = enemy_type

    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time * 60  # Move para esquerda
        if self.rect.right < 0:
            self.kill()