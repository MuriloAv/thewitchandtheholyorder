# code/enemy.py
import pygame
import os
import random
from . import const
from .enemyshot import EnemyShot


class Enemy(pygame.sprite.Sprite):
    """Classe base para todos os inimigos do jogo."""

    def __init__(self, position, speed, animation_speed, animation_prefix, num_frames):
        super().__init__()
        self.name = f"{animation_prefix.replace('walk', '')}"
        self.speed = speed
        self.animation_speed = animation_speed
        self.walk_frames = []
        self._load_animation_frames(animation_prefix, num_frames)

        if self.walk_frames:
            self.image = self.walk_frames[0]
        else:
            self.image = pygame.Surface((const.ENEMY_WIDTH, const.ENEMY_HEIGHT), pygame.SRCALPHA)
            self.image.fill(const.RED_COLOR)

        self.rect = self.image.get_rect(topleft=position)
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.health = 100

        self.shoot_cooldown = 2.0
        self.shots_group = pygame.sprite.Group()

        # --- NOVA LÓGICA DE CONTROLE ---
        # Esta flag controla se o primeiro tiro (ao entrar na tela) já foi dado.
        self.has_fired_on_screen = False
        self.time_since_last_shot = 0.0

    def _load_animation_frames(self, prefix, num_frames):
        """Carrega os frames de animação para o inimigo."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')
        for i in range(1, num_frames + 1):
            frame_file = os.path.join(asset_path, f'{prefix}{i}.png')
            try:
                img = pygame.image.load(frame_file).convert_alpha()
                self.walk_frames.append(pygame.transform.scale(img, (const.ENEMY_WIDTH, const.ENEMY_HEIGHT)))
            except pygame.error as e:
                print(f"Erro ao carregar frame '{frame_file}': {e}")

    def update(self, delta_time, camera_offset_x, screen_width):
        """Atualiza a lógica do inimigo com a verificação de entrada na tela."""
        # Movimento e animação sempre acontecem
        self.rect.x -= self.speed * delta_time
        if self.walk_frames:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.current_frame_index = (self.current_frame_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame_index]

        # --- LÓGICA DE TIRO COMPLETAMENTE REFEITA ---

        # 1. Verifica se o primeiro tiro já foi dado
        if not self.has_fired_on_screen:
            # 2. Se não foi, verifica se o inimigo ENTROU na tela
            # (a borda direita do inimigo é menor que a borda direita da tela)
            if self.rect.right < camera_offset_x + screen_width:
                self.shoot()
                self.has_fired_on_screen = True  # Marca que o primeiro tiro já foi
                self.time_since_last_shot = 0.0  # Inicia o cooldown para o PRÓXIMO tiro

        # 3. Se o primeiro tiro já foi, usa a lógica de cooldown normal
        else:
            self.time_since_last_shot += delta_time
            if self.time_since_last_shot >= self.shoot_cooldown:
                self.shoot()
                self.time_since_last_shot = 0.0

        # Atualiza os projéteis e remove o inimigo se sair da tela
        self.shots_group.update(delta_time, camera_offset_x, screen_width)
        if self.rect.right < 0:
            self.kill()

    def shoot(self):
        """Método de tiro a ser implementado pelas subclasses."""
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def draw(self, surface, camera_offset_x):
        screen_x = self.rect.x - camera_offset_x
        surface.blit(self.image, (screen_x, self.rect.y))
        for shot in self.shots_group:
            shot.draw(surface, camera_offset_x)


# --- Subclasses de Inimigos Específicos ---
# Nenhuma mudança necessária aqui, elas herdam o novo comportamento.

class Enemy1(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY1_SPEED, const.ENEMY1_ANIMATION_SPEED, "enemy1walk", 6)
        self.health = const.ENEMY1_HEALTH
        self.shoot_cooldown = const.ENEMY1_SHOOT_COOLDOWN

    def shoot(self):
        new_shot = EnemyShot(self.rect.midleft, 'enemy1', direction=-1)
        self.shots_group.add(new_shot)


class Enemy2(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY2_SPEED, const.ENEMY2_ANIMATION_SPEED, "enemy2walk", 4)
        self.health = const.ENEMY2_HEALTH
        self.shoot_cooldown = const.ENEMY2_SHOOT_COOLDOWN

    def shoot(self):
        new_shot = EnemyShot(self.rect.midleft, 'enemy2', direction=-1)
        self.shots_group.add(new_shot)


class Enemy3(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY3_SPEED, const.ENEMY3_ANIMATION_SPEED, "enemy3walk", 5)
        self.health = const.ENEMY3_HEALTH
        self.shoot_cooldown = const.ENEMY3_SHOOT_COOLDOWN

    def shoot(self):
        new_shot = EnemyShot(self.rect.midleft, 'enemy3', direction=-1)
        self.shots_group.add(new_shot)