# code/game.py
import pygame
from .menu import Menu
import os # Importa o módulo os para manipular caminhos de arquivo

# --- Definição de Estados do Jogo (Constantes) ---
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_QUIT = 2

class Game:
    def __init__(self):
        # 1. Configurações Iniciais do Pygame e da Janela
        pygame.init()
        pygame.mixer.init() # Inicializa o mixer para áudio

        self.largura_janela = 800
        self.altura_janela = 600
        self.tela = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        pygame.display.set_caption("The Witch and The Holy Order - Por Murilo")

        # 2. Definição de Cores
        self.PRETO = (0, 0, 0)
        self.AZUL_CLARO = (173, 216, 230)
        self.VERMELHO = (255, 0, 0)

        # 3. Configuração do Relógio do Jogo
        self.relogio = pygame.time.Clock()
        self.FPS = 60

        # --- Gerenciamento de Estado do Jogo ---
        # O jogo começa no estado de menu
        self.game_state = GAME_STATE_MENU

        # --- Caminho para a fonte gótica ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # IMPORTANTE: Confirme que 'OldLondon.ttf' está na pasta 'asset' e o nome está EXATO.
        self.gothic_font_path = os.path.join(base_dir, '..', 'asset', 'OldLondon.ttf')

        # Para depurar: Imprime o caminho que está sendo usado para a fonte
        print(f"DEBUG: Caminho da fonte gótica em Game: {self.gothic_font_path}")


        # --- Inicializa o Objeto Menu ---
        # Passa a superfície da tela e o caminho da fonte para o menu poder desenhar nela
        # Aumentei o tamanho da fonte para 55, para ver se ajuda na legibilidade com fontes góticas.
        self.menu = Menu(self.tela, font_path=self.gothic_font_path, font_size=55)

        # --- Elementos do Jogo (serão usados no estado PLAYING) ---
        # Exemplo de jogador: um quadrado vermelho
        self.player_rect = pygame.Rect(self.largura_janela // 2 - 25, self.altura_janela - 60, 50, 50)
        self.velocidade_jogador = 5
        self.pontuacao = 0

    def handle_events(self):
        """
        Processa os eventos do usuário (teclado, mouse, fechar janela).
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.game_state = GAME_STATE_QUIT  # Se o usuário fechar a janela, muda o estado para sair

        # --- Eventos específicos do estado PLAYING ---
        if self.game_state == GAME_STATE_PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_rect.left > 0:
                self.player_rect.x -= self.velocidade_jogador
            if keys[pygame.K_RIGHT] and self.player_rect.right < self.largura_janela:
                self.player_rect.x += self.velocidade_jogador
            # Adicione aqui outras interações do jogador (ex: pular, atirar)

    def update_game_logic(self):
        """
        Atualiza a lógica do jogo (movimento de inimigos, colisões, pontuação).
        Esta função só é chamada quando o jogo está no estado PLAYING.
        """
        if self.game_state == GAME_STATE_PLAYING:
            # Implemente aqui a lógica principal do seu jogo:
            # - Movimento de inimigos/objetos
            # - Verificação de colisões
            # - Atualização de pontuação, vidas
            # - Lógica de IA para inimigos
            pass  # Use 'pass' como placeholder, remova quando adicionar sua lógica real

    def draw_elements(self):
        """
        Desenha todos os elementos do jogo na tela.
        Esta função só é chamada quando o jogo está no estado PLAYING.
        """
        if self.game_state == GAME_STATE_PLAYING:
            self.tela.fill(self.AZUL_CLARO)  # Preenche o fundo do jogo

            # Desenha o jogador
            pygame.draw.rect(self.tela, self.VERMELHO, self.player_rect)

            # Desenha a pontuação na tela
            font_pontuacao = pygame.font.Font(None, 36)
            texto_pontuacao = font_pontuacao.render(f"Pontos: {self.pontuacao}", True, self.PRETO)
            self.tela.blit(texto_pontuacao, (10, 10))

        # Esta parte é importante: Atualiza a exibição APENAS UMA VEZ por frame
        pygame.display.flip()

    def run(self):
        """
        Loop principal do jogo.
        Gerencia os diferentes estados do jogo (menu, jogando, sair).
        """
        rodando = True
        while rodando:
            # --- Gerenciamento de Estados ---
            if self.game_state == GAME_STATE_MENU:
                # Chama o loop do menu. Ele "bloqueia" aqui até o usuário escolher algo.
                action_from_menu = self.menu.run()
                if action_from_menu == "start_game":
                    self.game_state = GAME_STATE_PLAYING
                    # Opcional: Reinicializar elementos do jogo aqui se estiver começando uma nova partida
                    self.player_rect.center = (self.largura_janela // 2, self.altura_janela - 30)
                    self.pontuacao = 0
                elif action_from_menu == "quit":
                    self.game_state = GAME_STATE_QUIT  # Usuário escolheu sair do menu

            elif self.game_state == GAME_STATE_PLAYING:
                # Se o jogo está no estado de jogo, processa eventos, atualiza a lógica e desenha
                self.handle_events()
                self.update_game_logic()
                self.draw_elements()

            elif self.game_state == GAME_STATE_QUIT:
                # Se o estado é para sair, encerra o loop principal
                rodando = False

            # --- Controle de FPS ---
            # Garante que o loop rode na taxa de quadros desejada.
            # É importante que o clock.tick() esteja sempre no loop principal do Game.
            if rodando:  # Garante que não tente "ticar" após decidir sair
                self.relogio.tick(self.FPS)

        # --- Finalização do Pygame ---
        pygame.quit()
