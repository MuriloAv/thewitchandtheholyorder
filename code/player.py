# code/player.py

import pygame
import os
from . import const


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.name = "Player"

        self.screen = pygame.display.get_surface()
        self.speed = const.PLAYER_SPEED

        # --- Gerenciamento de Assets de Animação ---
        self.idle_image = None
        self.walk_frames = []
        self.jump_frames = []  # NOVO: Lista para os frames de pulo
        self._load_animation_frames()  # Carrega todos os frames

        # Define a imagem inicial e o retângulo do jogador
        # A imagem inicial é playerwalk0.png (idle)
        if self.idle_image:
            self.image = self.idle_image
        elif self.walk_frames:
            self.image = self.walk_frames[0]
        else:
            self.image = pygame.Surface((const.PLAYER_WIDTH, const.PLAYER_HEIGHT), pygame.SRCALPHA)
            self.image.fill(const.RED_COLOR)
            print("AVISO: Nenhuma imagem de player carregada. Usando fallback de cor sólida.")

        # O rect define a posição e tamanho do jogador
        self.rect = self.image.get_rect(topleft=position)

        # --- Variáveis de Animação de Caminhada (nomes ajustados para clareza) ---
        self.current_walk_frame_index = 0  # Renomeado de current_frame_index
        self.walk_animation_timer = 0.0  # Renomeado de animation_timer
        self.walk_animation_speed = 0.1  # Renomeado de animation_speed

        self.is_moving = False

        # --- NOVO: Variáveis de Pulo e Física ---
        self.is_jumping = False  # Booleano para indicar se o personagem está pulando
        self.on_ground = True  # Booleano para indicar se o personagem está no chão
        self.y_velocity = 0  # Velocidade vertical do personagem

        # Variáveis de Animação de Pulo
        self.current_jump_frame_index = 0
        self.jump_animation_timer = 0.0

    def _load_animation_frames(self):
        """Carrega todas as imagens de animação do jogador (idle, walk, jump)."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        # Carrega a imagem idle (parado)
        idle_file = os.path.join(asset_path, 'playerwalk0.png')
        try:
            temp_image = pygame.image.load(idle_file).convert_alpha()
            self.idle_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar imagem IDLE do jogador '{idle_file}': {e}")
            self.idle_image = None

        # Carrega os frames de caminhada (1 a 7)
        for i in range(1, 8):
            walk_file = os.path.join(asset_path, f'playerwalk{i}.png')
            try:
                temp_image = pygame.image.load(walk_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
                self.walk_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame de caminhada '{walk_file}': {e}")

        if not self.walk_frames:
            print("AVISO: Nenhum frame de caminhada carregado. Animação de movimento não funcionará.")

        # NOVO: Carrega os frames de pulo (1 a 6)
        for i in range(1, 7):  # pulo1.png até pulo6.png
            jump_file = os.path.join(asset_path, f'pulo{i}.png')
            try:
                temp_image = pygame.image.load(jump_file).convert_alpha()
                # É importante escalar os frames de pulo para o mesmo tamanho do jogador
                scaled_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
                self.jump_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame de pulo '{jump_file}': {e}")

        if not self.jump_frames:
            print("AVISO: Nenhum frame de pulo carregado. Animação de pulo não funcionará.")

    # NOVO: Método para lidar com eventos discretos (como pressionar uma tecla)
    def handle_event(self, event):
        """Processa eventos específicos como o pulo."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.on_ground:
                self.is_jumping = True
                self.on_ground = False
                self.y_velocity = -const.JUMP_STRENGTH  # Y negativo é para cima em Pygame
                self.current_jump_frame_index = 0  # Reinicia a animação de pulo
                self.jump_animation_timer = 0.0

    def update(self, delta_time):
        """
        Atualiza o estado do jogador, incluindo movimento horizontal, física de pulo e animação.
        delta_time: Tempo em segundos desde o último frame.
        """
        # --- Movimento Horizontal (contínuo, usando teclas pressionadas) ---
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        # Só atualiza a posição horizontal se não estiver pulando ou no ar para simplificar o controle
        # Para jogos mais complexos, o movimento horizontal pode ser mantido durante o pulo
        if self.on_ground:
            self.rect.x += dx
        else:  # Se estiver no ar, o movimento horizontal pode ser um pouco mais lento
            self.rect.x += dx * 0.7  # Exemplo: 70% da velocidade horizontal no ar

        self.is_moving = (dx != 0)

        # --- NOVO: Aplicação da Gravidade e Movimento Vertical ---
        if not self.on_ground:  # Aplica gravidade se não estiver no chão
            self.y_velocity += const.GRAVITY * delta_time

        self.rect.y += self.y_velocity * delta_time

        # --- NOVO: Detecção de Colisão com o Chão ---
        # Se o jogador descer abaixo da linha do chão (const.PLAYER_GROUND_Y)
        if self.rect.y >= const.PLAYER_GROUND_Y:
            self.rect.y = const.PLAYER_GROUND_Y  # Fixa a posição no chão
            if not self.on_ground:  # Se acabou de aterrissar (transição de "no ar" para "no chão")
                self.on_ground = True
                self.is_jumping = False
                self.y_velocity = 0  # Zera a velocidade vertical
                # Após aterrissar, reseta animação de pulo e retorna para idle/walk
                self.current_jump_frame_index = 0
                self.jump_animation_timer = 0.0

        # --- Lógica de Seleção de Animação (Walk/Idle/Jump) ---
        if self.is_jumping or not self.on_ground:  # Se estiver pulando ou no ar
            if self.jump_frames:
                self.jump_animation_timer += delta_time
                if self.jump_animation_timer >= const.JUMP_ANIMATION_SPEED:
                    self.jump_animation_timer -= const.JUMP_ANIMATION_SPEED
                    # Cicla pelos frames de pulo
                    self.current_jump_frame_index = (self.current_jump_frame_index + 1) % len(self.jump_frames)
                self.image = self.jump_frames[self.current_jump_frame_index]
            else:
                # Fallback se não houver frames de pulo (usa idle_image se existir)
                if self.idle_image:
                    self.image = self.idle_image
        elif self.is_moving:  # Se estiver no chão e movendo (caminhando)
            if self.walk_frames:
                self.walk_animation_timer += delta_time
                if self.walk_animation_timer >= self.walk_animation_speed:
                    self.walk_animation_timer -= self.walk_animation_speed
                    self.current_walk_frame_index = (self.current_walk_frame_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_walk_frame_index]
            else:
                if self.idle_image:  # Fallback se não houver frames de caminhada
                    self.image = self.idle_image
        else:  # Se estiver no chão e parado (idle)
            if self.idle_image:
                self.image = self.idle_image
            # Reseta o índice e timer da animação de caminhada/pulo ao parar/aterrissar
            self.current_walk_frame_index = 0
            self.walk_animation_timer = 0.0
            self.current_jump_frame_index = 0
            self.jump_animation_timer = 0.0

    def draw(self, surface, camera_offset_x):
        """
        Desenha o jogador na tela, ajustando pela posição da câmera.
        surface: A superfície do Pygame onde o jogador será desenhado.
        camera_offset_x: O deslocamento horizontal da câmera.
        """
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))

    def get_rect(self):
        """Retorna o retângulo de colisão e posição atual do jogador."""
        return self.rect