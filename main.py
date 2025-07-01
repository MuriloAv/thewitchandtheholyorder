# Importa a biblioteca Pygame, que nos permite criar jogos e aplicações gráficas
import pygame

# Inicializa todos os módulos do Pygame.
# É o primeiro passo e é essencial para que o Pygame funcione corretamente.
pygame.init()

# Define as dimensões da janela do jogo (largura em pixels, altura em pixels)
LARGURA_JANELA = 800
ALTURA_JANELA = 600

# Cria o objeto de tela (ou "superfície de exibição").
# Esta é a janela principal
TELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))

# Define o título que aparecerá na barra superior da janela do seu jogo.
pygame.display.set_caption("The Witch and the Holy Order")

BRANCO = (255, 255, 255)  # Branco puro
PRETO = (0, 0, 0)  # Preto puro
AZUL_CLARO = (173, 216, 230)  # Um tom de azul

# O relógio é usado para controlar a taxa de quadros por segundo (FPS).
# Isso garante que o jogo rode em uma velocidade consistente em diferentes computadores.
RELOGIO = pygame.time.Clock()
FPS = 60
# O jogo tentará rodar a 60 quadros por segundo

#Loop Principal do Jogo
# Tudo o que acontece no jogo (atualizar lógica, desenhar, processar eventos)
# ocorre repetidamente dentro deste loop.
rodando = True
# Variável de controle: enquanto for True, o loop continua.

while rodando:
    # Percorre todos os eventos que aconteceram desde o último quadro.
    # Eventos podem ser: clicar no mouse, pressionar uma tecla, fechar a janela, etc.
    for evento in pygame.event.get():
        # Se o evento for o usuário clicando no botão 'X' para fechar a janela...
        if evento.type == pygame.QUIT:
            rodando = False  # então definimos 'rodando' como False para sair do loop.

    # Por enquanto, não há lógica de jogo ativa, apenas a janela.
    # 4.3. Desenho na Tela

    # Primeiro, preenchemos o fundo da tela com uma cor.
    # Isso é importante para "apagar" o que foi desenhado no quadro anterior
    # evitando rastros e animações estranhas.
    TELA.fill(AZUL_CLARO)

    # Esta função "vira" o buffer de desenho, mostrando tudo o que foi desenhado
    # no TELA para o usuário. É o que faz o conteúdo aparecer na janela.
    pygame.display.flip()

    # Garante que o jogo não rode mais rápido do que o FPS definido (60 quadros/segundo).
    # Isso pausa o loop brevemente se ele estiver rodando muito rápido.
    RELOGIO.tick(FPS)

# Quando o loop principal termina (porque 'rodando' se tornou False),
# esta linha desinicializa todos os módulos do Pygame, liberando os recursos do sistema.
pygame.quit()
print("Janela do jogo fechada.")
