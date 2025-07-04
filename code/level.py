# code/level.py

import pygame
import os
import random
from . import const
from .player import Player
from .enemy import Enemy1, Enemy2, Enemy3


class Level:
    def __init__(self, screen, bg_prefix, bg_count, bg_start_index, level_actual_width):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.level_width = level_actual_width
        self.level_height = const.SCREEN_HEIGHT
        self.level_number = int(bg_prefix[3])

        # --- Player Setup ---
        player_start_position = (const.PLAYER_START_X, const.PLAYER_START_Y)
        self.player = Player(player_start_position)

        # --- Inimigos Setup ---
        self.enemies = pygame.sprite.Group()
        self.enemy_spawn_timer = 0.0
        self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN, const.ENEMY_SPAWN_INTERVAL_MAX)

        # Camera setup
        self.camera_offset_x = 0

        # --- CONFIGURAÇÃO DO BACKGROUND PARALLAX ---
        self.parallax_layers = []
        scroll_factors_base = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]
        if bg_count > len(scroll_factors_base):
            scroll_factors = [(i + 1) * (1.0 / bg_count) for i in range(bg_count)]
        else:
            scroll_factors = scroll_factors_base[:bg_count]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        for i in range(bg_start_index, bg_start_index + bg_count):
            layer_filename = f'{bg_prefix}{i}.png'
            layer_path = os.path.join(base_dir, '..', 'asset', layer_filename)

            loaded_image = None
            scaled_layer_image = None

            try:
                loaded_image = pygame.image.load(layer_path).convert_alpha()
                if loaded_image is None:
                    print(f"AVISO: Imagem carregada é None para '{layer_filename}'. Pulando esta camada.")
                    continue

                original_width, original_height = loaded_image.get_size()
                scale_factor_h = self.screen_height / original_height
                scaled_width = int(original_width * scale_factor_h)
                scaled_height = self.screen_height

                scaled_layer_image = pygame.transform.scale(loaded_image, (scaled_width, scaled_height))
                if scaled_layer_image is None:
                    print(f"AVISO: Imagem escalada é None para '{layer_filename}'. Pulando esta camada.")
                    continue

                current_scroll_factor = scroll_factors[i - bg_start_index] if (i - bg_start_index) < len(
                    scroll_factors) else 1.0

                self.parallax_layers.append({
                    'image': scaled_layer_image,
                    'scroll_factor': current_scroll_factor
                })
            except pygame.error as e:
                print(f"ERRO CRÍTICO: Falha ao carregar ou processar camada de parallax '{layer_filename}': {e}")
                self.parallax_layers.clear()
                break
            except Exception as e:
                print(f"ERRO INESPERADO: Falha geral ao processar camada de parallax '{layer_filename}': {e}")
                self.parallax_layers.clear()
                break

        if not self.parallax_layers:
            print("Nenhuma camada de parallax carregada. Usando cor de fundo sólida.")
            self.fallback_bg_color = const.BLUE_SKY_COLOR

    def _handle_input(self):
        pass

    def _update_camera(self):
        """Atualiza o offset da câmera para seguir o jogador."""
        target_camera_x = self.player.rect.centerx - (self.screen_width // 2)

        if target_camera_x < 0:
            target_camera_x = 0
        if target_camera_x > self.level_width - self.screen_width:
            target_camera_x = self.level_width - self.screen_width

        self.camera_offset_x = target_camera_x

        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.level_width:
            self.player.rect.right = self.level_width

    def _spawn_enemy(self):
        """Spawns um inimigo aleatório na tela, na altura do jogador."""
        enemy_types = [Enemy1, Enemy2, Enemy3]
        chosen_enemy_class = random.choice(enemy_types)

        spawn_x = self.camera_offset_x + self.screen_width + const.ENEMY_SPAWN_X_OFFSET

        # ALTERADO: Inimigos aparecem na mesma altura Y do jogador (const.PLAYER_START_Y)
        spawn_y = const.PLAYER_START_Y

        new_enemy = chosen_enemy_class((spawn_x, spawn_y))
        self.enemies.add(new_enemy)

        print(f"DEBUG: Spawned {chosen_enemy_class.__name__} at X={spawn_x}, Y={spawn_y} (PLAYER_START_Y)")

    def _draw_elements(self):
        """
        Desenha os elementos do nível na tela, incluindo o fundo parallax, o jogador e os inimigos.
        """
        self.screen.fill(const.BLACK_COLOR)

        if self.parallax_layers:
            for layer in self.parallax_layers:
                layer_image = layer['image']

                if layer_image is None:
                    continue

                layer_image_width = layer_image.get_width()

                total_offset = int(self.camera_offset_x * layer['scroll_factor'])
                wrapped_offset = total_offset % layer_image_width

                draw_start_x = -wrapped_offset

                while draw_start_x < self.screen_width:
                    self.screen.blit(layer_image, (draw_start_x, 0))
                    draw_start_x += layer_image_width
        else:
            self.screen.fill(self.fallback_bg_color)

        # --- Desenha o jogador ---
        self.player.draw(self.screen, self.camera_offset_x)

        # --- Desenha os inimigos ---
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset_x)

        pygame.display.flip()

    def run(self, clock):
        """Loop principal de gameplay para o nível."""
        level_running = True
        while level_running:
            delta_time = clock.tick(const.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"

                self.player.handle_event(event)

            # --- Lógica de Spawn de Inimigos ---
            self.enemy_spawn_timer += delta_time
            if self.enemy_spawn_timer >= self.next_spawn_time:
                self._spawn_enemy()
                self.enemy_spawn_timer = 0.0
                self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN, const.ENEMY_SPAWN_INTERVAL_MAX)

            self.player.update(delta_time)
            self.enemies.update(delta_time)

            self._update_camera()
            self._draw_elements()

            # --- Condição de Nível Completo ---
            if self.player.rect.x >= self.level_width - self.player.rect.width:
                print(f"Nível completo! Player atingiu o fim do nível ({self.level_width}).")
                self.enemies.empty()
                return "level_complete"

        return "continue"