import os

import pygame


class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, position, enemy_type):
        super().__init__()

        # Seu código para carregar a imagem
        self.shots_group = None
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, '..', 'asset', f'{enemy_type}shot.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            # ajuste do tamanho se quiser
            # self.image = pygame.transform.scale(self.image, tamanho_adequado)
        except:
            self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
            self.image.fill((255, 100, 100))  # Exemplo de fallback

        # **Aqui que cria o rect!**
        self.rect = self.image.get_rect(center=position)

        # Outras variáveis
        self.speed = 300  # Exemplo, pode variar por enemy_type
        self.enemy_type = enemy_type

    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time * 60
        if self.rect.right < 0:
            self.kill()

    def draw(self, surface, camera_offset_x):
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))

