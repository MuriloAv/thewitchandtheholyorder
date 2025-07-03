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
        player_start_position = (const.PLAYER_START_X, const.PLAYER_START_Y)
        self.player = Player(player_start_position)  # Instancia o jogador

        # Camera setup (offset para simular scrolling)
        self.camera_offset_x = 0

        # --- CONFIGURAÇÃO DO BACKGROUND PARALLAX ---
        self.parallax_layers = []
        # scroll_factors pode precisar de ajuste dependendo do seu jogo
        # Garante que temos fatores suficientes para todas as camadas que podem ser carregadas
        scroll_factors_base = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]
        # Se bg_count for maior que o número de fatores base, crie fatores adicionais
        if bg_count > len(scroll_factors_base):
            scroll_factors = [(i + 1) * (1.0 / bg_count) for i in range(bg_count)]  # Gerar fatores uniformes
        else:
            scroll_factors = scroll_factors_base[:bg_count]  # Usar apenas os necessários

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Para carregar backgrounds
        for i in range(bg_start_index, bg_start_index + bg_count):
            layer_filename = f'{bg_prefix}{i}.png'
            layer_path = os.path.join(base_dir, '..', 'asset', layer_filename)

            loaded_image = None  # Inicializa para None
            scaled_layer_image = None  # Inicializa para None

            try:
                # 1. Carrega a imagem original
                loaded_image = pygame.image.load(layer_path).convert_alpha()

                # VERIFICAÇÃO 1: Se a imagem carregada é None, pula esta camada
                if loaded_image is None:
                    print(f"AVISO: Imagem carregada é None para '{layer_filename}'. Pulando esta camada.")
                    continue  # Não adiciona esta camada à lista

                original_width, original_height = loaded_image.get_size()
                scale_factor_h = self.screen_height / original_height
                scaled_width = int(original_width * scale_factor_h)
                scaled_height = self.screen_height

                # 2. Escala a imagem
                scaled_layer_image = pygame.transform.scale(loaded_image, (scaled_width, scaled_height))

                # VERIFICAÇÃO 2: Se a imagem escalada é None, pula esta camada
                if scaled_layer_image is None:
                    print(f"AVISO: Imagem escalada é None para '{layer_filename}'. Pulando esta camada.")
                    continue  # Não adiciona esta camada à lista

                # Garante que o índice para scroll_factor é válido
                current_scroll_factor = scroll_factors[i - bg_start_index] if (i - bg_start_index) < len(
                    scroll_factors) else 1.0

                self.parallax_layers.append({
                    'image': scaled_layer_image,
                    'scroll_factor': current_scroll_factor
                })
            except pygame.error as e:
                print(f"ERRO CRÍTICO: Falha ao carregar ou processar camada de parallax '{layer_filename}': {e}")
                # Em caso de erro crítico, limpamos todas as camadas para usar um fundo sólido.
                self.parallax_layers.clear()
                break  # Sai do loop, pois o carregamento está comprometido.
            except Exception as e:  # Captura qualquer outra exceção inesperada
                print(f"ERRO INESPERADO: Falha geral ao processar camada de parallax '{layer_filename}': {e}")
                self.parallax_layers.clear()
                break  # Sai do loop

        if not self.parallax_layers:
            print("Nenhuma camada de parallax carregada. Usando cor de fundo sólida.")
            self.fallback_bg_color = const.BLUE_SKY_COLOR
        # Caso contrário, se algumas camadas foram carregadas, não defina um fallback_bg_color
        # porque as camadas carregadas serão usadas.

    def _handle_input(self):
        # Este método não será mais usado diretamente para o player.
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

    def _draw_elements(self):
        """
        Desenha os elementos do nível na tela, incluindo o fundo parallax e o jogador.
        """
        self.screen.fill(const.BLACK_COLOR)

        if self.parallax_layers:
            for layer in self.parallax_layers:
                layer_image = layer['image']

                # VERIFICAÇÃO DEFENSIVA: Garante que a imagem não é None antes de tentar usá-la
                if layer_image is None:
                    print(
                        f"AVISO: Imagem de camada nula encontrada na lista de parallax. Pulando desenho desta camada.")
                    continue  # Pula para a próxima camada do loop

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

                # Passa o evento para o método handle_event do player
                self.player.handle_event(event)  # <--- ESSA É A LINHA CHAVE PARA O PULO!

            # Atualiza o jogador, passando delta_time (inclui física e animação de caminhada/pulo)
            self.player.update(delta_time)

            self._update_camera()  # A câmera agora usa self.player.rect
            self._draw_elements()

            # --- Condição de Nível Completo ---
            if self.player.rect.x >= self.level_width - self.player.rect.width:
                print(f"Nível completo! Player atingiu o fim do nível ({self.level_width}).")
                return "level_complete"

        return "continue"