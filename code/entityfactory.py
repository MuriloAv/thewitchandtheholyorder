# entityfactory.py

import pygame
import os  # Importar os para manipulação de caminhos
from typing import Type, Dict, Any, Optional, Tuple
from entity import Entity
from background import Background

# Futuramente, importaremos Player, Enemy, etc.
# from player import Player
# from enemy import Enemy

# A seção de MOCK para Pygame (simplificada)
# Reintroduzida aqui para garantir que EntityFactory possa ser testado de forma isolada.
try:
    import pygame
except ImportError:
    print("Pygame não encontrado em entityfactory.py. Usando objetos mock.")


    class MockRect:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.topleft = (x, y)

        def __repr__(self): return f"MockRect(x={self.x}, y={self.y}, w={self.width}, h={self.height})"

        def move(self, dx, dy): self.x += dx; self.y += dy; self.topleft = (self.x, self.y); return self

        def copy(self): return MockRect(self.x, self.y, self.width, self.height)


    class MockSurface:
        def __init__(self, size=(1, 1), flags=0, depth=0): self.width, self.height = size; self.rect = MockRect(0, 0,
                                                                                                                self.width,
                                                                                                                self.height)

        def get_rect(self): return self.rect

        def fill(self, color): pass

        def blit(self, source, dest): pass

        def set_colorkey(self, color): pass

        def convert_alpha(self): return self

        def convert(self): return self


    class MockImage:
        def load(self, filename): print(f"MOCK: Carregando imagem '{filename}'..."); return MockSurface(
            (50, 50))  # Tamanho padrão para entidades


    class MockPygame:
        def __init__(self): self.Rect = MockRect; self.Surface = MockSurface; self.image = MockImage()


    pygame = MockPygame()


# --- FIM DO MOCK ---


class EntityFactory:
    """
    Fábrica responsável pela criação de instâncias de diferentes tipos de entidades.
    Centraliza a lógica de carregamento de recursos e instanciação, tornando o sistema
    mais modular e fácil de estender com novos tipos de entidades.
    """

    # Um dicionário para mapear nomes de entidades para caminhos de imagem padrão
    # Em um jogo real, isso seria carregado de um arquivo de configuração (JSON/YAML)
    # ou definido de forma mais robusta.
    _ENTITY_RESOURCES: Dict[str, Dict[str, Any]] = {
        "Background": {
            "image_filename": "menubg.png",
            # Usando a imagem de fundo do menu como exemplo (ou qualquer outra imagem de background na raiz asset)
            "default_size": (800, 600),
            "default_color": (0, 0, 0, 255)  # Preto
        },
        "Player": {
            "image_filename": "playerwalk1.png",
            "default_size": (50, 50),
            "default_color": (0, 255, 0, 255)  # Verde
        },
        "Enemy": {
            "image_filename": "enemy1walk1.png",
            "default_size": (40, 40),
            "default_color": (255, 0, 0, 255)  # Vermelho
        }
        # Adicione mais tipos de entidades conforme o jogo se desenvolve
    }

    @staticmethod
    def _load_image(image_filename: str, default_size: Tuple[int, int] = (50, 50),
                    default_color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> pygame.Surface:
        """
        Carrega uma imagem do caminho especificado. Se a imagem não for encontrada,
        cria uma superfície colorida padrão como fallback.
        Considera que todos os assets estão na raiz da pasta 'asset'.

        Args:
            image_filename (str): O nome do arquivo de imagem (ex: 'playerwalk1.png').
            default_size (Tuple[int, int]): O tamanho da superfície fallback.
            default_color (Tuple[int, int, int, int]): A cor da superfície fallback (RGBA).

        Returns:
            pygame.Surface: A imagem carregada ou a superfície fallback.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual (code)
        image_path = os.path.join(base_dir, '..', 'asset', image_filename)  # Caminho completo para o asset

        try:
            # Em um jogo real, teríamos pygame.image.load(image_path).convert_alpha()
            # O mock de pygame.image.load já retorna um MockSurface.
            image = pygame.image.load(image_path).convert_alpha()
            print(f"Imagem '{image_filename}' carregada com sucesso.")
            return image
        except pygame.error:  # Captura erros de carregamento de imagem (se pygame real estivesse ativo)
            print(
                f"AVISO: Não foi possível carregar a imagem '{image_filename}' em '{image_path}'. Criando superfície padrão.")
            # Cria uma superfície padrão colorida como fallback
            fallback_image = pygame.Surface(default_size, pygame.SRCALPHA)
            fallback_image.fill(default_color)
            return fallback_image
        except Exception as e:  # Captura outros erros (especialmente com o mock)
            print(f"AVISO: Erro genérico ao carregar a imagem '{image_filename}': {e}. Criando superfície padrão.")
            fallback_image = pygame.Surface(default_size, pygame.SRCALPHA)
            fallback_image.fill(default_color)
            return fallback_image

    @staticmethod
    def create_entity(entity_type: str, *args, **kwargs) -> Entity:
        """
        Cria e retorna uma instância de Entity baseada no tipo especificado.

        Args:
            entity_type (str): Uma string que representa o tipo de entidade a ser criada
                               (ex: 'Player', 'Enemy', 'Background').
            *args: Argumentos posicionais a serem passados para o construtor da entidade.
            **kwargs: Argumentos nomeados a serem passados para o construtor da entidade.
                      Pode incluir 'image_filename' para carregar uma imagem específica.

        Returns:
            Entity: Uma nova instância da classe de entidade correspondente.

        Raises:
            ValueError: Se o tipo de entidade for desconhecido.
        """
        entity_type_lower = entity_type.lower()

        # Recupera as configurações de recurso para o tipo de entidade
        resource_info = EntityFactory._ENTITY_RESOURCES.get(entity_type)
        if not resource_info:
            raise ValueError(f"Tipo de entidade desconhecido: '{entity_type}'. Adicione-o a _ENTITY_RESOURCES.")

        # Carrega a imagem para a entidade
        # Permite sobrescrever o filename padrão se passado via kwargs
        image_filename = kwargs.pop('image_filename', resource_info.get('image_filename'))
        image = None
        if image_filename:
            image = EntityFactory._load_image(
                image_filename,
                resource_info.get('default_size'),
                resource_info.get('default_color')
            )

        # Passa a imagem carregada e outras kwargs para o construtor da entidade
        kwargs['image'] = image

        # Define um nome padrão se não for fornecido
        if 'name' not in kwargs and not args:  # Se name não foi passado como kwarg e nem como primeiro arg posicional
            kwargs['name'] = entity_type  # Nome padrão é o tipo da entidade

        # Lógica de criação baseada no tipo
        if entity_type == "Background":
            # Background pode precisar de argumentos específicos como scroll_speed
            return Background(*args, **kwargs)
        # elif entity_type == "Player":
        #     return Player(*args, **kwargs)
        # elif entity_type == "Enemy":
        #     return Enemy(*args, **kwargs)
        else:
            # Para outros tipos de entidades que ainda não têm uma classe concreta,
            # podemos retornar uma Entity base (se ela fosse concreta) ou levantar um erro.
            # Como Entity é abstrata, levantamos um erro por enquanto,
            # até que Player e Enemy sejam implementados.
            raise NotImplementedError(
                f"A criação para o tipo de entidade '{entity_type}' ainda não foi implementada "
                "na fábrica (classes Player/Enemy ainda não existem)."
            )


# Exemplo de uso (para teste local):
if __name__ == "__main__":
    print("Testando a classe EntityFactory.")

    # Criar um background usando a fábrica
    print("\n--- Criando Background ---")
    try:
        # A factory tentará carregar a imagem 'menubg.png' (definida em _ENTITY_RESOURCES)
        # O mock de pygame.image.load irá simular isso.
        bg = EntityFactory.create_entity("Background", x=0, y=0, scroll_speed_x=-2)
        print(
            f"Background criado: {bg.name}, Posição: {bg.rect.topleft}, Velocidade de Rolagem X: {bg._scroll_speed_x}")
        # Testar update e draw para o background
        mock_screen = pygame.Surface((800, 600))
        bg.update(0.1)
        bg.draw(mock_screen)
    except Exception as e:
        print(f"Erro ao criar Background: {e}")

    # Tentar criar um Player (que ainda não foi implementado concretamente)
    print("\n--- Tentando criar Player ---")
    try:
        player = EntityFactory.create_entity("Player", x=100, y=200)
        # Se Player estivesse implementado, poderíamos imprimir seus detalhes
        # print(f"Player criado: {player.name}, Posição: {player.rect.topleft}")
    except NotImplementedError as e:
        print(f"Erro esperado ao criar Player (não implementado): {e}")
    except ValueError as e:
        print(f"Erro inesperado: {e}")

    # Tentar criar um tipo de entidade desconhecido
    print("\n--- Tentando criar Entidade Desconhecida ---")
    try:
        unknown = EntityFactory.create_entity("Dragon", x=50, y=50)
    except ValueError as e:
        print(f"Erro esperado ao criar Entidade Desconhecida: {e}")

    # Criar um background com um nome customizado
    print("\n--- Criando Background com nome customizado ---")
    try:
        custom_bg = EntityFactory.create_entity("Background", name="MyCustomBackground", x=0, y=0)
        print(f"Background customizado criado: {custom_bg.name}")
    except Exception as e:
        print(f"Erro ao criar Background customizado: {e}")