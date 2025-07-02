# code/game.py
import pygame
from .menu import Menu
import os
from .level import Level  # Importa a classe Level
from . import const  # Importa o módulo de constantes

# --- Definição de Estados do Jogo (Constantes) ---
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_QUIT = 2


# GAME_STATE_INTRO = 3 # REMOVIDO: Não precisamos mais deste estado

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.largura_janela = 800
        self.altura_janela = 600
        self.tela = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        pygame.display.set_caption(const.GAME_TITLE)

        self.relogio = pygame.time.Clock()  # Relógio para controlar o FPS

        # --- NOVO: Define o estado inicial do jogo para o MENU ---
        self.game_state = GAME_STATE_MENU

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', 'OldLondon.ttf')

        print(f"DEBUG: Caminho da fonte gótica em Game: {self.gothic_font_path}")

        # Menu é sempre inicializado, pois é o ponto de entrada
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=const.MENU_FONT_SIZE)

        # IntroScene removida
        # self.intro_scene = None

        # --- NOVO: Level é inicializado como None, será criado apenas ao iniciar o jogo ---
        self.level = None

        self.pontuacao = 0

    def handle_events(self):
        # Este método agora é mais um placeholder.
        # Os eventos são processados principalmente dentro dos loops de run() de Menu e Level.
        # No entanto, a verificação de QUIT global ainda é útil.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.game_state = GAME_STATE_QUIT

    def update_game_logic(self):
        pass  # Por enquanto, a lógica principal está dentro do Level

    def draw_elements(self):
        pass  # Por enquanto, o desenho principal está dentro do Level ou Menu

    def run(self):
        rodando = True
        while rodando:
            # Captura eventos globais como fechar a janela.
            # Os loops de run() de Menu e Level também processam seus próprios eventos.
            self.handle_events()

            if self.game_state == GAME_STATE_MENU:
                # O menu.run() tem seu próprio loop e controla o FPS.
                action_from_menu = self.menu.run()
                if action_from_menu == "start_game":
                    self.game_state = GAME_STATE_PLAYING
                    # --- NOVO: Cria o Level SOMENTE QUANDO O JOGO COMEÇA ---
                    self.level = Level(self.tela)
                elif action_from_menu == "quit":
                    self.game_state = GAME_STATE_QUIT

            # REMOVIDO: Não há mais estado de IntroScene
            # elif self.game_state == GAME_STATE_INTRO:
            #     if self.intro_scene:
            #         action_from_intro = self.intro_scene.run()
            #         if action_from_intro == "playing":
            #             self.game_state = GAME_STATE_PLAYING
            #             self.level = Level(self.tela)
            #             self.pontuacao = 0
            #         elif action_from_intro == "quit":
            #             self.game_state = GAME_STATE_QUIT
            #     else:
            #         self.game_state = GAME_STATE_QUIT

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
                    self.game_state = GAME_STATE_MENU  # Ou GAME_STATE_QUIT

            elif self.game_state == GAME_STATE_QUIT:
                rodando = False

            # Observação: O clock.tick() está dentro dos métodos run() de Menu e Level.
            # Este loop principal do Game apenas gerencia as transições de estado.

        pygame.quit()