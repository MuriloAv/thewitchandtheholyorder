# code/const.py

import pygame # Manter por enquanto, embora não seja estritamente necessário neste arquivo

# --- Constantes do Jogo ---
GAME_TITLE = "The Witch and The Holy Order"
FPS = 60

# --- Cores ---
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
BLUE_SKY_COLOR = (135, 206, 235)
GREEN_COLOR = (0, 255, 0)
YELLOW_COLOR = (255, 255, 0)
PURPLE_COLOR = (128, 0, 128)
HIGHLIGHT_COLOR = YELLOW_COLOR

# --- Constantes de Nível ---
LEVEL_WIDTH = 4000
LEVEL_HEIGHT = 600

# --- Constantes de Assets de Fundo de Nível (Parallax) ---
# LEVEL_BACKGROUND_FOLDER = 'lvl1bg' # Esta deve estar removida ou comentada
LEVEL_BACKGROUND_DEFAULT_LAYER = 'lvl1bg1.png'

# --- Constantes do Jogador ---
PLAYER_SPEED = 5
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 75
# PLAYER_ASSET_FOLDER = 'playerwalk' # Esta deve estar removida ou comentada
PLAYER_SPRITE_FILENAME = 'playerwalk0.png'

# --- Constantes do Menu ---
MENU_FONT_SIZE = 48 # Reduzido de 64 para 48, por exemplo
MENU_ITEM_COLOR = WHITE_COLOR
MENU_SELECTED_ITEM_COLOR = YELLOW_COLOR

# --- Outras Constantes ---
FONT_NAME = "OldLondon" # Nome da fonte (sem a extensão)