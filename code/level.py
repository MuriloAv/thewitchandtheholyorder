# code/level.py

import pygame
import os
from . import const
from .player import Player  # <--- Importa a classe Player


class Level:
    def __init__(self, screen, bg_prefix, bg_count, bg_start_index, level_actual_width):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.level_width = level_actual_width
        self.level_height = const.SCREEN_HEIGHT

        # --- Player Setup (usando a nova classe Player) ---
        # A posição inicial do player agora é responsabilidade do Player
        player_start_position = (const.PLAYER_START_X, const.PLAYER_START_Y)
        self.player = Player(player_start_position)  # Instancia o jogador
        # player_rect agora é self.player.rect

        # Camera setup (offset para simular scrolling)
        self.camera_offset_x = 0

        # --- CONFIGURAÇÃO DO BACKGROUND PARALLAX (sem alterações) ---
        self.parallax_layers = []
        scroll_factors = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Para carregar backgrounds
        for i in range(bg_start_index, bg_start_index + bg_count):
            layer_filename = f'{bg_prefix}{i}.png'
            layer_path = os.path.join(base_dir, '..', 'asset', layer_filename)
            try:
                layer_image_original = pygame.image.load(layer_path).convert_alpha()
                original_width, original_height = layer_image_original.get_size()
                scale_factor_h = self.screen_height / original_height
                scaled_width = int(original_width * scale_factor_h)
                scaled_height = self.screen_height
                scaled_layer_image = pygame.transform.scale(layer_image_original, (scaled_width, scaled_height))
                self.parallax_layers.append({
                    'image': scaled_layer_image,
                    'scroll_factor': scroll_factors[i - bg_start_index]
                })
            except pygame.error as e:
                print(f"Erro ao carregar ou preparar a camada de parallax '{layer_filename}': {e}")
                self.parallax_layers.clear()
                break

        if not self.parallax_layers:
            print("Nenhuma camada de parallax carregada. Usando cor de fundo sólida.")
            self.fallback_bg_color = const.BLUE_SKY_COLOR

    def _handle_input(self):
        """
        Processa a entrada do teclado.
        Agora, a lógica de input do jogador é gerenciada pelo objeto player.
        """
        # O self.player.handle_input() já é chamado dentro de self.player.update()
        # Portanto, não precisamos chamá-lo explicitamente aqui.
        pass

    def _update_camera(self):
        """Atualiza o offset da câmera para seguir o jogador."""
        # A câmera segue o self.player.rect
        target_camera_x = self.player.rect.centerx - (self.screen_width // 2)

        if target_camera_x < 0:
            target_camera_x = 0
        if target_camera_x > self.level_width - self.screen_width:
            target_camera_x = self.level_width - self.screen_width

        self.camera_offset_x = target_camera_x

        # Limita o movimento do jogador para não sair do nível
        # (Isso é feito aqui para interagir com a largura do nível)
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.level_width:
            self.player.rect.right = self.level_width

    def _draw_elements(self):
        """
        Desenha os elementos do nível na tela, incluindo o fundo parallax e o jogador.
        """
        self.screen.fill(const.BLACK_COLOR)

        if self.parallax_layers:
            for layer in self.parallax_layers:
                layer_image = layer['image']
                layer_image_width = layer_image.get_width()

                total_offset = int(self.camera_offset_x * layer['scroll_factor'])
                wrapped_offset = total_offset % layer_image_width

                draw_start_x = -wrapped_offset

                while draw_start_x < self.screen_width:
                    self.screen.blit(layer_image, (draw_start_x, 0))
                    draw_start_x += layer_image_width
        else:
            self.screen.fill(self.fallback_bg_color)

        # --- Desenha o jogador (usando o método draw da classe Player) ---
        self.player.draw(self.screen, self.camera_offset_x)

        pygame.display.flip()

    def run(self, clock):
        """Loop principal de gameplay para o nível."""
        level_running = True
        while level_running:
            delta_time = clock.tick(const.FPS) / 1000.0  # Calcula delta_time em segundos

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"

            # Atualiza o jogador, passando delta_time
            self.player.update(delta_time)

            self._update_camera()  # A câmera agora usa self.player.rect
            self._draw_elements()

            # --- Condição de Nível Completo ---
            # Usa self.player.rect.x para verificar o fim do nível
            if self.player.rect.x >= self.level_width - self.player.rect.width:
                print(f"Nível completo! Player atingiu o fim do nível ({self.level_width}).")
                # Resetar a posição do jogador para o início do próximo nível pode ser feito em game.py
                # Ou aqui, se o Level for sempre um novo objeto.
                return "level_complete"

        return "continue"