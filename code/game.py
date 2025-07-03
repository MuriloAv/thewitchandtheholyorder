# code/game.py

import pygame
from .menu import Menu
import os
from .level import Level
from . import const  # Importa o módulo de constantes


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Inicializa o mixer de áudio

        self.tela = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption(const.GAME_TITLE)

        self.relogio = pygame.time.Clock()

        # --- Gerenciamento de Estados do Jogo ---
        self.game_state = const.GAME_STATE_MENU
        self.previous_game_state = None
        # NOVO: Variável para rastrear qual música está tocando atualmente
        self.current_playing_music = None  # Pode ser 'menu', 'game', ou None

        # --- Gerenciamento de Níveis ---
        self.current_level_number = 0  # 0 significa nenhum nível ativo (ou no menu)

        # Caminhos para os assets de música
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.game_music_path = os.path.join(base_dir, '..', 'asset', 'gamesong.mp3')
        self.menu_music_path = os.path.join(base_dir, '..', 'asset', 'menusong.mp3')

        # Caminho para a fonte
        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', f'{const.FONT_NAME}.ttf')

        # Menu é sempre inicializado
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)

        self.level = None  # O nível será carregado por _load_level

        self.pontuacao = 0

    def _load_level(self, level_num: int):
        """
        Carrega e inicializa um nível específico do jogo (APENAS OS ASSETS VISUAIS E LÓGICA DO NÍVEL).
        A lógica de carregamento e reprodução da música foi movida para o método run().
        """
        # REMOVIDO: pygame.mixer.music.stop()
        # REMOVIDO: pygame.mixer.music.load()
        # REMOVIDO: pygame.mixer.music.play()

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
        elif level_num == 3:  # Nível 3
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
        self.current_level_number = level_num  # Atualiza o número do nível atual

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.game_state = const.GAME_STATE_QUIT

    def run(self):
        rodando = True
        while rodando:
            self.handle_events()

            # --- Gerenciamento de Música baseado na Transição de Estado ---
            if self.game_state != self.previous_game_state:
                # Interrompe a música atual se houver uma mudança de estado que requeira uma nova música.
                # Não paramos a música do jogo quando passamos de level para level, pois ela deve continuar.
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

                elif self.game_state == const.GAME_STATE_QUIT and self.current_playing_music is not None:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    self.current_playing_music = None

                # Atualiza o estado anterior
                self.previous_game_state = self.game_state

            # --- Lógica do loop de jogo baseada no estado atual ---
            if self.game_state == const.GAME_STATE_MENU:
                action_from_menu = self.menu.run()
                if action_from_menu == "start_game":
                    self.game_state = const.GAME_STATE_PLAYING
                    # Começa o jogo carregando o Nível 1.
                    # A música do jogo será iniciada na próxima iteração do loop 'run'
                    # quando self.game_state for PLAYING e self.previous_game_state for MENU.
                    self._load_level(1)
                elif action_from_menu == "quit":
                    self.game_state = const.GAME_STATE_QUIT

            elif self.game_state == const.GAME_STATE_PLAYING:
                if self.level:
                    action_from_level = self.level.run(self.relogio)
                    if action_from_level == "quit":
                        self.game_state = const.GAME_STATE_QUIT
                    elif action_from_level == "level_complete":  # Nível atual foi completo
                        print(f"DEBUG: Nível {self.current_level_number} completo. Tentando carregar próximo nível...")
                        self.current_level_number += 1
                        if self.current_level_number <= const.MAX_GAME_LEVELS:
                            self._load_level(
                                self.current_level_number)  # Carrega o próximo nível (apenas visual e lógica)
                            # A música do jogo continua tocando, pois self.game_state permanece PLAYING
                            # e self.current_playing_music já é 'game'.
                        else:
                            print("DEBUG: Todos os níveis completos! Fim do jogo.")
                            self.game_state = const.GAME_STATE_GAME_OVER_WIN

                else:
                    print("Erro: Nível não inicializado no estado PLAYING. Voltando ao menu.")
                    self.game_state = const.GAME_STATE_MENU

            elif self.game_state == const.GAME_STATE_GAME_OVER_WIN:
                self.tela.fill(const.BLACK_COLOR)
                font = pygame.font.Font(None, 74)
                text = font.render("Você Venceu!", True, const.WHITE_COLOR)
                text_rect = text.get_rect(center=(self.tela.get_width() // 2, self.tela.get_height() // 2))
                self.tela.blit(text, text_rect)
                pygame.display.flip()

                pygame.time.wait(3000)
                self.game_state = const.GAME_STATE_QUIT

            elif self.game_state == const.GAME_STATE_QUIT:
                rodando = False

        pygame.quit()