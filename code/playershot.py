# code/playershot.py
import pygame
import os
from . import const

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.animation_frames = []
        self._load_animation_frames()

        if self.animation_frames:
            self.image = self.animation_frames[0]
        else:
            self.image = pygame.Surface((30, 15), pygame.SRCALPHA)
            self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect(center=position)
        self.speed = 500  # Aumentei a velocidade para o tiro ser mais eficaz
        self.direction = direction
        self.damage = 25
        self.owner = "player"

        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.05

    def _load_animation_frames(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')
        for i in range(1, 6):
            frame_file = os.path.join(asset_path, f'playershot{i}.png')
            try:
                temp_image = pygame.image.load(frame_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (30, 15))
                self.animation_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame '{frame_file}' do PlayerShot: {e}")

    def update(self, delta_time, camera_offset_x, screen_width):
        """
        Atualiza a posição do tiro e verifica se ele saiu da ÁREA VISÍVEL da câmera.
        """
        self.rect.x += self.speed * self.direction * delta_time

        if self.animation_frames:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame_index]

        # --- ESTA É A CORREÇÃO PRINCIPAL ---
        # Verifica se o tiro saiu da visão da câmera, não da tela fixa.
        if self.rect.right < camera_offset_x or self.rect.left > camera_offset_x + screen_width:
            self.kill()

    def draw(self, surface, camera_offset_x):
        screen_x = self.rect.x - camera_offset_x
        surface.blit(self.image, (screen_x, self.rect.y))