# code/menu.py
import pygame
import os
from . import const  # Importa o módulo de constantes


class Menu:
    def __init__(self, screen, font_path=None, font_size=None):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # Configuração da fonte - Usando const.MENU_FONT_SIZE
        if font_size is None:
            font_size = const.MENU_FONT_SIZE

        if font_path and os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, font_size)
        else:
            print(f"Aviso: Fonte '{font_path}' não encontrada. Usando fonte padrão do Pygame.")
            self.font = pygame.font.Font(None, font_size)

        # --- Sistema de Tradução ---
        self.translations = {
            "en": {
                "title": const.GAME_TITLE,
                "start_game": "Start Game",
                "language_en": "English (EN)",
                "language_pt": "Portuguese (BR)",
                "quit_game": "Quit",
                "win_message": const.WIN_TEXT_EN,
                "game_over_message": const.GAME_OVER_TEXT_EN # Adicionado: Mensagem de Game Over em inglês
            },
            "pt": {
                "title": "A Bruxa e a Santa Ordem",
                "start_game": "Iniciar Jogo",
                "language_en": "Inglês (EN)",
                "language_pt": "Português (BR)",
                "quit_game": "Sair",
                "win_message": const.WIN_TEXT_PT,
                "game_over_message": const.GAME_OVER_TEXT_PT # Adicionado: Mensagem de Game Over em português
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
        self.option_rects = []  # Será preenchido em draw()

        # Carregando Imagem de Fundo e Música
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.menu_bg_path = os.path.join(base_dir, '..', 'asset', 'menubg.png')
        try:
            self.menu_bg_image = pygame.image.load(self.menu_bg_path).convert()
            self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo do menu: {e}")
            self.menu_bg_image = None

        self.menusong_path = os.path.join(base_dir, '..', 'asset', 'menusong.mp3')

    def _get_translated_text(self, key):
        # Garante que a chave existe na linguagem atual, caso contrário, retorna a própria chave
        return self.translations[self.current_language].get(key, key)

    def _handle_option_selection(self, index):
        if 0 <= index < len(self.selectable_options):
            selected_key = self.selectable_options[index]

            if selected_key == "start_game":
                return "start_game"
            elif selected_key == "quit_game":
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
            self.screen.fill(const.BLACK_COLOR)

        # Renderiza e posiciona o título do jogo
        title_surface = self.font.render(self._get_translated_text("title"), True,
                                         const.PURPLE_COLOR)
        title_rect = title_surface.get_rect(
            center=(self.width / 2, const.SCREEN_HEIGHT * const.MENU_TITLE_Y_FACTOR))
        self.screen.blit(title_surface, title_rect)

        self.option_rects.clear()

        line_height = self.font.get_height() + 10
        total_options_height = len(self.selectable_options) * line_height

        y_start_options = title_rect.bottom + 30

        for i, option_key in enumerate(self.selectable_options):
            text = self._get_translated_text(option_key)

            if i == self.selected_index or i == self.hovered_index:
                text_color = const.HIGHLIGHT_COLOR
            else:
                text_color = const.PURPLE_COLOR

            option_surface = self.font.render(text, True, text_color)

            option_rect = option_surface.get_rect(center=(self.width / 2, y_start_options + i * line_height))

            self.screen.blit(option_surface, option_rect)
            self.option_rects.append(option_rect)

        pygame.display.flip()

    def run(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                        return "quit"

            self.draw()
            pygame.time.Clock().tick(const.FPS)

        return "quit"