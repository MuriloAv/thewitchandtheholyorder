# code/level.py
import pygame
import os
from . import const  # Importa as constantes


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.level_width = const.LEVEL_WIDTH
        self.level_height = const.LEVEL_HEIGHT  # <-- CORRIGIDO AQUI! AGORA É const.LEVEL_HEIGHT (tudo maiúsculo)

        # Player setup (agora com asset de imagem)
        self.player_speed = const.PLAYER_SPEED
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Agora o asset do jogador está diretamente na pasta 'asset'
        player_asset_path = os.path.join(base_dir, '..', 'asset',
                                         const.PLAYER_SPRITE_FILENAME)  # <-- LINHA ALTERADA

        self.player_image = None  # Inicializa self.player_image como None por padrão
        try:
            # Tenta carregar e redimensionar a imagem
            temp_image = pygame.image.load(player_asset_path).convert_alpha()
            self.player_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar o asset do jogador '{player_asset_path}': {e}")
            # Se der erro, self.player_image permanece None, o que é o comportamento desejado para o fallback

        # Esta parte AGORA está fora do bloco try-except e será SEMPRE executada
        # Inicializa o player_rect com base na imagem (se carregada) ou com as dimensões de fallback
        if self.player_image:
            self.player_rect = self.player_image.get_rect()
        else:
            # Fallback para retângulo vermelho, mantendo dimensões de const.py
            self.player_rect = pygame.Rect(0, 0, const.PLAYER_WIDTH, const.PLAYER_HEIGHT)
            print("Usando retângulo de fallback para o jogador.")

        self.player_rect.x = self.screen_width // 4  # Posição inicial X
        self.player_rect.y = self.screen_height - self.player_rect.height - 10  # Posição inicial Y (próximo à base)

        # Camera setup (offset para simular scrolling)
        self.camera_offset_x = 0

        # --- CONFIGURAÇÃO DO BACKGROUND PARALLAX ---
        self.parallax_layers = []

        # Fatores de rolagem para cada camada.
        scroll_factors = [0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]

        # Carrega todas as camadas de bg1 a bg7

        for i in range(1, 7):
            layer_filename = f'lvl1bg{i}.png'
            # Agora os assets de background estão diretamente na pasta 'asset'
            layer_path = os.path.join(base_dir, '..', 'asset', layer_filename)  # <-- LINHA ALTERADA

            try:
                layer_image = pygame.image.load(layer_path).convert_alpha()
                layer_image = pygame.transform.scale(layer_image, (self.screen_width, self.screen_height))

                self.parallax_layers.append({
                    'image': layer_image,
                    'scroll_factor': scroll_factors[i - 1]
                })
            except pygame.error as e:
                print(f"Erro ao carregar a camada de parallax '{layer_filename}': {e}")
                self.parallax_layers.clear()
                break

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
        if target_camera_x < 0:
            target_camera_x = 0
        if target_camera_x > self.level_width - self.screen_width:
            target_camera_x = self.level_width - self.screen_width

        self.camera_offset_x = target_camera_x

    def _draw_elements(self):
        """
        Desenha os elementos do nível na tela, incluindo o fundo parallax e o jogador.
        """
        self.screen.fill(const.BLACK_COLOR)

        # Desenha as camadas de parallax
        if self.parallax_layers:
            for layer in self.parallax_layers:
                scrolled_x = (self.camera_offset_x * layer['scroll_factor']) % layer['image'].get_width()
                self.screen.blit(layer['image'], (-scrolled_x, 0))
                self.screen.blit(layer['image'], (layer['image'].get_width() - scrolled_x, 0))
        else:
            self.screen.fill(self.fallback_bg_color)

        # Desenha o jogador (sempre na frente do fundo)
        player_screen_x = self.player_rect.x - self.camera_offset_x

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
                # Esta é a forma correta de detectar a tecla ESC
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"

            self._handle_input()
            self._update_camera()
            self._draw_elements()

            clock.tick(const.FPS)