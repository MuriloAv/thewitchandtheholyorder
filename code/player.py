# code/player.py

import pygame
import os
from . import const
from .playershot import PlayerShot


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.name = "Player"
        self.speed = const.PLAYER_SPEED

        # Controle de tiro
        self.shoot_cooldown = 0.75
        self.time_since_last_shot = 0.0
        self.shots_group = pygame.sprite.Group()

        # Adicionado: Controle de Vida e Invencibilidade
        self.lives = const.PLAYER_LIVES_START
        self.invincible_timer = 0.0
        self.invincible_duration = const.PLAYER_INVINCIBILITY_DURATION # Define a duração aqui

        # Estados de movimento e física
        self.on_ground = True
        self.is_jumping = False
        self.y_velocity = 0

        # Carregamento das animações
        self.idle_image = None
        self.walk_frames = []
        self.jump_frames = []
        self._load_animation_frames()

        # Imagem inicial
        if self.idle_image:
            self.image = self.idle_image
        elif self.walk_frames:
            self.image = self.walk_frames[0]
        else:
            self.image = pygame.Surface((const.PLAYER_WIDTH, const.PLAYER_HEIGHT), pygame.SRCALPHA)
            self.image.fill(const.RED_COLOR)
            print("AVISO: Nenhuma imagem de player carregada. Usando fallback de cor sólida.")

        self.original_image = self.image # Salva a imagem original para piscar quando invencível
        self.rect = self.image.get_rect(topleft=position)

        # Animações
        self.current_walk_frame_index = 0
        self.walk_animation_timer = 0.0
        self.walk_animation_speed = 0.1

        self.is_moving = False

        # Animação de pulo
        self.current_jump_frame_index = 0
        self.jump_animation_timer = 0.0

    def _load_animation_frames(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        # Idle
        idle_file = os.path.join(asset_path, 'playerwalk0.png')
        try:
            temp_image = pygame.image.load(idle_file).convert_alpha()
            self.idle_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar imagem IDLE do jogador '{idle_file}': {e}")
            self.idle_image = None

        # Walk frames
        for i in range(1, 8):
            walk_file = os.path.join(asset_path, f'playerwalk{i}.png')
            try:
                temp_image = pygame.image.load(walk_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
                self.walk_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame de caminhada '{walk_file}': {e}")

        # Jump frames
        for i in range(1, 7):
            jump_file = os.path.join(asset_path, f'pulo{i}.png')
            try:
                temp_image = pygame.image.load(jump_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
                self.jump_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame de pulo '{jump_file}': {e}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.on_ground:
                self.is_jumping = True
                self.on_ground = False
                self.y_velocity = -const.JUMP_STRENGTH
                self.current_jump_frame_index = 0
                self.jump_animation_timer = 0.0
            elif event.key == pygame.K_SPACE:
                self.shoot()

    def shoot(self):
        if self.time_since_last_shot >= self.shoot_cooldown:
            shot_pos = self.rect.midright
            new_shot = PlayerShot(shot_pos, direction=1)
            self.shots_group.add(new_shot)
            self.time_since_last_shot = 0.0

    # NOVO MÉTODO: Player recebe dano
    def take_damage(self, amount):
        if self.invincible_timer <= 0: # Só recebe dano se não estiver invencível
            self.lives -= amount
            self.invincible_timer = self.invincible_duration # Ativa o timer de invencibilidade
            print(f"Player levou dano! Vidas restantes: {self.lives}")
            if self.lives <= 0:
                print("Player KO!")
                # Aqui você chamaria a lógica de Game Over

    def update(self, delta_time):
        self.time_since_last_shot += delta_time

        # Atualiza timer de invencibilidade
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time
            # Adiciona efeito de piscar enquanto invencível
            if int(self.invincible_timer * 10) % 2 == 0: # Pisca a cada 0.1s
                self.image = pygame.Surface((1,1), pygame.SRCALPHA) # Torna invisível
            else:
                self.image = self.original_image # Volta a imagem original
        else:
            self.image = self.original_image # Garante que a imagem esteja normal quando não invencível

        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        if self.on_ground:
            self.rect.x += dx
        else:
            self.rect.x += dx * 0.7

        self.is_moving = (dx != 0)

        if not self.on_ground:
            self.y_velocity += const.GRAVITY * delta_time
        self.rect.y += self.y_velocity * delta_time

        if self.rect.y >= const.PLAYER_GROUND_Y:
            self.rect.y = const.PLAYER_GROUND_Y
            if not self.on_ground:
                self.on_ground = True
                self.is_jumping = False
                self.y_velocity = 0
                self.current_jump_frame_index = 0
                self.jump_animation_timer = 0.0

        # Atualiza animações (jump, walk, idle)
        # IMPORTANTE: A lógica de animação foi movida para DENTRO
        # do else do invencible_timer para não conflitar com o piscar
        # e para garantir que a animação seja aplicada à self.original_image
        # e depois copiada para self.image, se necessário.

        current_animation_image = self.idle_image # Imagem base
        if self.is_jumping or not self.on_ground:
            if self.jump_frames:
                self.jump_animation_timer += delta_time
                if self.jump_animation_timer >= const.JUMP_ANIMATION_SPEED:
                    self.jump_animation_timer -= const.JUMP_ANIMATION_SPEED
                    self.current_jump_frame_index = (self.current_jump_frame_index + 1) % len(self.jump_frames)
                current_animation_image = self.jump_frames[self.current_jump_frame_index]
        elif self.is_moving:
            if self.walk_frames:
                self.walk_animation_timer += delta_time
                if self.walk_animation_timer >= self.walk_animation_speed:
                    self.walk_animation_timer -= self.walk_animation_speed
                    self.current_walk_frame_index = (self.current_walk_frame_index + 1) % len(self.walk_frames)
                current_animation_image = self.walk_frames[self.current_walk_frame_index]
        else:
            # Já está self.idle_image
            self.current_walk_frame_index = 0
            self.walk_animation_timer = 0.0
            self.current_jump_frame_index = 0
            self.jump_animation_timer = 0.0

        self.original_image = current_animation_image # Atualiza a imagem base (não invencível)

        self.shots_group.update(delta_time)

    def draw(self, surface, camera_offset_x):
        # O self.image já é atualizado no update para piscar
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))

        for shot in self.shots_group:
            shot.draw(surface, camera_offset_x)

    def get_rect(self):
        return self.rect