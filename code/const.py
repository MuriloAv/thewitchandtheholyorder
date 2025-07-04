# code/const.py

# --- Constantes da Tela ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GAME_TITLE = "The Witch and The Holy Order"
FPS = 60 # Frames por segundo

# --- Cores (RGB) ---
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
BLUE_SKY_COLOR = (135, 206, 235)
YELLOW_COLOR = (255, 255, 0)
PURPLE_COLOR = (128, 0, 128)
HIGHLIGHT_COLOR = (255, 165, 0)

# --- Constantes do Jogador ---
PLAYER_SPEED = 5
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_SPRITE_FILENAME = 'playerwalk0.png'
PLAYER_START_X = 100
PLAYER_START_Y = 340

# --- Constantes do Pulo ---
JUMP_STRENGTH = 600       # Velocidade inicial do pulo (pixels/segundo)
GRAVITY = 1500            # Aceleração da gravidade (pixels/segundo²)
PLAYER_GROUND_Y = PLAYER_START_Y # Posição Y onde o jogador "aterriza"
JUMP_ANIMATION_SPEED = 0.08 # Tempo em segundos para cada frame de pulo

# --- Constantes dos Inimigos ---
ENEMY_WIDTH = 80 # Largura padrão para todos os inimigos (ajuste se quiser tamanhos diferentes)
ENEMY_HEIGHT = 80 # Altura padrão para todos os inimigos

# Inimigo 1 (6 frames: enemy1walk1 a enemy1walk6)
ENEMY1_SPEED = 300 # Velocidade em pixels/segundo
ENEMY1_ANIMATION_SPEED = 0.1 # Tempo em segundos para cada frame
ENEMY1_HEALTH = 100 # Exemplo de vida

# Inimigo 2 (4 frames: enemy2walk1 a enemy2walk4)
ENEMY2_SPEED = 400
ENEMY2_ANIMATION_SPEED = 0.12
ENEMY2_HEALTH = 75

# Inimigo 3 (5 frames: enemy3walk1 a enemy3walk5)
ENEMY3_SPEED = 350
ENEMY3_ANIMATION_SPEED = 0.09
ENEMY3_HEALTH = 120

# Constantes para o Spawn dos Inimigos
ENEMY_SPAWN_INTERVAL_MIN = 1.0 # Tempo mínimo em segundos entre spawns
ENEMY_SPAWN_INTERVAL_MAX = 1.5 # Tempo máximo em segundos entre spawns
ENEMY_SPAWN_X_OFFSET = 50 # Distância fora da tela à direita para aparecer

# --- Constantes do Nível ---
LEVEL1_WIDTH = 3000
LEVEL2_WIDTH = 4000
LEVEL3_WIDTH = 5000
MAX_GAME_LEVELS = 3

LVL1_BG_PREFIX = 'lvl1bg'
LVL1_BG_COUNT = 6
LVL1_BG_START_INDEX = 1

LVL2_BG_PREFIX = 'lvl2bg'
LVL2_BG_COUNT = 7
LVL2_BG_START_INDEX = 0

LVL3_BG_PREFIX = 'lvl3bg'
LVL3_BG_COUNT = 5
LVL3_BG_START_INDEX = 1

# --- Constantes do Menu ---
MENU_FONT_SIZE = 40
MENU_ITEM_COLOR = WHITE_COLOR
MENU_SELECTED_ITEM_COLOR = YELLOW_COLOR
FONT_NAME = 'OldLondon'
MENU_TITLE_Y_FACTOR = 0.50

# --- Estados do Jogo (Usados em game.py) ---
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_QUIT = 2
GAME_STATE_GAME_OVER_WIN = 3

# --- Constantes da Tela de Fim de Jogo ---
GAME_OVER_WIN_IMAGE = 'asset/scorebg.png' # Caminho para a imagem de fundo de vitória
WIN_TEXT_PT = "Você venceu os tiranos"
WIN_TEXT_EN = "You defeated the tyrants"

# --- Estados do Jogo (Usados em game.py) ---
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_QUIT = 2
GAME_STATE_GAME_OVER_WIN = 3 # Garanta que este estado esteja definido e com o valor 3