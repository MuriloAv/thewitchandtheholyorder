# code/menu.py
import pygame
import os
from . import const


class Menu:
    def __init__(self, screen, font_path=None, font_size=None):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        font_size = font_size or const.MENU_FONT_SIZE
        try:
            self.font = pygame.font.Font(font_path, font_size)
            self.info_font = pygame.font.Font(None, 32)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, font_size)
            self.info_font = pygame.font.Font(None, 32)

        self.current_menu_state = "main"
        self.menu_options = {
            "main": ["start_game", const.OPTIONS_TEXT_KEY, "quit_game"],
            "options": [const.LANGUAGE_TEXT_KEY, const.CONTROLS_TEXT_KEY, const.BACK_TEXT_KEY],
            "language": ["language_en", "language_pt", const.BACK_TEXT_KEY],
            "controls": [const.BACK_TEXT_KEY]
        }

        # --- MUDANÇA 1: Adiciona as traduções para as descrições dos controles ---
        self.translations = {
            "en": {
                "title": const.GAME_TITLE, "start_game": "Start Game", const.OPTIONS_TEXT_KEY: "Options",
                "quit_game": "Quit", "language_en": "English (EN)", "language_pt": "Portuguese (BR)",
                const.LANGUAGE_TEXT_KEY: "Language", const.CONTROLS_TEXT_KEY: "Controls",
                const.CONTROLS_MOVE_KEY: "Move:", const.CONTROLS_JUMP_KEY: "Jump:",
                const.CONTROLS_ATTACK_KEY: "Attack:", const.BACK_TEXT_KEY: "Back",
                const.CONTROLS_MOVE_VALUE_KEY: "Left and Right Arrows",
                const.CONTROLS_JUMP_VALUE_KEY: "Up Arrow",
                const.CONTROLS_ATTACK_VALUE_KEY: "Spacebar",
                "win_message": const.WIN_TEXT_EN, "game_over_message": const.GAME_OVER_TEXT_EN
            },
            "pt": {
                "title": "A Bruxa e a Santa Ordem", "start_game": "Iniciar Jogo", const.OPTIONS_TEXT_KEY: "Opções",
                "quit_game": "Sair", "language_en": "Inglês (EN)", "language_pt": "Português (BR)",
                const.LANGUAGE_TEXT_KEY: "Idioma", const.CONTROLS_TEXT_KEY: "Controles",
                const.CONTROLS_MOVE_KEY: "Mover:", const.CONTROLS_JUMP_KEY: "Pular:",
                const.CONTROLS_ATTACK_KEY: "Atacar:", const.BACK_TEXT_KEY: "Voltar",
                const.CONTROLS_MOVE_VALUE_KEY: "Setas Esquerda e Direita",
                const.CONTROLS_JUMP_VALUE_KEY: "Seta para Cima",
                const.CONTROLS_ATTACK_VALUE_KEY: "Barra de Espaço",
                "win_message": const.WIN_TEXT_PT, "game_over_message": const.GAME_OVER_TEXT_PT
            }
        }
        self.current_language = "pt"
        self.selected_index = 0
        self.option_rects = []

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            bg_path = os.path.join(base_dir, '..', 'asset', 'menubg.png')
            self.menu_bg_image = pygame.transform.scale(pygame.image.load(bg_path).convert(), (self.width, self.height))
        except pygame.error as e:
            self.menu_bg_image = None
            print(f"Erro ao carregar a imagem de fundo do menu: {e}")

    def _get_translated_text(self, key):
        return self.translations[self.current_language].get(key, key.replace("_", " ").title())

    def _handle_selection(self):
        options = self.menu_options[self.current_menu_state]
        selected_key = options[self.selected_index]

        if selected_key == "start_game": return "start_game"
        if selected_key == "quit_game": return "quit"

        if selected_key == const.OPTIONS_TEXT_KEY:
            self.current_menu_state = "options"
        elif selected_key == const.LANGUAGE_TEXT_KEY:
            self.current_menu_state = "language"
        elif selected_key == const.CONTROLS_TEXT_KEY:
            self.current_menu_state = "controls"
        elif selected_key == const.BACK_TEXT_KEY:
            if self.current_menu_state in ["language", "controls"]:
                self.current_menu_state = "options"
            elif self.current_menu_state == "options":
                self.current_menu_state = "main"

        elif selected_key == "language_en":
            self.current_language = "en"
        elif selected_key == "language_pt":
            self.current_language = "pt"

        self.selected_index = 0
        return None

    def _draw_static_info(self):
        if self.current_menu_state == 'controls':
            y_pos = self.height * 0.4

            controls_title_surf = self.font.render(self._get_translated_text(const.CONTROLS_TEXT_KEY), True,
                                                   const.WHITE_COLOR)
            self.screen.blit(controls_title_surf, controls_title_surf.get_rect(center=(self.width / 2, y_pos)))
            y_pos += 60

            # --- MUDANÇA 2: O dicionário agora usa chaves para os valores também ---
            controls = {
                const.CONTROLS_MOVE_KEY: const.CONTROLS_MOVE_VALUE_KEY,
                const.CONTROLS_JUMP_KEY: const.CONTROLS_JUMP_VALUE_KEY,
                const.CONTROLS_ATTACK_KEY: const.CONTROLS_ATTACK_VALUE_KEY
            }
            for label_key, value_key in controls.items():
                # --- MUDANÇA 3: Traduz tanto o rótulo quanto a descrição ---
                label = self._get_translated_text(label_key)
                value = self._get_translated_text(value_key)
                text = f"{label} {value}"

                control_surf = self.info_font.render(text, True, const.WHITE_COLOR)
                self.screen.blit(control_surf, control_surf.get_rect(center=(self.width / 2, y_pos)))
                y_pos += 45

    def draw(self):
        self.screen.blit(self.menu_bg_image, (0, 0)) if self.menu_bg_image else self.screen.fill(const.BLACK_COLOR)
        title_surface = self.font.render(self._get_translated_text("title"), True, const.PURPLE_COLOR)
        self.screen.blit(title_surface,
                         title_surface.get_rect(center=(self.width / 2, self.height * const.MENU_TITLE_Y_FACTOR)))

        self._draw_static_info()

        self.option_rects.clear()
        current_options = self.menu_options[self.current_menu_state]

        y_start_options = self.height * 0.45
        for i, option_key in enumerate(current_options):
            text = self._get_translated_text(option_key)
            color = const.HIGHLIGHT_COLOR if i == self.selected_index else const.WHITE_COLOR
            option_surface = self.font.render(text, True, color)

            if option_key == const.BACK_TEXT_KEY:
                y_pos = self.height - 70
            else:
                y_pos = y_start_options + i * 55

            option_rect = option_surface.get_rect(center=(self.width / 2, y_pos))
            if self.current_menu_state != 'controls' or option_key == const.BACK_TEXT_KEY:
                self.screen.blit(option_surface, option_rect)

            self.option_rects.append(option_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    current_options = self.menu_options[self.current_menu_state]
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(current_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(current_options)
                    elif event.key == pygame.K_RETURN:
                        action = self._handle_selection()
                        if action: return action
                    elif event.key == pygame.K_ESCAPE:
                        if self.current_menu_state != "main":
                            if self.current_menu_state in ["language", "controls"]:
                                self.current_menu_state = "options"
                            else:
                                self.current_menu_state = "main"
                            self.selected_index = 0
                        else:
                            return "quit"

                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos): self.selected_index = i; break

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.option_rects and self.selected_index < len(self.option_rects):
                        if self.option_rects[self.selected_index].collidepoint(event.pos):
                            action = self._handle_selection()
                            if action: return action

            self.draw()
            pygame.time.Clock().tick(const.FPS)