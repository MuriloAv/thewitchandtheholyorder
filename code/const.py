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
PURPLE_COLOR = (128, 0, 128)  # ADICIONADO: Cor roxa para o título e itens não selecionados
HIGHLIGHT_COLOR = YELLOW_COLOR # ADICIONADO: Cor de destaque, usando o YELLOW_COLOR existente

# --- Constantes de Nível (Exemplo - Ajuste conforme o design do seu nível) ---
LEVEL_WIDTH = 4000  # A largura total do seu nível virtual
LEVEL_HEIGHT = 600 # A altura total do seu nível virtual (geralmente igual à altura da tela)

# --- Constantes de Assets de Fundo de Nível (Parallax) ---
LEVEL_BACKGROUND_FOLDER = 'lvl1bg' # Pasta onde estão as imagens de fundo
LEVEL_BACKGROUND_DEFAULT_LAYER = 'lvl1bg1.png' # Exemplo de uma camada padrão

# --- Constantes do Jogador ---
PLAYER_SPEED = 5
PLAYER_WIDTH = 50  # Largura do sprite do jogador
PLAYER_HEIGHT = 50 # Altura do sprite do jogador
PLAYER_ASSET_FOLDER = 'playerwalk' # <--- ALTERE AQUI: O nome da pasta agora é 'playerwalk'
PLAYER_SPRITE_FILENAME = 'playerwalk1.png' # <--- ALTERE AQUI: O nome do arquivo é 'playerwalk1.png' (assumindo que a

# --- Constantes do Menu ---
MENU_FONT_SIZE = 64
MENU_ITEM_COLOR = WHITE_COLOR
MENU_SELECTED_ITEM_COLOR = YELLOW_COLOR

# --- Outras Constantes ---
FONT_NAME = "OldLondon" # Nome da fonte (sem a extensão)