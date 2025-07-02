# code/menu.py
import pygame
import os
from . import const  # NOVO: Importa o módulo de constantes


class Menu:
    def __init__(self, screen, font_path=None, font_size=None):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # Cores: Agora importadas de const.py, removendo definições locais
        # self.PURPLE = (128, 0, 128)
        # self.HIGHLIGHT_COLOR = (255, 255, 0)
        # self.BLACK = (0, 0, 0)

        # Configuração da fonte - Usando const.MENU_FONT_SIZE
        if font_size is None:  # Garante que se font_size não for passado, ele use a constante
            font_size = const.MENU_FONT_SIZE

        if font_path and os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, font_size)
        else:
            print(f"Aviso: Fonte '{font_path}' não encontrada. Usando fonte padrão do Pygame.")
            self.font = pygame.font.Font(None, font_size)

        # --- Sistema de Tradução ---
        self.translations = {
            "en": {
                "title": const.GAME_TITLE,  # Usando a constante GAME_TITLE
                "start_game": "Start Game",
                "language_en": "English (EN)",
                "language_pt": "Portuguese (BR)",
                "quit_game": "Quit"
            },
            "pt": {
                "title": "A Bruxa e a Santa Ordem",
                "start_game": "Iniciar Jogo",
                "language_en": "Inglês (EN)",
                "language_pt": "Português (BR)",
                "quit_game": "Sair"
            }
        }
        self.current_language = "pt"

        # Opções selecionáveis do menu (as chaves usadas no dicionário de traduções)
        self.selectable_options = [
            "start_game",
            "language_en",
            "language_pt",
            "quit_game"
        ]

        # Variáveis de Interatividade (Foco/Hover)
        self.selected_index = 0
        self.hovered_index = -1
        self.option_rects = []

        # Carregando Imagem de Fundo e Música
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.menu_bg_path = os.path.join(base_dir, '..', 'asset', 'menubg.png')
        try:
            self.menu_bg_image = pygame.image.load(self.menu_bg_path).convert()
            self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo do menu: {e}")
            self.menu_bg_image = None

        self.menusong_path = os.path.join(base_dir, '..', 'asset', 'songs', 'menusong.mp3')

    def _get_translated_text(self, key):
        return self.translations[self.current_language].get(key, key)

    def _handle_option_selection(self, index):
        if 0 <= index < len(self.selectable_options):
            selected_key = self.selectable_options[index]

            if selected_key == "start_game":
                pygame.mixer.music.fadeout(1000)
                return "start_game"
            elif selected_key == "quit_game":
                pygame.mixer.music.fadeout(1000)
                return "quit"
            elif selected_key == "language_en":
                self.current_language = "en"
            elif selected_key == "language_pt":
                self.current_language = "pt"
        return None

    def draw(self):
        if self.menu_bg_image:
            self.screen.blit(self.menu_bg_image, (0, 0))
        else:
            self.screen.fill(const.BLACK_COLOR)  # Usando const.BLACK_COLOR

        # Renderiza e posiciona o título do jogo
        title_surface = self.font.render(self._get_translated_text("title"), True,
                                         const.PURPLE_COLOR)  # Usando const.PURPLE_COLOR
        title_rect = title_surface.get_rect(center=(self.width / 2, self.height * 0.4))
        self.screen.blit(title_surface, title_rect)

        self.option_rects.clear()

        y_start_pos = self.height * 0.65
        option_spacing = 60

        for i, option_key in enumerate(self.selectable_options):
            text = self._get_translated_text(option_key)

            if i == self.selected_index or i == self.hovered_index:
                text_color = const.HIGHLIGHT_COLOR  # Usando const.HIGHLIGHT_COLOR
            else:
                text_color = const.PURPLE_COLOR  # Usando const.PURPLE_COLOR

            option_surface = self.font.render(text, True, text_color)
            option_rect = option_surface.get_rect(center=(self.width / 2, y_start_pos + i * option_spacing))

            self.screen.blit(option_surface, option_rect)
            self.option_rects.append(option_rect)

        pygame.display.flip()

    def run(self):
        try:
            pygame.mixer.music.load(self.menusong_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar ou reproduzir a música do menu: {e}")

        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.fadeout(1000)
                    return "quit"

                if event.type == pygame.MOUSEMOTION:
                    self.hovered_index = -1
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            self.hovered_index = i
                            self.selected_index = i
                            break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.hovered_index != -1:
                        action = self._handle_option_selection(self.hovered_index)
                        if action:
                            return action

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.selectable_options)
                        self.hovered_index = -1
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.selectable_options)
                        self.hovered_index = -1
                    elif event.key == pygame.K_RETURN:
                        action = self._handle_option_selection(self.selected_index)
                        if action:
                            return action
                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(1000)
                        return "quit"

            self.draw()

        pygame.mixer.music.stop()
        return "quit"