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

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.game_music_path = os.path.join(base_dir, '..', 'asset', 'gamesong.mp3')
        self.menu_music_path = os.path.join(base_dir, '..', 'asset', 'menusong.mp3')

        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', f'{const.FONT_NAME}.ttf')

        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)

        self.level = None

        self.pontuacao = 0

        # Carrega a imagem de vitória
        win_image_full_path = os.path.join(base_dir, '..', const.GAME_OVER_WIN_IMAGE)
        try:
            self.win_background_image = pygame.image.load(win_image_full_path).convert_alpha()
            self.win_background_image = pygame.transform.scale(self.win_background_image,
                                                               (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de vitória '{win_image_full_path}': {e}")
            self.win_background_image = None

        # Carrega a imagem de derrota (Game Over)
        lose_image_full_path = os.path.join(base_dir, '..', const.GAME_OVER_LOSE_IMAGE)
        try:
            self.lose_background_image = pygame.image.load(lose_image_full_path).convert_alpha()
            self.lose_background_image = pygame.transform.scale(self.lose_background_image,
                                                               (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem de derrota '{lose_image_full_path}': {e}")
            self.lose_background_image = None


    def _load_level(self, level_num: int):
        bg_prefix = ''
        bg_count = 0
        bg_start_index = 0
        level_width = 0

        if level_num == 1:
            bg_prefix = const.LVL1_BG_PREFIX
            bg_count = const.LVL1_BG_COUNT
            bg_start_index = const.LVL1_BG_START_INDEX
            level_width = const.LEVEL1_WIDTH
            print(f"DEBUG: Carregando Nível 1 com background '{bg_prefix}'.")
        elif level_num == 2:
            bg_prefix = const.LVL2_BG_PREFIX
            bg_count = const.LVL2_BG_COUNT
            bg_start_index = const.LVL2_BG_START_INDEX
            level_width = const.LEVEL2_WIDTH
            print(f"DEBUG: Carregando Nível 2 com background '{bg_prefix}'.")
        elif level_num == 3:
            bg_prefix = const.LVL3_BG_PREFIX
            bg_count = const.LVL3_BG_COUNT
            bg_start_index = const.LVL3_BG_START_INDEX
            level_width = const.LEVEL3_WIDTH
            print(f"DEBUG: Carregando Nível 3 com background '{bg_prefix}'.")
        else:
            print(f"DEBUG: Nível {level_num} desconhecido ou todos os níveis completos. Fim do jogo.")
            self.game_state = const.GAME_STATE_GAME_OVER_WIN
            return

        self.level = Level(self.tela, bg_prefix, bg_count, bg_start_index, level_width)
        self.current_level_number = level_num

    # REMOVIDO: def handle_events(self): pass
    # Este método não é mais necessário, pois os eventos são tratados em cada estado específico.


    def _get_translated_win_text(self):
        lang = self.menu.current_language
        return self.menu.translations[lang].get("win_message", const.WIN_TEXT_EN)

    def _get_translated_game_over_text(self):
        lang = self.menu.current_language
        return self.menu.translations[lang].get("game_over_message", const.GAME_OVER_TEXT_EN)


    def run(self):
        rodando = True
        while rodando:
            # REMOVIDO: self.handle_events()
            # Os eventos agora são coletados *apenas* dentro de Level.run() ou nos loops de menu/game over.

            # Lógica de transição de música baseada no estado do jogo
            if self.game_state != self.previous_game_state:
                if self.game_state == const.GAME_STATE_MENU and self.current_playing_music != 'menu':
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(self.menu_music_path)
                        pygame.mixer.music.play(-1)
                        print(f"DEBUG: Música do menu '{os.path.basename(self.menu_music_path)}' iniciada.")
                        self.current_playing_music = 'menu'
                    except pygame.error as e:
                        print(f"ERRO: Não foi possível carregar ou tocar a música do menu: {e}")

                elif self.game_state == const.GAME_STATE_PLAYING and self.current_playing_music != 'game':
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(self.game_music_path)
                        pygame.mixer.music.play(-1)
                        print(f"DEBUG: Música do jogo '{os.path.basename(self.game_music_path)}' iniciada.")
                        self.current_playing_music = 'game'
                    except pygame.error as e:
                        print(f"ERRO: Não foi possível carregar ou tocar a música do jogo: {e}")

                elif (self.game_state == const.GAME_STATE_GAME_OVER_WIN or
                      self.game_state == const.GAME_STATE_GAME_OVER_LOSE) and self.current_playing_music != 'none':
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    self.current_playing_music = 'none'

                elif self.game_state == const.GAME_STATE_QUIT and self.current_playing_music is not None:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    self.current_playing_music = None

                self.previous_game_state = self.game_state

            # Lógica principal baseada no estado do jogo
            if self.game_state == const.GAME_STATE_MENU:
                action_from_menu = self.menu.run()
                if action_from_menu == "start_game":
                    self.game_state = const.GAME_STATE_PLAYING
                    self._load_level(1)
                elif action_from_menu == "quit":
                    self.game_state = const.GAME_STATE_QUIT

            elif self.game_state == const.GAME_STATE_PLAYING:
                if self.level:
                    action_from_level = self.level.run(self.relogio)

                    if action_from_level == "quit":
                        self.game_state = const.GAME_STATE_QUIT
                    elif action_from_level == "level_complete":
                        print(f"DEBUG: Nível {self.current_level_number} completo. Tentando carregar próximo nível...")
                        self.current_level_number += 1
                        if self.current_level_number <= const.MAX_GAME_LEVELS:
                            self._load_level(self.current_level_number)
                        else:
                            print("DEBUG: Todos os níveis completos! Fim do jogo.")
                            self.game_state = const.GAME_STATE_GAME_OVER_WIN
                    elif action_from_level == const.GAME_STATE_GAME_OVER_LOSE:
                        self.game_state = const.GAME_STATE_GAME_OVER_LOSE
                else:
                    print("Erro: Nível não inicializado no estado PLAYING. Voltando ao menu.")
                    self.game_state = const.GAME_STATE_MENU

            elif self.game_state == const.GAME_STATE_GAME_OVER_WIN:
                for event in pygame.event.get(): # Eventos coletados aqui, localmente para esta tela
                    if event.type == pygame.QUIT:
                        self.game_state = const.GAME_STATE_QUIT
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            self.game_state = const.GAME_STATE_MENU

                if self.win_background_image:
                    self.tela.blit(self.win_background_image, (0, 0))
                else:
                    self.tela.fill(const.BLACK_COLOR)

                win_text = self._get_translated_win_text()
                win_surface = self.menu.font.render(win_text, True, const.WHITE_COLOR)
                win_rect = win_surface.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2))
                self.tela.blit(win_surface, win_rect)

                pygame.display.flip()
                self.relogio.tick(const.FPS) # Mantenha o relógio ativo para esta tela

            elif self.game_state == const.GAME_STATE_GAME_OVER_LOSE:
                for event in pygame.event.get(): # Eventos coletados aqui, localmente para esta tela
                    if event.type == pygame.QUIT:
                        self.game_state = const.GAME_STATE_QUIT
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            self.game_state = const.GAME_STATE_MENU # Volta para o menu principal

                if self.lose_background_image:
                    self.tela.blit(self.lose_background_image, (0, 0))
                else:
                    self.tela.fill(const.BLACK_COLOR)
                    print("AVISO: Imagem de derrota não carregada. Usando tela preta.")

                game_over_text = self._get_translated_game_over_text()
                game_over_surface = self.menu.font.render(game_over_text, True, const.WHITE_COLOR)
                game_over_rect = game_over_surface.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2))
                self.tela.blit(game_over_surface, game_over_rect)

                pygame.display.flip()
                self.relogio.tick(const.FPS) # Mantenha o relógio ativo para esta tela

            elif self.game_state == const.GAME_STATE_QUIT:
                rodando = False

        pygame.quit()