# code/level.py

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

        player_start_position = (const.PLAYER_START_X, const.PLAYER_START_Y)
        self.player = Player(player_start_position)
        self.player_shots = self.player.shots_group

        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()

        self.enemy_spawn_timer = 0.0
        self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN, const.ENEMY_SPAWN_INTERVAL_MAX)

        self.camera_offset_x = 0

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
                    'scroll_factor': scroll_factors[i - bg_start_index] if i - bg_start_index < len(
                        scroll_factors) else 1.0
                })
            except Exception as e:
                print(f"[ERRO PARALLAX] {filename}: {e}")
                self.parallax_layers.clear()
                break

        if not self.parallax_layers:
            self.fallback_bg_color = const.BLUE_SKY_COLOR

        self.heart_image = None
        heart_image_path = os.path.join(base_dir, '..', 'asset', 'lifeplayer.PNG')
        try:
            temp_heart_img = pygame.image.load(heart_image_path).convert_alpha()
            self.heart_image = pygame.transform.scale(temp_heart_img, (30, 25))
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem do coração '{heart_image_path}': {e}")
            self.heart_image = pygame.Surface((30, 25), pygame.SRCALPHA)
            self.heart_image.fill(const.RED_COLOR)

        font_path = os.path.join(base_dir, '..', 'asset', f'{const.FONT_NAME}.ttf')
        try:
            self.font = pygame.font.Font(font_path, 24)
        except Exception as e:
            print(f"ERRO: Não foi possível carregar a fonte '{font_path}': {e}. Usando fonte padrão.")
            self.font = pygame.font.Font(None, 24)

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
        print(f"DEBUG_LEVEL: Spawned {new_enemy.name} at ({spawn_x}, {spawn_y})")  # DEBUG

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

        self.player.draw(self.screen, self.camera_offset_x)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset_x)
        for shot in self.enemy_shots:
            shot.draw(self.screen, self.camera_offset_x)

        for shot in self.player_shots:
            shot.draw(self.screen, self.camera_offset_x)

        if self.heart_image:
            self.screen.blit(self.heart_image, (10, 10))

        lives_text_surface = self.font.render(f"x{self.player.lives}", True, const.WHITE_COLOR)
        self.screen.blit(lives_text_surface, (10 + self.heart_image.get_width() + 5, 10))

        pygame.display.flip()

    def run(self, clock):
        # Garante que o primeiro delta_time é válido e não zero
        clock.tick(const.FPS)

        # Variável para controlar a taxa de prints de DEBUG_LEVEL_RUN
        debug_print_timer = 0.0
        debug_print_interval = 0.5  # Printa a cada 0.5 segundos

        while True:
            dt_raw = clock.tick(const.FPS)
            delta_time = dt_raw / 1000.0

            # DEBUG: Printar a cada intervalo para não lotar o terminal
            debug_print_timer += delta_time
            if debug_print_timer >= debug_print_interval:
                print(
                    f"DEBUG_LEVEL_RUN: Frame start. Delta time: {delta_time:.4f}. Player X: {self.player.rect.x}. Camera X: {self.camera_offset_x}")
                debug_print_timer = 0.0  # Resetar timer

            # Processamento de Eventos:
            # Coletamos os eventos e os passamos para o player para pulo e quit.
            # A checagem de K_SPACE para atirar será feita AQUI no Level.run.
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        (event.type == pygame.K_ESCAPE and event.type == pygame.KEYDOWN):  # K_ESCAPE para sair
                    return "quit"

                # ADICIONADO: Print para QUALQUER tecla pressionada (fora do player)
                if event.type == pygame.KEYDOWN:
                    print(f"DEBUG_LEVEL_EVENT: KEYDOWN detected in Level.run: Key: {event.key} (ASCII: {event.key})")

                # ADICIONADO: Print para QUALQUER tecla solta (fora do player)
                if event.type == pygame.KEYUP:
                    print(f"DEBUG_LEVEL_EVENT: KEYUP detected in Level.run: Key: {event.key} (ASCII: {event.key})")
                    if event.key == pygame.K_SPACE:  # NOVO: Reinicia a flag de tiro ao soltar K_SPACE aqui no Level.
                        self.player.can_shoot = True  # Esta flag deve estar no player para ser acessada.
                        print("DEBUG_LEVEL_EVENT: K_SPACE released, player can shoot again.")

                self.player.handle_event(event)  # Passa o evento para o player (agora apenas para pulo)

            # NOVO: Checagem direta de K_SPACE usando pygame.key.get_pressed() aqui no Level.run()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # Chamamos o shoot() do player aqui. A lógica de cooldown está dentro do player.
                # A flag can_shoot também é usada aqui para evitar spam de tiro mantendo a tecla.
                if self.player.can_shoot:  # Apenas se a flag permitir (evita spam ao segurar)
                    self.player.shoot()
                    self.player.can_shoot = False  # Impede novo tiro até a tecla ser solta (KEYUP)

            # Lógica de atualização só acontece se houver tempo decorrido válido
            if delta_time > 0:
                self.enemy_spawn_timer += delta_time
                if self.enemy_spawn_timer >= self.next_spawn_time:
                    self._spawn_enemy()
                    self.enemy_spawn_timer = 0.0
                    self.next_spawn_time = random.uniform(const.ENEMY_SPAWN_INTERVAL_MIN,
                                                          const.ENEMY_SPAWN_INTERVAL_MAX)

                self.player.update(delta_time)  # O player ainda atualiza seus próprios tiros.
                self.enemies.update(delta_time)

                for enemy in self.enemies:
                    for shot in list(enemy.shots_group):
                        if shot.alive():
                            self.enemy_shots.add(shot)
                self.enemy_shots.update(delta_time)

                for shot in list(self.enemy_shots):
                    if not shot.alive():
                        self.enemy_shots.remove(shot)

                EntityMediator.check_all_collisions(
                    self.player,
                    self.enemies,
                    self.player_shots,
                    self.enemy_shots
                )

                if self.player.lives <= 0:
                    print("DEBUG_LEVEL: Player died, returning GAME_OVER_LOSE.")  # DEBUG
                    self.enemies.empty()
                    self.player_shots.empty()
                    self.enemy_shots.empty()
                    return const.GAME_STATE_GAME_OVER_LOSE

                self._update_camera()

                if self.player.rect.x >= self.level_width - self.player.rect.width:
                    print("DEBUG_LEVEL: Level complete, returning 'level_complete'.")  # DEBUG
                    self.enemies.empty()
                    self.player_shots.empty()
                    self.enemy_shots.empty()
                    return "level_complete"

            self._draw_elements()