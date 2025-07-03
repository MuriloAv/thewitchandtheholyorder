# code/game.py

import pygame
from .menu import Menu
import os
from .level import Level  # Importa a classe Level
from . import const  # Importa o módulo de constantes

# --- Definição de Estados do Jogo (Constantes) ---
# IMPORTANTE: Para melhor organização, é recomendado mover estas constantes
# para 'code/const.py' se elas forem usadas em múltiplos arquivos.
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_QUIT = 2


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Inicializa o mixer de áudio

        # Define o tamanho da tela do jogo
        self.tela = pygame.display.set_mode((640, 480))  # Definido para 640x480
        pygame.display.set_caption(const.GAME_TITLE)

        self.relogio = pygame.time.Clock()  # Relógio para controlar o FPS

        # --- Gerenciamento de Estados do Jogo ---
        self.game_state = GAME_STATE_MENU  # Estado inicial do jogo é o MENU
        # previous_game_state é inicializado como None para garantir que a música do menu
        # comece na primeira iteração do loop 'run'.
        self.previous_game_state = None

        # Caminhos para os assets de música
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.game_music_path = os.path.join(base_dir, '..', 'asset', 'gamesong.mp3')
        self.menu_music_path = os.path.join(base_dir, '..', 'asset', 'menusong.mp3')  # Caminho para a música do menu

        # Caminho para a fonte gótica (para o menu)
        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', 'OldLondon.ttf')

        # Menu é sempre inicializado, pois é o ponto de entrada
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)

        # Level é inicializado como None, será criado apenas ao iniciar o jogo
        self.level = None

        self.pontuacao = 0

    def handle_events(self):
        """
        Processa eventos globais, como o fechamento da janela.
        Eventos mais específicos são tratados nos loops de Menu e Level.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.game_state = GAME_STATE_QUIT

    def update_game_logic(self):
        """Método placeholder para lógica de atualização global do jogo."""
        pass

    def draw_elements(self):
        """Método placeholder para desenho de elementos globais do jogo."""
        pass

    def run(self):
        """Loop principal de execução do jogo, gerenciando estados e transições."""
        rodando = True
        while rodando:
            # Captura eventos globais como fechar a janela
            self.handle_events()

            # --- Gerenciamento de Música baseado na Transição de Estado ---
            # Este bloco é executado APENAS quando o game_state muda.
            if self.game_state != self.previous_game_state:
                pygame.mixer.music.stop()  # Para qualquer música que esteja tocando

                if self.game_state == GAME_STATE_MENU:
                    try:
                        pygame.mixer.music.load(self.menu_music_path)
                        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop contínuo
                        print(f"DEBUG: Música do menu '{os.path.basename(self.menu_music_path)}' iniciada.")
                    except pygame.error as e:
                        print(f"ERRO: Não foi possível carregar ou tocar a música do menu: {e}")

                elif self.game_state == GAME_STATE_PLAYING:
                    try:
                        pygame.mixer.music.load(self.game_music_path)
                        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop contínuo
                        print(f"DEBUG: Música do jogo '{os.path.basename(self.game_music_path)}' iniciada.")
                    except pygame.error as e:
                        print(f"ERRO: Não foi possível carregar ou tocar a música do jogo: {e}")

                # Atualiza previous_game_state APÓS lidar com a transição de música,
                # para que o próximo ciclo possa detectar uma nova mudança.
                self.previous_game_state = self.game_state

            # --- Lógica do loop de jogo baseada no estado atual ---
            if self.game_state == GAME_STATE_MENU:
                # O menu.run() tem seu próprio loop e controla o FPS.
                action_from_menu = self.menu.run()
                if action_from_menu == "start_game":
                    self.game_state = GAME_STATE_PLAYING
                    # Cria a instância do Level SOMENTE QUANDO O JOGO COMEÇA
                    self.level = Level(self.tela)
                elif action_from_menu == "quit":
                    self.game_state = GAME_STATE_QUIT

            elif self.game_state == GAME_STATE_PLAYING:
                if self.level:  # Garante que o Level foi inicializado
                    # O level.run() tem seu próprio loop e controla o FPS.
                    action_from_level = self.level.run(self.relogio)
                    if action_from_level == "quit":  # Se Level retornar "quit", encerra o jogo
                        self.game_state = GAME_STATE_QUIT
                    # Futuramente, "game_over", "level_complete", etc.
                else:
                    # Se level não estiver inicializado (não deveria acontecer aqui após o start_game),
                    # volta para o menu ou sai.
                    print("Erro: Level não inicializado no estado PLAYING. Voltando ao menu.")
                    self.game_state = GAME_STATE_MENU

            elif self.game_state == GAME_STATE_QUIT:
                rodando = False

            # Observação: O clock.tick() está dentro dos métodos run() de Menu e Level.
            # Este loop principal do Game apenas gerencia as transições de estado e a música.

        pygame.quit()  # Finaliza o Pygame ao sair do loop principal