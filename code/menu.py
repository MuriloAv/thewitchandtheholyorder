# code/menu.py
import pygame
import os


class Menu:
    def __init__(self, screen, font_path=None, font_size=48):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # Cores para o menu
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.PURPLE = (128, 0, 128)  # Um tom de roxo

        # --- NOVIDADE: Carregar a fonte baseada no font_path recebido ---
        if font_path and os.path.exists(font_path):  # Verifica se o caminho foi fornecido E se o arquivo existe
            self.font = pygame.font.Font(font_path, font_size)
        else:
            print(f"Aviso: Fonte '{font_path}' não encontrada. Usando fonte padrão do Pygame.")
            self.font = pygame.font.Font(None, font_size)  # Usa a fonte padrão do Pygame como fallback

        self.title_text = "The Witch and The Holy Order"
        self.start_button_text = "Pressione ENTER para Jogar"
        self.quit_button_text = "Pressione ESC para Voltar"

        # --- Carregando a imagem de fundo do menu ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.menu_bg_path = os.path.join(base_dir, '..', 'asset', 'menubg.png')

        try:
            self.menu_bg_image = pygame.image.load(self.menu_bg_path).convert()
            self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo do menu: {e}")
            self.menu_bg_image = None

        self.menusong_path = os.path.join(base_dir, '..', 'asset', 'songs', 'menusong.mp3')

    def draw(self):
        if self.menu_bg_image:
            self.screen.blit(self.menu_bg_image, (0, 0))
        else:
            self.screen.fill(self.BLACK)

        # --- NOVIDADE: Todos os textos em roxo ---
        title_surface = self.font.render(self.title_text, True, self.PURPLE)
        title_rect = title_surface.get_rect(center=(self.width / 2, self.height * 0.4))
        self.screen.blit(title_surface, title_rect)

        start_surface = self.font.render(self.start_button_text, True, self.PURPLE)  # Cor alterada para PURPLE
        start_rect = start_surface.get_rect(center=(self.width / 2, self.height * 0.85))
        self.screen.blit(start_surface, start_rect)

        quit_surface = self.font.render(self.quit_button_text, True, self.PURPLE)  # Cor alterada para PURPLE
        quit_rect = quit_surface.get_rect(center=(self.width / 2, self.height * 0.85 + 60))
        self.screen.blit(quit_surface, quit_rect)

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.fadeout(1000)
                        return "start_game"
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(1000)
                        return "quit"

            self.draw()

        pygame.mixer.music.stop()
        return "quit"