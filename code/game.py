# code/game.py
import pygame
from .menu import Menu
import os
from .level import Level
from . import const
from .score import ScoreManager  # Importa o novo gerenciador


class Game:
    """Orquestra o jogo, gerenciando estados, níveis e o score."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption(const.GAME_TITLE)
        self.relogio = pygame.time.Clock()

        self.game_state = const.GAME_STATE_MENU
        self.previous_game_state = None
        self.current_level_number = 0
        self.player_current_lives = const.PLAYER_LIVES_START

        # O Jogo agora tem uma instância do ScoreManager
        self.score_manager = ScoreManager()

        self._load_assets()
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)
        self.level = None

    def _load_assets(self):
        """Carrega assets globais como músicas e imagens de tela."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(base_dir, '..', 'asset')

        self.game_music_path = os.path.join(asset_dir, 'gamesong.mp3')
        self.menu_music_path = os.path.join(asset_dir, 'menusong.mp3')
        self.gothic_font_path = os.path.join(asset_dir, f'{const.FONT_NAME}.ttf')

        try:
            win_img_path = os.path.join(base_dir, '..', const.GAME_OVER_WIN_IMAGE)
            self.win_background_image = pygame.transform.scale(pygame.image.load(win_img_path).convert_alpha(),
                                                               (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error:
            self.win_background_image = None
        try:
            lose_img_path = os.path.join(base_dir, '..', const.GAME_OVER_LOSE_IMAGE)
            self.lose_background_image = pygame.transform.scale(pygame.image.load(lose_img_path).convert_alpha(),
                                                                (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error:
            self.lose_background_image = None

    def _load_level(self, level_num):
        """Carrega um nível, passando o estado do jogador e o score manager."""
        level_data = {
            1: (const.LVL1_BG_PREFIX, const.LVL1_BG_COUNT, const.LVL1_BG_START_INDEX, const.LEVEL1_WIDTH),
            2: (const.LVL2_BG_PREFIX, const.LVL2_BG_COUNT, const.LVL2_BG_START_INDEX, const.LEVEL2_WIDTH),
            3: (const.LVL3_BG_PREFIX, const.LVL3_BG_COUNT, const.LVL3_BG_START_INDEX, const.LEVEL3_WIDTH),
        }
        if level_num not in level_data:
            self.game_state = const.GAME_STATE_GAME_OVER_WIN
            return

        bg_prefix, bg_count, bg_start_index, level_width = level_data[level_num]
        self.level = Level(self.tela, bg_prefix, bg_count, bg_start_index, level_width,
                           player_lives=self.player_current_lives,
                           score_manager=self.score_manager)
        self.current_level_number = level_num

    def _handle_music(self):
        """Gerencia a transição de música entre os estados do jogo."""
        if self.game_state == self.previous_game_state: return
        music_path = None
        if self.game_state == const.GAME_STATE_MENU:
            music_path = self.menu_music_path
        elif self.game_state == const.GAME_STATE_PLAYING:
            music_path = self.game_music_path
        if music_path:
            try:
                pygame.mixer.music.load(music_path); pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"ERRO ao tocar música '{music_path}': {e}")
        else:
            pygame.mixer.music.stop()
        self.previous_game_state = self.game_state

    def run(self):
        """O loop principal que gerencia os estados do jogo."""
        running = True
        while running:
            self._handle_music()

            if self.game_state == const.GAME_STATE_MENU:
                self.player_current_lives = const.PLAYER_LIVES_START
                self.score_manager.reset()  # Zera o score para uma nova partida

                action = self.menu.run()
                if action == "start_game":
                    self.game_state = const.GAME_STATE_PLAYING
                    self._load_level(1)
                elif action == "quit":
                    self.game_state = const.GAME_STATE_QUIT

            elif self.game_state == const.GAME_STATE_PLAYING:
                action = self.level.run(self.relogio)
                if action == "quit":
                    self.game_state = const.GAME_STATE_QUIT
                elif action == "level_complete":
                    self.player_current_lives = self.level.player.lives
                    self.current_level_number += 1
                    if self.current_level_number > const.MAX_GAME_LEVELS:
                        self.game_state = const.GAME_STATE_GAME_OVER_WIN
                        self.score_manager.save_current_score_if_high()  # Salva o score
                    else:
                        self._load_level(self.current_level_number)
                elif action == const.GAME_STATE_GAME_OVER_LOSE:
                    self.game_state = const.GAME_STATE_GAME_OVER_LOSE

            elif self.game_state == const.GAME_STATE_GAME_OVER_WIN:
                self._draw_win_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.game_state = const.GAME_STATE_QUIT
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                        self.game_state = const.GAME_STATE_MENU

            elif self.game_state == const.GAME_STATE_GAME_OVER_LOSE:
                self._draw_lose_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.game_state = const.GAME_STATE_QUIT
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                        self.game_state = const.GAME_STATE_MENU

            elif self.game_state == const.GAME_STATE_QUIT:
                running = False
        pygame.quit()

    def _draw_win_screen(self):
        """Desenha a tela de vitória com o score final e o ranking."""
        self.tela.blit(self.win_background_image, (0, 0)) if self.win_background_image else self.tela.fill(
            const.BLACK_COLOR)

        # Mensagem de Vitória
        win_text = self.menu.translations[self.menu.current_language].get("win_message", const.WIN_TEXT_EN)
        win_surface = self.menu.font.render(win_text, True, const.WHITE_COLOR)
        self.tela.blit(win_surface, win_surface.get_rect(center=(const.SCREEN_WIDTH / 2, 100)))

        # Score Final
        final_score_text = f"Seu Score Final: {self.score_manager.get_current_score()} abates"
        final_score_surface = self.menu.font.render(final_score_text, True, const.YELLOW_COLOR)
        self.tela.blit(final_score_surface, final_score_surface.get_rect(center=(const.SCREEN_WIDTH / 2, 180)))

        # Ranking
        y_pos = 250
        ranking_font = pygame.font.Font(self.gothic_font_path, 32)
        title_surface = ranking_font.render("High Scores:", True, const.WHITE_COLOR)
        self.tela.blit(title_surface, title_surface.get_rect(center=(const.SCREEN_WIDTH / 2, y_pos)))
        y_pos += 40

        for i, score_entry in enumerate(self.score_manager.get_high_scores()[:5]):
            score_text = f"{i + 1}. {score_entry['score']} abates"
            score_surface = ranking_font.render(score_text, True, const.WHITE_COLOR)
            self.tela.blit(score_surface, score_surface.get_rect(center=(const.SCREEN_WIDTH / 2, y_pos)))
            y_pos += 35

        pygame.display.flip()
        self.relogio.tick(const.FPS)

    def _draw_lose_screen(self):
        """Desenha a tela de derrota."""
        self.tela.blit(self.lose_background_image, (0, 0)) if self.lose_background_image else self.tela.fill(
            const.BLACK_COLOR)
        text = self.menu.translations[self.menu.current_language].get("game_over_message", const.GAME_OVER_TEXT_EN)
        text_surface = self.menu.font.render(text, True, const.WHITE_COLOR)
        self.tela.blit(text_surface, text_surface.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2)))
        pygame.display.flip()
        self.relogio.tick(const.FPS)