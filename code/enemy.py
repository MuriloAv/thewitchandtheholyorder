import pygame
import os
from . import const
from .enemyshot import EnemyShot  # Importa EnemyShot para os tiros dos inimigos


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, speed, animation_speed, animation_prefix, num_frames):
        super().__init__()
        self.name = f"{animation_prefix.replace('walk', '')}_{id(self)}"

        self.speed = speed
        self.animation_speed = animation_speed

        self.walk_frames = []
        self._load_animation_frames(animation_prefix, num_frames)

        # Imagem inicial
        if self.walk_frames:
            self.image = self.walk_frames[0]
        else:
            self.image = pygame.Surface((const.ENEMY_WIDTH, const.ENEMY_HEIGHT), pygame.SRCALPHA)
            self.image.fill(const.RED_COLOR)
            print(f"AVISO: Nenhuma imagem de inimigo carregada para {animation_prefix}. Usando fallback.")

        self.rect = self.image.get_rect(topleft=position)

        self.current_frame_index = 0
        self.animation_timer = 0.0

        self.health = 100

        # Tiro
        self.shoot_cooldown = 2.0
        self.time_since_last_shot = 0.0
        self.shots_group = pygame.sprite.Group()

    def _load_animation_frames(self, prefix, num_frames):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_dir, '..', 'asset')

        for i in range(1, num_frames + 1):
            frame_file = os.path.join(asset_path, f'{prefix}{i}.png')
            try:
                temp_image = pygame.image.load(frame_file).convert_alpha()
                scaled_image = pygame.transform.scale(temp_image, (const.ENEMY_WIDTH, const.ENEMY_HEIGHT))
                self.walk_frames.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar frame '{frame_file}': {e}")

    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time

        if self.walk_frames:
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                self.current_frame_index = (self.current_frame_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame_index]

        self.time_since_last_shot += delta_time
        if self.time_since_last_shot >= self.shoot_cooldown:
            self.shoot()
            self.time_since_last_shot = 0.0

        self.shots_group.update(delta_time)

        if self.rect.right < 0:
            self.kill()

    def shoot(self):
        # Sobrescrito nas subclasses
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            print(f"{self.name} foi destruído!")

    def draw(self, surface, camera_offset_x):
        screen_x = int(self.rect.x - camera_offset_x)
        surface.blit(self.image, (screen_x, self.rect.y))

        # Desenha todos os tiros desse inimigo
        for shot in self.shots_group:
            shot.draw(surface, camera_offset_x)


# --- Subclasses específicas para tipos de inimigo ---

class Enemy1(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY1_SPEED, const.ENEMY1_ANIMATION_SPEED, "enemy1walk", 6)
        self.health = const.ENEMY1_HEALTH
        self.shoot_cooldown = 0.5

    def shoot(self):
        # shot_pos = self.rect.midleft # Antigo
        shot_pos_x = self.rect.centerx - 20  # Exemplo: 20 pixels à esquerda do centro
        shot_pos_y = self.rect.centery
        new_shot = EnemyShot((shot_pos_x, shot_pos_y), 'enemy1')  # Ou 'enemy2', 'enemy3'
        self.shots_group.add(new_shot)


class Enemy2(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY2_SPEED, const.ENEMY2_ANIMATION_SPEED, "enemy2walk", 4)
        self.health = const.ENEMY2_HEALTH
        self.shoot_cooldown = 0.5

    def shoot(self):
        # shot_pos = self.rect.midleft # Antigo
        shot_pos_x = self.rect.centerx - 20  # Exemplo: 20 pixels à esquerda do centro
        shot_pos_y = self.rect.centery
        new_shot = EnemyShot((shot_pos_x, shot_pos_y), 'enemy2')  # Ou 'enemy2', 'enemy3'
        self.shots_group.add(new_shot)


class Enemy3(Enemy):
    def __init__(self, position):
        super().__init__(position, const.ENEMY3_SPEED, const.ENEMY3_ANIMATION_SPEED, "enemy3walk", 5)
        self.health = const.ENEMY3_HEALTH
        self.shoot_cooldown = 0.7

    def shoot(self):
        # shot_pos = self.rect.midleft # Antigo
        shot_pos_x = self.rect.centerx - 20  # Exemplo: 20 pixels à esquerda do centro
        shot_pos_y = self.rect.centery
        new_shot = EnemyShot((shot_pos_x, shot_pos_y), 'enemy3')  # Ou 'enemy2', 'enemy3'
        self.shots_group.add(new_shot)
