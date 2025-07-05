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
PLAYER_START_X = 100
PLAYER_START_Y = 420
PLAYER_LIVES_START = 10
PLAYER_INVINCIBILITY_DURATION = 1.5
PLAYER_SHOOT_COOLDOWN = 2.0  # <-- ADICIONADO: Cadência de tiro do jogador (aumente para tiro mais lento)

# --- Constantes do Pulo ---
JUMP_STRENGTH = 600
GRAVITY = 1500
PLAYER_GROUND_Y = PLAYER_START_Y # Posição Y onde o jogador "aterriza"
JUMP_ANIMATION_SPEED = 0.08

# --- Constantes dos Inimigos ---
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 80
ENEMY_START_Y = 340 # <-- ADICIONADO: Altura inicial dos inimigos, independente do jogador

# Inimigo 1 (6 frames: enemy1walk1 a enemy1walk6)
ENEMY1_SPEED = 200
ENEMY1_ANIMATION_SPEED = 0.1
ENEMY1_HEALTH = 1
ENEMY1_SHOOT_COOLDOWN = 1.2 # <-- ADICIONADO: Cadência de tiro (diminua para tiro mais rápido)

# Inimigo 2 (4 frames: enemy2walk1 a enemy2walk4)
ENEMY2_SPEED = 250
ENEMY2_ANIMATION_SPEED = 0.12
ENEMY2_HEALTH = 1
ENEMY2_SHOOT_COOLDOWN = 1.0 # <-- ADICIONADO

# Inimigo 3 (5 frames: enemy3walk1 a enemy3walk5)
ENEMY3_SPEED = 275
ENEMY3_ANIMATION_SPEED = 0.09
ENEMY3_HEALTH = 1
ENEMY3_SHOOT_COOLDOWN = 0.8 # <-- ADICIONADO

# Constantes para o Spawn dos Inimigos
ENEMY_SPAWN_INTERVAL_MIN = 1.0
ENEMY_SPAWN_INTERVAL_MAX = 1.5
ENEMY_SPAWN_X_OFFSET = 50

# --- Constantes do Nível ---
LEVEL1_WIDTH = 3500
LEVEL2_WIDTH = 4500
LEVEL3_WIDTH = 5500
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
GAME_STATE_GAME_OVER_WIN = 2
GAME_STATE_GAME_OVER_LOSE = 3
GAME_STATE_QUIT = 4

# --- Constantes da Tela de Fim de Jogo ---
GAME_OVER_WIN_IMAGE = 'asset/scorebg.png'
GAME_OVER_LOSE_IMAGE = 'asset/dead.PNG'

WIN_TEXT_PT = "Você venceu os tiranos"
WIN_TEXT_EN = "You defeated the tyrants"

GAME_OVER_TEXT_EN = "YOU DIED"
GAME_OVER_TEXT_PT = "VOCÊ MORREU"