# code/level.py
import pygame
import os
import random
from . import const
from .player import Player
from .enemy import Enemy1, Enemy2, Enemy3
from .entity_mediator import EntityMediator


class Level:
    # O __init__ agora aceita a vida do jogador como argumento
    def __init__(self, screen, bg_prefix, bg_count, bg_start_index, level_actual_width, player_lives):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.level_width = level_actual_width

        # --- MUDANÇA PRINCIPAL AQUI ---
        # Cria o jogador passando a vida recebida
        self.player = Player((const.PLAYER_START_X, const.PLAYER_START_Y), starting_lives=player_lives)

        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.enemy_spawn_timer = 0.0
        self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN, const.ENEMY_SPAWN_INTERVAL_MAX)
        self.camera_offset_x = 0
        self._load_assets(bg_prefix, bg_count, bg_start_index)

    # O resto do arquivo continua igual...
    def _load_assets(self, bg_prefix, bg_count, bg_start_index):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(base_dir, '..', 'asset')
        self.parallax_layers = []
        scroll_factors = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0][:bg_count]
        for i in range(bg_start_index, bg_start_index + bg_count):
            path = os.path.join(asset_dir, f'{bg_prefix}{i}.png')
            try:
                img = pygame.image.load(path).convert_alpha()
                sw = int(img.get_width() * (self.screen_height / img.get_height()))
                img = pygame.transform.scale(img, (sw, self.screen_height))
                self.parallax_layers.append({'image': img, 'scroll_factor': scroll_factors[i - bg_start_index]})
            except Exception as e:
                print(f"[ERRO PARALLAX] {path}: {e}");
                self.parallax_layers.clear();
                break
        if not self.parallax_layers: self.fallback_bg_color = const.BLUE_SKY_COLOR
        try:
            img = pygame.image.load(os.path.join(asset_dir, 'lifeplayer.PNG')).convert_alpha()
            self.heart_image = pygame.transform.scale(img, (30, 25))
        except pygame.error as e:
            self.heart_image = pygame.Surface((30, 25), pygame.SRCALPHA);
            self.heart_image.fill(const.RED_COLOR)
            print(f"ERRO: Não foi possível carregar a imagem do coração: {e}")
        try:
            self.font = pygame.font.Font(os.path.join(asset_dir, f'{const.FONT_NAME}.ttf'), 24)
        except Exception as e:
            self.font = pygame.font.Font(None, 24);
            print(f"ERRO: Não foi possível carregar a fonte: {e}. Usando fonte padrão.")

    def _update_camera(self):
        target_x = self.player.rect.centerx - self.screen_width // 2
        self.camera_offset_x = max(0, min(target_x, self.level_width - self.screen_width))
        self.player.rect.left = max(self.camera_offset_x, self.player.rect.left)
        self.player.rect.right = min(self.camera_offset_x + self.screen_width, self.player.rect.right)

    def _spawn_enemy(self):
        enemy_class = random.choice([Enemy1, Enemy2, Enemy3])
        spawn_x = self.camera_offset_x + self.screen_width + const.ENEMY_SPAWN_X_OFFSET
        spawn_y = const.ENEMY_START_Y
        new_enemy = enemy_class((spawn_x, spawn_y));
        self.enemies.add(new_enemy)

    def _draw_elements(self):
        self.screen.fill(self.fallback_bg_color if not self.parallax_layers else const.BLACK_COLOR)
        if self.parallax_layers:
            for layer in self.parallax_layers:
                scroll = self.camera_offset_x * layer['scroll_factor'];
                img_width = layer['image'].get_width()
                x = -(scroll % img_width)
                while x < self.screen_width:
                    self.screen.blit(layer['image'], (x, 0));
                    x += img_width
        for enemy in self.enemies: enemy.draw(self.screen, self.camera_offset_x)
        for shot in self.enemy_shots: shot.draw(self.screen, self.camera_offset_x)
        self.player.draw(self.screen, self.camera_offset_x)
        for shot in self.player.shots_group: shot.draw(self.screen, self.camera_offset_x)
        if self.heart_image:
            self.screen.blit(self.heart_image, (10, 10))
            lives_text = self.font.render(f"x{self.player.lives}", True, const.WHITE_COLOR)
            self.screen.blit(lives_text, (10 + self.heart_image.get_width() + 5, 10))
        pygame.display.flip()

    def run(self, clock):
        while True:
            delta_time = clock.tick(const.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return "quit"
                self.player.handle_event(event)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]: self.player.shoot()
            if delta_time > 0:
                self.enemy_spawn_timer += delta_time
                if self.enemy_spawn_timer >= self.next_spawn_time:
                    self._spawn_enemy();
                    self.enemy_spawn_timer = 0.0
                    self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN,
                                                          const.ENEMY_SPAWN_INTERVAL_MAX)
                self.player.update(delta_time, self.camera_offset_x, self.screen_width)
                self.enemies.update(delta_time, self.camera_offset_x, self.screen_width)
                self.enemy_shots.empty()
                for enemy in self.enemies: self.enemy_shots.add(enemy.shots_group.sprites())
                EntityMediator.check_all_collisions(self.player, self.enemies, self.player.shots_group,
                                                    self.enemy_shots)
                if self.player.lives <= 0: return const.GAME_STATE_GAME_OVER_LOSE
                self._update_camera()
                if self.player.rect.x >= self.level_width - self.player.rect.width: return "level_complete"
            self._draw_elements()