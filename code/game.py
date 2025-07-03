# code/game.py

import pygame
from .menu import Menu
import os
from .level import Level # O Level possui a instância do Player
from . import const


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.tela = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption(const.GAME_TITLE)

        self.relogio = pygame.time.Clock()

        # --- Gerenciamento de Estados do Jogo ---
        self.game_state = const.GAME_STATE_MENU
        self.previous_game_state = None
        self.current_playing_music = None

        # --- Gerenciamento de Níveis ---
        self.current_level_number = 0

        # Caminhos para os assets de música
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.game_music_path = os.path.join(base_dir, '..', 'asset', 'gamesong.mp3')
        self.menu_music_path = os.path.join(base_dir, '..', 'asset', 'menusong.mp3')

        # Caminho para a fonte
        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', f'{const.FONT_NAME}.ttf')

        # Menu é sempre inicializado
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)

        self.level = None # O nível será carregado por _load_level

        self.pontuacao = 0

        # --- Carrega a imagem de vitória ---
        win_image_full_path = os.path.join(base_dir, '..', const.GAME_OVER_WIN_IMAGE)
        try:
            self.win_background_image = pygame.image.load(win_image_full_path).convert_alpha()
            self.win_background_image = pygame.transform.scale(self.win_background_image,
                                                               (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de vitória '{win_image_full_path}': {e}")
            self.win_background_image = None

    def _load_level(self, level_num: int):
        """
        Carrega e inicializa um nível específico do jogo (APENAS OS ASSETS VISUAIS E LÓGICA DO NÍVEL).
        A lógica de carregamento e reprodução da música foi movida para o método run().
        """
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

        # A instância do Player é criada dentro do construtor de Level
        self.level = Level(self.tela, bg_prefix, bg_count, bg_start_index, level_width)
        self.current_level_number = level_num

    def handle_events(self):
        # Este método no Game é para eventos que afetam o estado GERAL do jogo (ex: QUIT)
        # Eventos específicos do Player (como pulo) serão tratados dentro do Level.run()
        # Não iteramos pygame.event.get() aqui para não consumir eventos antes do Level.run()
        pass # Mantido como pass para evitar consumo duplicado de eventos


    def _get_translated_win_text(self):
        lang = self.menu.current_language
        return self.menu.translations[lang].get("win_message", const.WIN_TEXT_EN)

    def run(self):
        rodando = True
        while rodando:
            # handle_events() é chamado aqui, mas ele não itera os eventos para o player.
            # Os eventos são iterados e passados para o player dentro de Level.run().
            self.handle_events() # Para eventos de QUIT do Pygame que podem vir a qualquer momento

            # --- Gerenciamento de Música baseado na Transição de Estado ---
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

                elif self.game_state == const.GAME_STATE_GAME_OVER_WIN and self.current_playing_music != 'none':
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    self.current_playing_music = 'none'

                elif self.game_state == const.GAME_STATE_QUIT and self.current_playing_music is not None:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    self.current_playing_music = None

                self.previous_game_state = self.game_state

            # --- Lógica do loop de jogo baseada no estado atual ---
            if self.game_state == const.GAME_STATE_MENU:
                action_from_menu = self.menu.run()
                if action_from_menu == "start_game":
                    self.game_state = const.GAME_STATE_PLAYING
                    self._load_level(1)
                elif action_from_menu == "quit":
                    self.game_state = const.GAME_STATE_QUIT

            elif self.game_state == const.GAME_STATE_PLAYING:
                if self.level:
                    # Level.run() agora é responsável por:
                    # 1. Obter os eventos do Pygame (pygame.event.get())
                    # 2. Passar esses eventos para self.player.handle_event()
                    # 3. Chamar self.player.update(delta_time)
                    # 4. Chamar self.player.draw()
                    # 5. Atualizar a câmera e desenhar o background
                    action_from_level = self.level.run(self.relogio) # <-- Aqui o Level controla o Player

                    if action_from_level == "quit":
                        self.game_state = const.GAME_STATE_QUIT
                    elif action_from_level == "level_complete":
                        print(f"DEBUG: Nível {self.current_level_number} completo. Tentando carregar próximo nível...")
                        self.current_level_number += 1
                        if self.current_level_number <= const.MAX_GAME_LEVELS:
                            self._load_level(self.current_level_number)
                            # NOVO: Ao carregar um novo nível, o player é recriado dentro do Level.
                            # Se você precisar resetar a posição do player (x e y) ao trocar de nível,
                            # essa lógica deve ser adicionada no construtor de Level, ou o Level deve
                            # ter um método para "resetar" o player.
                            # Por enquanto, como o Player é recriado em Level, ele já deve estar na START_X/Y.
                        else:
                            print("DEBUG: Todos os níveis completos! Fim do jogo.")
                            self.game_state = const.GAME_STATE_GAME_OVER_WIN

                else:
                    print("Erro: Nível não inicializado no estado PLAYING. Voltando ao menu.")
                    self.game_state = const.GAME_STATE_MENU

            elif self.game_state == const.GAME_STATE_GAME_OVER_WIN:
                for event in pygame.event.get():
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

            elif self.game_state == const.GAME_STATE_QUIT:
                rodando = False

        pygame.quit()