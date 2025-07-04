import pygame
import os
from . import const

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()

        # Carrega a imagem específica do projétil do jogador
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, '..', 'asset', 'playershot.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 15))  # Ajuste conforme necessário
        except:
            # Fallback visual
            self.image = pygame.Surface((30, 15), pygame.SRCALPHA)
            self.image.fill((255, 255, 0))  # Amarelo para projéteis do jogador

        self.rect = self.image.get_rect(center=position)
        self.speed = 800  # Velocidade alta para projéteis do jogador
        self.direction = direction  # 1 (direita) ou -1 (esquerda)
        self.damage = 25  # Dano suficiente para matar inimigos com um tiro
        self.owner = "player"

    def update(self, delta_time):
        self.rect.x += self.speed * self.direction * delta_time * 60

        # Remove se sair da tela
        if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH:
            self.kill()