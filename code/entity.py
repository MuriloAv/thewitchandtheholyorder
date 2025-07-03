# entity.py

import abc
from abc import ABC, abstractmethod
from typing import Optional, Tuple

# --- MOCK para Pygame para desenvolvimento/testes sem a biblioteca instalada ---
try:
    import pygame
except ImportError:
    print("Pygame não encontrado. Usando objetos mock para desenvolvimento de classes.")


    class MockRect:
        """Um mock simplificado para pygame.Rect."""

        def __init__(self, x: int, y: int, width: int, height: int):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.topleft = (x, y)

        def __repr__(self):
            return f"MockRect(x={self.x}, y={self.y}, w={self.width}, h={self.height})"

        def move(self, dx: float, dy: float):
            self.x += dx
            self.y += dy
            self.topleft = (self.x, self.y)
            return self  # Permite encadeamento

        def copy(self):
            return MockRect(self.x, self.y, self.width, self.height)


    class MockSurface:
        """Um mock simplificado para pygame.Surface."""

        def __init__(self, size: Tuple[int, int] = (1, 1), flags: int = 0, depth: int = 0):
            self.width, self.height = size
            self.rect = MockRect(0, 0, self.width, self.height)

        def get_rect(self):
            return self.rect

        def fill(self, color: Tuple[int, int, int]):
            pass  # No actual drawing in mock

        def blit(self, source: 'MockSurface', dest: Tuple[int, int]):
            pass  # No actual drawing in mock

        def set_colorkey(self, color: Tuple[int, int, int]):
            pass

        def convert_alpha(self) -> 'MockSurface':
            return self  # Mock conversion

        def convert(self) -> 'MockSurface':
            return self  # Mock conversion


    class MockImage:
        """Um mock para pygame.image."""

        def load(self, filename: str) -> MockSurface:
            print(f"MOCK: Carregando imagem '{filename}'...")
            # Retorna uma Surface mock com um tamanho padrão para simular a imagem
            return MockSurface((50, 50))


    class MockPygame:
        """Um mock para o módulo pygame."""

        def __init__(self):
            self.Rect = MockRect
            self.Surface = MockSurface
            self.image = MockImage()
            # Outros mocks necessários podem ser adicionados aqui


    pygame = MockPygame()


# --- FIM DO MOCK ---


class Entity(ABC):
    """
    Classe base abstrata para todas as entidades do jogo.
    Define a interface comum para objetos que precisam ser atualizados e desenhados.

    Atributos:
        _name (str): Nome identificador da entidade (ex: 'Player', 'Enemy_1').
        _image (pygame.Surface): Superfície Pygame que representa a imagem visual da entidade.
        _rect (pygame.Rect): Objeto Pygame.Rect para gerenciar a posição e o tamanho da entidade,
                             usado para desenho e detecção de colisões.
    """

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 image: Optional[pygame.Surface] = None,
                 color: Optional[Tuple[int, int, int]] = None):
        """
        Inicializa uma nova entidade.

        Args:
            name (str): Nome da entidade.
            x (int): Posição inicial X da entidade.
            y (int): Posição inicial Y da entidade.
            width (Optional[int]): Largura da entidade. Obrigatório se 'image' não for fornecido.
            height (Optional[int]): Altura da entidade. Obrigatório se 'image' não for fornecido.
            image (Optional[pygame.Surface]): A superfície Pygame que representa a entidade.
                                              Se fornecido, 'width' e 'height' serão inferidos.
            color (Optional[Tuple[int, int, int]]): Cor para preencher a superfície se 'image' não for fornecido.
                                                     Padrão é branco se imagem não fornecida.
        Raises:
            ValueError: Se 'image' não for fornecido e 'width' ou 'height' estiverem ausentes.
        """
        self._name: str = name
        self._image: pygame.Surface
        self._rect: pygame.Rect

        if image:
            self._image = image
            self._rect = self._image.get_rect(topleft=(x, y))
        else:
            if width is None or height is None:
                raise ValueError("Se 'image' não for fornecido, 'width' e 'height' devem ser especificados.")

            # Cria uma superfície padrão se nenhuma imagem for fornecida
            self._image = pygame.Surface((width, height), pygame.SRCALPHA)  # SRCALPHA para transparência
            self._image.fill(color if color else (255, 255, 255, 255))  # Cor padrão: branco (com alpha)
            self._rect = self._image.get_rect(topleft=(x, y))

    @property
    def name(self) -> str:
        """Retorna o nome da entidade."""
        return self._name

    @property
    def image(self) -> pygame.Surface:
        """Retorna a superfície Pygame da entidade."""
        return self._image

    @image.setter
    def image(self, new_image: pygame.Surface):
        """Define uma nova superfície Pygame para a entidade e atualiza seu rect."""
        self._image = new_image
        # Atualiza o rect para corresponder às novas dimensões da imagem, mantendo a posição
        self._rect = self._image.get_rect(topleft=self._rect.topleft)

    @property
    def rect(self) -> pygame.Rect:
        """Retorna o objeto Pygame.Rect da entidade."""
        return self._rect

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Método abstrato para atualizar o estado da entidade (ex: posição, animação, lógica).

        Args:
            delta_time (float): Tempo decorrido desde o último frame em segundos.
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Método abstrato para desenhar a entidade na tela.

        Args:
            screen (pygame.Surface): A superfície Pygame onde a entidade será desenhada.
        """
        pass

    @abstractmethod
    def move(self) -> None:
        """
        Método abstrato para lidar com a lógica de movimento da entidade.
        Esta é uma especialização do `update` focada na movimentação, conforme o diagrama.
        Pode ser chamado internamente por `update` ou diretamente dependendo da implementação.
        """
        pass


# Exemplo de uso (para teste local):
if __name__ == "__main__":
    print("Testando a classe Entity (abstrata, não pode ser instanciada diretamente).")
    print("No entanto, podemos verificar suas propriedades e métodos abstratos.")


    # Para testar, precisaremos de uma subclasse concreta.
    class ConcreteEntity(Entity):
        def __init__(self, name: str, x: int, y: int, width: int, height: int):
            super().__init__(name, x, y, width, height, color=(255, 0, 0, 255))  # Entidade vermelha

        def update(self, delta_time: float) -> None:
            print(f"{self.name}: Atualizando... (delta_time: {delta_time:.2f})")
            self.move()  # Chama o método move durante a atualização

        def draw(self, screen: pygame.Surface) -> None:
            print(f"{self.name}: Desenhando em {self.rect.topleft} (na tela mock).")
            # screen.blit(self.image, self.rect) # No mock, blit não faz nada visual

        def move(self) -> None:
            # Exemplo de movimento simples
            self._rect.x += 1  # Move para a direita
            print(f"{self.name}: Movendo-se para x={self.rect.x}")


    try:
        # Tentar instanciar Entity diretamente deve falhar
        # entity = Entity("Test Entity", 10, 20, 30, 40)
        pass  # Comentado para evitar erro em tempo de execução para este exemplo

    except TypeError as e:
        print(f"Erro esperado ao instanciar Entity: {e}")

    # Instanciar uma subclasse concreta
    entity1 = ConcreteEntity("My_Concrete_Entity", 100, 100, 50, 50)
    print(f"Nome: {entity1.name}")
    print(f"Rect inicial: {entity1.rect}")
    print(f"Image: {entity1.image}")

    # Simular game loop
    mock_screen = pygame.Surface((800, 600))
    for i in range(3):
        print(f"\n--- Ciclo {i + 1} ---")
        entity1.update(0.16)  # Simula 16ms de delta_time
        entity1.draw(mock_screen)
        print(f"Rect após update: {entity1.rect}")

    # Testar imagem via setter
    new_img = pygame.Surface((70, 70), pygame.SRCALPHA)
    new_img.fill((0, 0, 255, 255))  # Azul
    entity1.image = new_img
    print(f"\nImage trocada. Nova imagem: {entity1.image}")
    print(f"Novo Rect (mesma posição, novo tamanho): {entity1.rect}")