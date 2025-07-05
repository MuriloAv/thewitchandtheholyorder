# code/game.py
import pygame
from .menu import Menu
import os
from .level import Level
from . import const


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption(const.GAME_TITLE)
        self.relogio = pygame.time.Clock()
        self.game_state = const.GAME_STATE_MENU
        self.previous_game_state = None
        self.current_playing_music = None
        self.current_level_number = 0

        # --- MUDANÇA PRINCIPAL AQUI ---
        # A classe Game agora tem uma variável para guardar a vida do jogador
        self.player_current_lives = const.PLAYER_LIVES_START

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.game_music_path = os.path.join(base_dir, '..', 'asset', 'gamesong.mp3')
        self.menu_music_path = os.path.join(base_dir, '..', 'asset', 'menusong.mp3')
        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', f'{const.FONT_NAME}.ttf')
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)
        self.level = None
        self.pontuacao = 0

        try:
            win_img_path = os.path.join(base_dir, '..', const.GAME_OVER_WIN_IMAGE)
            self.win_background_image = pygame.transform.scale(pygame.image.load(win_img_path).convert_alpha(),
                                                               (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error as e:
            self.win_background_image = None; print(f"Erro ao carregar a imagem de vitória: {e}")
        try:
            lose_img_path = os.path.join(base_dir, '..', const.GAME_OVER_LOSE_IMAGE)
            self.lose_background_image = pygame.transform.scale(pygame.image.load(lose_img_path).convert_alpha(),
                                                                (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error as e:
            self.lose_background_image = None; print(f"ERRO: Não foi possível carregar a imagem de derrota: {e}")

    def _load_level(self, level_num):
        bg_prefix, bg_count, bg_start_index, level_width = '', 0, 0, 0
        if level_num == 1:
            bg_prefix, bg_count, bg_start_index, level_width = const.LVL1_BG_PREFIX, const.LVL1_BG_COUNT, const.LVL1_BG_START_INDEX, const.LEVEL1_WIDTH
        elif level_num == 2:
            bg_prefix, bg_count, bg_start_index, level_width = const.LVL2_BG_PREFIX, const.LVL2_BG_COUNT, const.LVL2_BG_START_INDEX, const.LEVEL2_WIDTH
        elif level_num == 3:
            bg_prefix, bg_count, bg_start_index, level_width = const.LVL3_BG_PREFIX, const.LVL3_BG_COUNT, const.LVL3_BG_START_INDEX, const.LEVEL3_WIDTH
        else:
            self.game_state = const.GAME_STATE_GAME_OVER_WIN;
            return

        # --- MUDANÇA PRINCIPAL AQUI ---
        # Passa a vida atual do jogador ao criar o novo nível
        self.level = Level(self.tela, bg_prefix, bg_count, bg_start_index, level_width,
                           player_lives=self.player_current_lives)
        self.current_level_number = level_num

    def _get_translated_text(self, key, default_text):
        return self.menu.translations[self.menu.current_language].get(key, default_text)

    def run(self):
        rodando = True
        while rodando:
            if self.game_state != self.previous_game_state:
                music_path = None
                if self.game_state == const.GAME_STATE_MENU:
                    music_path = self.menu_music_path
                elif self.game_state == const.GAME_STATE_PLAYING:
                    music_path = self.game_music_path
                if music_path:
                    try:
                        pygame.mixer.music.load(music_path);
                        pygame.mixer.music.play(-1)
                    except pygame.error as e:
                        print(f"ERRO ao tocar música: {e}")
                else:
                    pygame.mixer.music.stop()
                self.previous_game_state = self.game_state

            if self.game_state == const.GAME_STATE_MENU:
                # Reseta a vida do jogador quando volta para o menu
                self.player_current_lives = const.PLAYER_LIVES_START
                action = self.menu.run()
                if action == "start_game":
                    self.game_state = const.GAME_STATE_PLAYING;
                    self._load_level(1)
                elif action == "quit":
                    self.game_state = const.GAME_STATE_QUIT

            elif self.game_state == const.GAME_STATE_PLAYING:
                if self.level:
                    action = self.level.run(self.relogio)
                    if action == "quit":
                        self.game_state = const.GAME_STATE_QUIT
                    elif action == "level_complete":
                        # --- MUDANÇA PRINCIPAL AQUI ---
                        # Salva a vida do jogador antes de carregar o próximo nível
                        self.player_current_lives = self.level.player.lives
                        self.current_level_number += 1
                        if self.current_level_number <= const.MAX_GAME_LEVELS:
                            self._load_level(self.current_level_number)
                        else:
                            self.game_state = const.GAME_STATE_GAME_OVER_WIN
                    elif action == const.GAME_STATE_GAME_OVER_LOSE:
                        self.game_state = const.GAME_STATE_GAME_OVER_LOSE
                else:
                    self.game_state = const.GAME_STATE_MENU

            elif self.game_state in [const.GAME_STATE_GAME_OVER_WIN, const.GAME_STATE_GAME_OVER_LOSE]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.game_state = const.GAME_STATE_QUIT
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                        self.game_state = const.GAME_STATE_MENU

                is_win = self.game_state == const.GAME_STATE_GAME_OVER_WIN
                bg_image = self.win_background_image if is_win else self.lose_background_image
                text_key = "win_message" if is_win else "game_over_message"
                default_text = const.WIN_TEXT_EN if is_win else const.GAME_OVER_TEXT_EN

                self.tela.blit(bg_image, (0, 0)) if bg_image else self.tela.fill(const.BLACK_COLOR)
                text_surface = self.menu.font.render(self._get_translated_text(text_key, default_text), True,
                                                     const.WHITE_COLOR)
                self.tela.blit(text_surface,
                               text_surface.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2)))
                pygame.display.flip();
                self.relogio.tick(const.FPS)

            elif self.game_state == const.GAME_STATE_QUIT:
                rodando = False
        pygame.quit()