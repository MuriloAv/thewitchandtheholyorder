# code/const.py

# ==============================================================================
# --- GERAL E TELA ---
# ==============================================================================
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GAME_TITLE = "The Witch and The Holy Order"
FPS = 60

# ==============================================================================
# --- CORES (RGB) ---
# ==============================================================================
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
BLUE_SKY_COLOR = (135, 206, 235)
YELLOW_COLOR = (255, 255, 0)
PURPLE_COLOR = (128, 0, 128)
HIGHLIGHT_COLOR = (255, 165, 0)

# ==============================================================================
# --- JOGADOR ---
# ==============================================================================
PLAYER_SPEED = 5
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_START_X = 100
PLAYER_START_Y = 420
PLAYER_LIVES_START = 10
PLAYER_INVINCIBILITY_DURATION = 1.5
PLAYER_SHOOT_COOLDOWN = 2.0  # Tempo em segundos entre os tiros (aumente para tiro mais lento)

# --- FÍSICA DO PULO ---
JUMP_STRENGTH = 600
GRAVITY = 1500
PLAYER_GROUND_Y = PLAYER_START_Y # Posição Y onde o jogador "pousa"
JUMP_ANIMATION_SPEED = 0.08

# ==============================================================================
# --- INIMIGOS ---
# ==============================================================================
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 80
ENEMY_START_Y = 340 # Inimigos surgem na mesma altura do jogador

# --- Atributos por tipo de inimigo ---
# Inimigo 1
ENEMY1_SPEED = 200
ENEMY1_ANIMATION_SPEED = 0.1
ENEMY1_HEALTH = 1
ENEMY1_SHOOT_COOLDOWN = 1.2 # Diminua para tiro mais rápido

# Inimigo 2
ENEMY2_SPEED = 250
ENEMY2_ANIMATION_SPEED = 0.12
ENEMY2_HEALTH = 1
ENEMY2_SHOOT_COOLDOWN = 1.0 # Diminua para tiro mais rápido

# Inimigo 3
ENEMY3_SPEED = 275
ENEMY3_ANIMATION_SPEED = 0.09
ENEMY3_HEALTH = 1
ENEMY3_SHOOT_COOLDOWN = 0.8 # Diminua para tiro mais rápido

# --- Lógica de Spawn ---
ENEMY_SPAWN_INTERVAL_MIN = 1.0
ENEMY_SPAWN_INTERVAL_MAX = 1.5
ENEMY_SPAWN_X_OFFSET = 50

# ==============================================================================
# --- NÍVEIS ---
# ==============================================================================
MAX_GAME_LEVELS = 3
LEVEL1_WIDTH = 3500
LEVEL2_WIDTH = 4500
LEVEL3_WIDTH = 5500

# Level 1 Background
LVL1_BG_PREFIX = 'lvl1bg'
LVL1_BG_COUNT = 6
LVL1_BG_START_INDEX = 1

# Level 2 Background
LVL2_BG_PREFIX = 'lvl2bg'
LVL2_BG_COUNT = 7
LVL2_BG_START_INDEX = 0

# Level 3 Background
LVL3_BG_PREFIX = 'lvl3bg'
LVL3_BG_COUNT = 5
LVL3_BG_START_INDEX = 1

# ==============================================================================
# --- UI, MENUS E TEXTOS ---
# ==============================================================================
# --- Fontes e Cores do Menu ---
FONT_NAME = 'OldLondon'
MENU_FONT_SIZE = 40
MENU_ITEM_COLOR = WHITE_COLOR
MENU_SELECTED_ITEM_COLOR = YELLOW_COLOR
MENU_TITLE_Y_FACTOR = 0.25

# --- Chaves de Texto (para tradução em menu.py) ---
OPTIONS_TEXT_KEY = "options"
BACK_TEXT_KEY = "back"
LANGUAGE_TEXT_KEY = "language"
CONTROLS_TEXT_KEY = "controls"
CONTROLS_MOVE_KEY = "controls_move"
CONTROLS_JUMP_KEY = "controls_jump"
CONTROLS_ATTACK_KEY = "controls_attack"

# --- Textos de Fim de Jogo ---
GAME_OVER_WIN_IMAGE = 'asset/scorebg.png'
GAME_OVER_LOSE_IMAGE = 'asset/dead.PNG'
WIN_TEXT_PT = "Você venceu os tiranos"
WIN_TEXT_EN = "You defeated the tyrants"
GAME_OVER_TEXT_PT = "VOCÊ MORREU"
GAME_OVER_TEXT_EN = "YOU DIED"

# ==============================================================================
# --- ESTADOS DO JOGO ---
# ==============================================================================
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER_WIN = "win"
GAME_STATE_GAME_OVER_LOSE = "lose"
GAME_STATE_QUIT = "quit"