# code/player.py

import pygame
import os
from . import const


class Player(pygame.sprite.Sprite):  # Herdar de Sprite pode ser útil para grupos no futuro
    def __init__(self, position):
        super().__init__()

        self.screen = pygame.display.get_surface()  # Pega a surface da tela principal
        self.speed = const.PLAYER_SPEED

        # --- Gerenciamento de Assets de Animação ---
        self.idle_image = None
        self.walk_frames = []
        self._load_animation_frames()  # Carrega todos os frames

        # Define a imagem inicial e o retângulo do jogador
        # A imagem inicial é playerwalk0.png (idle)
        if self.idle_image:
            self.image = self.idle_image
        elif self.walk_frames:  # Fallback se não tiver idle, usa o primeiro frame de walk
            self.image = self.walk_frames[0]
        else:
            # Fallback para um retângulo sólido se não houver imagens
            self.image = pygame.Surface((const.PLAYER_WIDTH, const.PLAYER_HEIGHT), pygame.SRCALPHA)
            self.image.fill(const.RED_COLOR)  # Preenche com vermelho para debug
            print("AVISO: Nenhuma imagem de player carregada. Usando fallback de cor sólida.")

        # O rect define a posição e tamanho do jogador
        self.rect = self.image.get_rect(topleft=position)

        # --- Variáveis de Animação ---
        self.current_frame_index = 0
        self.animation_timer = 0.0  # Acumula o tempo para controlar a velocidade da animação
        self.animation_speed = 0.1  # Tempo em segundos para cada quadro (ex: 0.1 = 100ms por quadro)

        self.is_moving = False  # Estado para controlar se o player está se movendo

    def _load_animation_frames(self):
        """Carrega todas as imagens de animação do jogador."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        # Carrega a imagem idle (parado)
        idle_file = os.path.join(asset_path, 'playerwalk0.png')
        try:
            temp_image = pygame.image.load(idle_file).convert_alpha()
            self.idle_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar imagem IDLE do jogador '{idle_file}': {e}")
            self.idle_image = None  # Garante que idle_image seja None em caso de erro

        # Carrega os frames de caminhada (1 a 7)
        for i in range(1, 8):  # playerwalk1.png até playerwalk7.png
            walk_file = os.path.join(asset_path, f'playerwalk{i}.png')
            try:
                temp_image = pygame.image.load(walk_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
                self.walk_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame de caminhada '{walk_file}': {e}")

        if not self.walk_frames:
            print("AVISO: Nenhum frame de caminhada carregado. Animação de movimento não funcionará.")

    def handle_input(self):
        """Processa a entrada do teclado para movimento do jogador."""
        keys = pygame.key.get_pressed()

        dx = 0  # Deslocamento em X
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        # Atualiza a posição do jogador
        self.rect.x += dx

        # Define o estado de movimento
        self.is_moving = (dx != 0)  # True se houver deslocamento em X

    def update(self, delta_time):
        """
        Atualiza o estado do jogador, incluindo movimento e animação.
        delta_time: Tempo em segundos desde o último frame.
        """
        self.handle_input()  # Processa a entrada

        if self.is_moving:
            # Atualiza o timer da animação
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed  # Reseta o timer (mantendo o excesso)
                self.current_frame_index = (self.current_frame_index + 1) % len(self.walk_frames)
                # Atualiza a imagem para o próximo frame de caminhada
                self.image = self.walk_frames[self.current_frame_index]
        else:
            # Se não estiver movendo, exibe a imagem idle
            if self.idle_image:
                self.image = self.idle_image
            self.current_frame_index = 0  # Reseta o índice do frame
            self.animation_timer = 0.0  # Reseta o timer

    def draw(self, surface, camera_offset_x):
        """
        Desenha o jogador na tela, ajustando pela posição da câmera.
        surface: A superfície do Pygame onde o jogador será desenhado.
        camera_offset_x: O deslocamento horizontal da câmera.
        """
        # Calcula a posição do jogador na tela (em relação à câmera)
        screen_x = int(self.rect.x - camera_offset_x)

        # Desenha a imagem atual do jogador na tela
        surface.blit(self.image, (screen_x, self.rect.y))

    def get_rect(self):
        """Retorna o retângulo de colisão e posição atual do jogador."""
        return self.rect