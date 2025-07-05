# code/player.py

import pygame
import os
from . import const  # Garanta que const está sendo importado
from .playershot import PlayerShot


class Player(pygame.sprite.Sprite):
    """Representa o personagem do jogador, controlando seu estado, movimento e ações."""

    def __init__(self, position):
        super().__init__()
        self.name = "Player"
        self.speed = const.PLAYER_SPEED

        # --- CONTROLE DE TIRO ---
        # AQUI ESTÁ A MUDANÇA: Usa a constante em vez de um número fixo.
        self.shoot_cooldown = const.PLAYER_SHOOT_COOLDOWN
        self.time_since_last_shot = self.shoot_cooldown
        self.shots_group = pygame.sprite.Group()

        # ... (o resto do arquivo player.py pode continuar exatamente como estava)
        # --- VIDA E INVENCIBILIDADE ---
        self.lives = const.PLAYER_LIVES_START
        self.invincible_timer = 0.0
        self.invincible_duration = const.PLAYER_INVINCIBILITY_DURATION

        # --- FÍSICA E MOVIMENTO ---
        self.on_ground = True
        self.is_jumping = False
        self.y_velocity = 0

        # --- ANIMAÇÕES E IMAGENS ---
        self._load_animation_frames()
        self.image = self.idle_image if self.idle_image else pygame.Surface((const.PLAYER_WIDTH, const.PLAYER_HEIGHT),
                                                                            pygame.SRCALPHA)
        if not self.idle_image:
            self.image.fill(const.RED_COLOR)
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=position)
        self.is_moving = False

        self.animation_timer = 0.0
        self.current_frame_index = 0

    def _load_animation_frames(self):
        """Carrega todos os frames de animação do jogador a partir dos assets."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        try:
            img = pygame.image.load(os.path.join(asset_path, 'playerwalk0.png')).convert_alpha()
            self.idle_image = pygame.transform.scale(img, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT))
        except pygame.error as e:
            self.idle_image = None
            print(f"Erro ao carregar imagem IDLE do jogador: {e}")

        self.walk_frames = []
        for i in range(1, 8):
            try:
                img = pygame.image.load(os.path.join(asset_path, f'playerwalk{i}.png')).convert_alpha()
                self.walk_frames.append(pygame.transform.scale(img, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT)))
            except pygame.error as e:
                print(f"Erro ao carregar frame de caminhada 'playerwalk{i}.png': {e}")

        self.jump_frames = []
        for i in range(1, 7):
            try:
                img = pygame.image.load(os.path.join(asset_path, f'pulo{i}.png')).convert_alpha()
                self.jump_frames.append(pygame.transform.scale(img, (const.PLAYER_WIDTH, const.PLAYER_HEIGHT)))
            except pygame.error as e:
                print(f"Erro ao carregar frame de pulo 'pulo{i}.png': {e}")

    def handle_event(self, event):
        """Lida com eventos de input discretos (como um pulo)."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and self.on_ground:
            self.is_jumping = True
            self.on_ground = False
            self.y_velocity = -const.JUMP_STRENGTH

    def shoot(self):
        """Cria um novo projétil se o tempo de cooldown já passou."""
        if self.time_since_last_shot >= self.shoot_cooldown:
            new_shot = PlayerShot(self.rect.midright, direction=1)
            self.shots_group.add(new_shot)
            self.time_since_last_shot = 0.0

    def take_damage(self, amount):
        """Aplica dano ao jogador e ativa um temporizador de invencibilidade."""
        if self.invincible_timer <= 0:
            self.lives -= amount
            self.invincible_timer = self.invincible_duration

    def update(self, delta_time, camera_offset_x, screen_width):
        """Atualiza toda a lógica do jogador a cada frame."""
        self.time_since_last_shot += delta_time
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time

        self._update_movement(delta_time)
        self._update_animation(delta_time)

        self.shots_group.update(delta_time, camera_offset_x, screen_width)

    def _update_movement(self, delta_time):
        """Gerencia a movimentação horizontal e vertical (pulo/gravidade)."""
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed

        move_multiplier = 0.7 if not self.on_ground else 1.0
        self.rect.x += dx * move_multiplier

        self.is_moving = (dx != 0)

        if not self.on_ground:
            self.y_velocity += const.GRAVITY * delta_time
        self.rect.y += self.y_velocity * delta_time

        if self.rect.bottom >= const.PLAYER_GROUND_Y:
            self.rect.bottom = const.PLAYER_GROUND_Y
            self.on_ground = True
            self.is_jumping = False
            self.y_velocity = 0

    def _update_animation(self, delta_time):
        """Atualiza a imagem do jogador baseada em seu estado (parado, andando, pulando)."""
        current_animation = None
        animation_speed = 0.1

        if self.is_jumping and self.jump_frames:
            current_animation = self.jump_frames
            animation_speed = const.JUMP_ANIMATION_SPEED
        elif self.is_moving and self.walk_frames:
            current_animation = self.walk_frames
        else:
            self.image = self.idle_image
            self.current_frame_index = 0
            return

        if current_animation:
            self.animation_timer += delta_time
            if self.animation_timer >= animation_speed:
                self.animation_timer = 0.0
                self.current_frame_index = (self.current_frame_index + 1) % len(current_animation)
                self.original_image = current_animation[self.current_frame_index]
                self.image = self.original_image

        if self.invincible_timer > 0:
            if int(self.invincible_timer * 10) % 2 == 0:
                self.image = pygame.Surface((1, 1), pygame.SRCALPHA)

    def draw(self, surface, camera_offset_x):
        """Desenha o jogador na tela."""
        screen_x = self.rect.x - camera_offset_x
        surface.blit(self.image, (screen_x, self.rect.y))