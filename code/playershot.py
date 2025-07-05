# playershot.py
import pygame
import os
from . import const

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.animation_frames = []
        self._load_animation_frames() # Novo método para carregar frames

        # Imagem inicial do tiro
        if self.animation_frames:
            self.image = self.animation_frames[0]
        else:
            print("AVISO: Nenhuma imagem de PlayerShot carregada. Usando fallback.")
            self.image = pygame.Surface((30, 15), pygame.SRCALPHA)
            self.image.fill((255, 255, 0))  # amarelo como fallback

        self.rect = self.image.get_rect(center=position)
        self.speed = 400 # Velocidade do tiro (ajustada para um valor mais rápido, como nos códigos anteriores)
        self.direction = direction
        self.damage = 25
        self.owner = "player"

        # Controle de animação
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.05 # Velocidade da animação (tempo em segundos por frame)

    def _load_animation_frames(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        # Carrega playershot1.png até playershot5.png
        for i in range(1, 6): # Loop de 1 a 5 (exclusive 6)
            frame_file = os.path.join(asset_path, f'playershot{i}.png')
            try:
                temp_image = pygame.image.load(frame_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (30, 15)) # Ajuste o tamanho conforme necessário
                self.animation_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame '{frame_file}' do PlayerShot: {e}")
                # Não adicione frames se houver erro, para evitar IndexError
            except Exception as e:
                print(f"Erro inesperado ao carregar frame '{frame_file}' do PlayerShot: {e}")


    def update(self, delta_time):
        # Atualiza a posição do tiro
        self.rect.x += self.speed * self.direction * delta_time

        # Atualiza a animação do tiro
        if self.animation_frames: # Garante que há frames para animar
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame_index]

        # Remove o tiro se sair da tela
        if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH:
            self.kill()

    def draw(self, surface, camera_offset_x):
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))