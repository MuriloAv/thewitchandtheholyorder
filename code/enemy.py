# code/enemy.py

import pygame
import os
from . import const


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, speed, animation_speed, animation_prefix, num_frames):
        super().__init__()

        self.speed = speed  # Velocidade do inimigo (pixels/segundo)
        self.animation_speed = animation_speed  # Tempo por frame de animação

        self.walk_frames = []
        self._load_animation_frames(animation_prefix, num_frames)  # Carrega os frames específicos

        # Define a imagem inicial e o retângulo do inimigo
        if self.walk_frames:
            self.image = self.walk_frames[0]
        else:
            self.image = pygame.Surface((const.ENEMY_WIDTH, const.ENEMY_HEIGHT), pygame.SRCALPHA)
            self.image.fill(const.RED_COLOR)  # Fallback para um retângulo vermelho
            print(f"AVISO: Nenhuma imagem de inimigo carregada para {animation_prefix}. Usando fallback de cor sólida.")

        self.rect = self.image.get_rect(topleft=position)

        self.current_frame_index = 0
        self.animation_timer = 0.0

        self.health = 100  # Vida padrão, pode ser sobrescrita nas subclasses

    def _load_animation_frames(self, prefix, num_frames):
        """Carrega os frames de animação para um inimigo específico."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        for i in range(1, num_frames + 1):
            frame_file = os.path.join(asset_path, f'{prefix}{i}.png')
            try:
                temp_image = pygame.image.load(frame_file).convert_alpha()
                # Escala o inimigo para o tamanho definido nas constantes
                scaled_image = pygame.transform.scale(temp_image, (const.ENEMY_WIDTH, const.ENEMY_HEIGHT))
                self.walk_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame de inimigo '{frame_file}': {e}")

        if not self.walk_frames:
            print(f"AVISO: Nenhum frame carregado para {prefix}. Animação não funcionará.")

    def update(self, delta_time):
        """Atualiza o estado do inimigo (movimento e animação)."""

        # Movimento da direita para a esquerda
        self.rect.x -= self.speed * delta_time

        # Animação de caminhada
        if self.walk_frames:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                self.current_frame_index = (self.current_frame_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame_index]

        # Opcional: Remover inimigos que saem da tela
        if self.rect.right < 0:  # Se o inimigo saiu completamente da tela à esquerda
            self.kill()  # Remove o sprite de todos os grupos em que está

    def draw(self, surface, camera_offset_x):
        """
        Desenha o inimigo na tela, ajustando pela posição da câmera.
        surface: A superfície do Pygame onde o inimigo será desenhado.
        camera_offset_x: O deslocamento horizontal da câmera.
        """
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))


# --- Classes específicas para cada tipo de inimigo ---
class Enemy1(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY1_SPEED, const.ENEMY1_ANIMATION_SPEED, "enemy1walk", 6)
        self.health = const.ENEMY1_HEALTH


class Enemy2(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY2_SPEED, const.ENEMY2_ANIMATION_SPEED, "enemy2walk", 4)
        self.health = const.ENEMY2_HEALTH


class Enemy3(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY3_SPEED, const.ENEMY3_ANIMATION_SPEED, "enemy3walk", 5)
        self.health = const.ENEMY3_HEALTH