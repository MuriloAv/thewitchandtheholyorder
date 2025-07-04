import pygame
import os
import random
from . import const
from .player import Player
from .enemy import Enemy1, Enemy2, Enemy3
from .entity_mediator import EntityMediator


class Level:
    def __init__(self, screen, bg_prefix, bg_count, bg_start_index, level_actual_width):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.level_width = level_actual_width
        self.level_number = int(bg_prefix[3])

        # Player e seus tiros
        player_start_position = (const.PLAYER_START_X, const.PLAYER_START_Y)
        self.player = Player(player_start_position)
        self.player_shots = self.player.shots_group  # referência ao grupo de tiros do player (não muda!)

        # Enemies e tiros inimigos
        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()  # Grupo global único para tiros inimigos

        self.enemy_spawn_timer = 0.0
        self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN, const.ENEMY_SPAWN_INTERVAL_MAX)

        # Câmera
        self.camera_offset_x = 0

        # Parallax background
        self.parallax_layers = []
        scroll_factors = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0][:bg_count]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        for i in range(bg_start_index, bg_start_index + bg_count):
            filename = f'{bg_prefix}{i}.png'
            path = os.path.join(base_dir, '..', 'asset', filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                sw = int(img.get_width() * (self.screen_height / img.get_height()))
                img = pygame.transform.scale(img, (sw, self.screen_height))
                self.parallax_layers.append({
                    'image': img,
                    'scroll_factor': scroll_factors[i - bg_start_index] if i - bg_start_index < len(scroll_factors) else 1.0
                })
            except Exception as e:
                print(f"[ERRO PARALLAX] {filename}: {e}")
                self.parallax_layers.clear()
                break

        if not self.parallax_layers:
            self.fallback_bg_color = const.BLUE_SKY_COLOR

    def _update_camera(self):
        target_x = self.player.rect.centerx - self.screen_width // 2
        self.camera_offset_x = max(0, min(target_x, self.level_width - self.screen_width))
        self.player.rect.left = max(0, self.player.rect.left)
        self.player.rect.right = min(self.level_width, self.player.rect.right)

    def _spawn_enemy(self):
        enemy_class = random.choice([Enemy1, Enemy2, Enemy3])
        spawn_x = self.camera_offset_x + self.screen_width + const.ENEMY_SPAWN_X_OFFSET
        spawn_y = const.PLAYER_START_Y
        new_enemy = enemy_class((spawn_x, spawn_y))
        self.enemies.add(new_enemy)
        print(f"DEBUG: Spawned {new_enemy.name} at ({spawn_x}, {spawn_y})")

    def _draw_elements(self):
        self.screen.fill(const.BLACK_COLOR)

        if self.parallax_layers:
            for layer in self.parallax_layers:
                img = layer['image']
                scroll = int(self.camera_offset_x * layer['scroll_factor'])
                offset = scroll % img.get_width()
                x = -offset
                while x < self.screen_width:
                    self.screen.blit(img, (x, 0))
                    x += img.get_width()
        else:
            self.screen.fill(self.fallback_bg_color)

        # Desenhar player e seus tiros
        self.player.draw(self.screen, self.camera_offset_x)

        # Desenhar inimigos e seus tiros
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset_x)
        for shot in self.enemy_shots:
            shot.draw(self.screen, self.camera_offset_x)

        # Desenhar tiros do player
        for shot in self.player_shots:
            shot.draw(self.screen, self.camera_offset_x)

        pygame.display.flip()

    def run(self, clock):
        while True:
            delta_time = clock.tick(const.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "quit"
                self.player.handle_event(event)

            # Spawn de inimigos
            self.enemy_spawn_timer += delta_time
            if self.enemy_spawn_timer >= self.next_spawn_time:
                self._spawn_enemy()
                self.enemy_spawn_timer = 0.0
                self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN, const.ENEMY_SPAWN_INTERVAL_MAX)

            # Atualizar entidades
            self.player.update(delta_time)
            self.enemies.update(delta_time)

            # Atualizar tiros do player (grupo gerenciado internamente pelo player)
            self.player_shots.update(delta_time)

            # Atualizar tiros dos inimigos — adiciona tiros novos de cada inimigo no grupo global
            for enemy in self.enemies:
                for shot in enemy.shots_group:
                    if shot not in self.enemy_shots:
                        self.enemy_shots.add(shot)
            self.enemy_shots.update(delta_time)

            # Colisões
            EntityMediator.check_all_collisions(
                self.player,
                self.enemies,
                self.player_shots,
                self.enemy_shots
            )

            self._update_camera()
            self._draw_elements()

            # Checa fim do nível
            if self.player.rect.x >= self.level_width - self.player.rect.width:
                print("Nível completo!")
                self.enemies.empty()
                self.player_shots.empty()
                self.enemy_shots.empty()
                return "level_complete"
