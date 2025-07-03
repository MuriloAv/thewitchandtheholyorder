# code/level.py

import pygame
import os
from . import const


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.level_width = const.LEVEL_WIDTH
        self.level_height = const.LEVEL_HEIGHT

        # Player setup (mantido como está, apenas aprimorando o uso de constantes)
        self.player_speed = const.PLAYER_SPEED
        base_dir = os.path.dirname(os.path.abspath(__file__))
        player_asset_path = os.path.join(base_dir, '..', 'asset', const.PLAYER_SPRITE_FILENAME)

        self.player_image = None
        try:
            temp_image = pygame.image.load(player_asset_path).convert_alpha()
            self.player_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar o asset do jogador '{player_asset_path}': {e}")

        if self.player_image:
            # Garante que PLAYER_START_X e PLAYER_START_Y estão definidos em const.py.
            # Se não, define valores padrão para evitar erros.
            player_start_x = getattr(const, 'PLAYER_START_X', self.screen_width // 4)
            player_start_y = getattr(const, 'PLAYER_START_Y', self.screen_height - self.player_image.get_height() - 10)
            self.player_rect = self.player_image.get_rect(topleft=(player_start_x, player_start_y))
        else:
            self.player_rect = pygame.Rect(0, 0, const.PLAYER_WIDTH, const.PLAYER_HEIGHT)
            print("Usando retângulo de fallback para o jogador.")
            self.player_rect.x = self.screen_width // 4
            self.player_rect.y = self.screen_height - self.player_rect.height - 10

        # Camera setup (offset para simular scrolling)
        self.camera_offset_x = 0

        # --- CONFIGURAÇÃO DO BACKGROUND PARALLAX ---
        self.parallax_layers = []

        # Fatores de rolagem para cada camada. Ajuste esses valores para obter o efeito desejado.
        # Valores menores para camadas mais distantes (0.1 é muito lento), maiores para camadas mais próximas.
        # Experimente para encontrar o "feel" certo.
        scroll_factors = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]  # Ligeiramente ajustado para mais movimento

        # Carrega e prepara todas as camadas de bg1 a bg6
        for i in range(1, 7):  # Loop de 1 a 6, pois o lvl1bg vai até o 6.
            layer_filename = f'lvl1bg{i}.png'
            layer_path = os.path.join(base_dir, '..', 'asset', layer_filename)

            try:
                # 1. Carrega a imagem original da camada
                layer_image_original = pygame.image.load(layer_path).convert_alpha()

                # 2. Escala a imagem para preencher a altura da tela, mantendo a proporção.
                #    Esta será a imagem "tile" que repetiremos.
                original_width, original_height = layer_image_original.get_size()

                # Fator de escala baseado na altura da tela
                scale_factor_h = self.screen_height / original_height

                # Calcula a nova largura para manter a proporção
                scaled_width = int(original_width * scale_factor_h)
                scaled_height = self.screen_height

                scaled_layer_image = pygame.transform.scale(layer_image_original, (scaled_width, scaled_height))

                # Adiciona a imagem *única* escalada (que será o tile) à lista de camadas
                self.parallax_layers.append({
                    'image': scaled_layer_image,  # Armazena a imagem única escalada para ser o tile
                    'scroll_factor': scroll_factors[i - 1]
                })
            except pygame.error as e:
                print(f"Erro ao carregar ou preparar a camada de parallax '{layer_filename}': {e}")
                self.parallax_layers.clear()  # Limpa as camadas se houver um erro crítico
                break  # Sai do loop de carregamento

        if not self.parallax_layers:
            print("Nenhuma camada de parallax carregada. Usando cor de fundo sólida.")
            self.fallback_bg_color = const.BLUE_SKY_COLOR

    def _handle_input(self):
        """Processa a entrada do teclado para movimento do jogador."""
        keys = pygame.key.get_pressed()

        # O jogador se move no mundo, não apenas na tela
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed

        # Limita o movimento do jogador dentro das bordas do nível
        if self.player_rect.left < 0:
            self.player_rect.left = 0
        if self.player_rect.right > self.level_width:
            self.player_rect.right = self.level_width

    def _update_camera(self):
        """Atualiza o offset da câmera para seguir o jogador."""
        # Tenta manter o jogador centralizado na tela
        target_camera_x = self.player_rect.centerx - (self.screen_width // 2)

        # Limita o offset da câmera para não mostrar áreas fora do nível
        # (Isso só importa se o nível tem um tamanho fixo, como const.LEVEL_WIDTH)
        if target_camera_x < 0:
            target_camera_x = 0
        if target_camera_x > self.level_width - self.screen_width:
            target_camera_x = self.level_width - self.screen_width

        self.camera_offset_x = target_camera_x

    def _draw_elements(self):
        """
        Desenha os elementos do nível na tela, incluindo o fundo parallax e o jogador.
        """
        self.screen.fill(const.BLACK_COLOR)  # Sempre preencha o fundo primeiro

        if self.parallax_layers:
            for layer in self.parallax_layers:
                layer_image = layer['image']  # A imagem do tile (única, escalada)
                layer_image_width = layer_image.get_width()  # Largura do tile

                # Calcula o deslocamento total da camada, garantindo que seja um inteiro
                # Este é o valor bruto de quanto a imagem se moveu.
                total_offset = int(self.camera_offset_x * layer['scroll_factor'])

                # Calcula a parte do offset que corresponde ao loop da imagem.
                # Isto é a posição "real" do pixel 0 da imagem em relação ao início do seu loop.
                # Ex: se total_offset é 250 e image_width é 200, wrapped_offset é 50.
                # Isso significa que o pixel 50 da imagem é que deveria estar na posição 0 da tela.
                wrapped_offset = total_offset % layer_image_width

                # Calcula a posição inicial na tela para a primeira blit.
                # A imagem é desenhada começando de uma posição negativa, para que a parte visível
                # na tela esteja alinhada com o wrapped_offset.
                draw_start_x = -wrapped_offset

                # Loop para desenhar tiles da imagem até cobrir toda a largura da tela.
                # Isso garante que não importa o tamanho da imagem ou da tela, sempre haverá cobertura.
                while draw_start_x < self.screen_width:
                    self.screen.blit(layer_image, (draw_start_x, 0))
                    draw_start_x += layer_image_width  # Move para a próxima posição para blitar o próximo tile
        else:
            self.screen.fill(self.fallback_bg_color)

        # Desenha o jogador (sempre na frente do fundo)
        # Garanta que a posição X do jogador também seja um inteiro para evitar "tremores"
        player_screen_x = int(self.player_rect.x - self.camera_offset_x)

        if self.player_image:
            self.screen.blit(self.player_image, (player_screen_x, self.player_rect.y))
        else:
            pygame.draw.rect(self.screen, const.RED_COLOR,
                             (player_screen_x, self.player_rect.y, self.player_rect.width, self.player_rect.height))

        pygame.display.flip()

    def run(self, clock):
        """Loop principal de gameplay para o nível."""
        level_running = True
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"

            self._handle_input()
            self._update_camera()
            self._draw_elements()

            clock.tick(const.FPS)