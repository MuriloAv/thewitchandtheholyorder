# background.py

import pygame
from typing import Optional, Tuple
from entity import Entity  # Importa a classe base Entity

# A seção de MOCK para Pygame é importante para testes independentes.
# Para evitar repetição excessiva, e como entity.py já a define,
# vamos assumir que pygame (ou seu mock) já está disponível via `import pygame`.
# No entanto, se este arquivo for executado isoladamente, ele precisaria da definição do mock novamente,
# ou de uma importação de um módulo utilitário de mock.
# Para este exercício, vou reintroduzir o mock simplificado para clareza e auto-suficiência.
try:
    import pygame
except ImportError:
    print("Pygame não encontrado em background.py. Usando objetos mock.")


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
            (800, 600))  # Tamanho de fundo padrão


    class MockPygame:
        def __init__(self): self.Rect = MockRect; self.Surface = MockSurface; self.image = MockImage()


    pygame = MockPygame()


# --- FIM DO MOCK ---


class Background(Entity):
    """
    Representa o plano de fundo do jogo. Herda de Entity.
    Pode ser estático ou ter lógica de rolagem (scrolling).
    """

    def __init__(self,
                 name: str = "GameBackground",
                 x: int = 0,
                 y: int = 0,
                 image: Optional[pygame.Surface] = None,
                 scroll_speed_x: float = 0,
                 scroll_speed_y: float = 0):
        """
        Inicializa o background.

        Args:
            name (str): Nome do background (padrão: "GameBackground").
            x (int): Posição inicial X do background.
            y (int): Posição inicial Y do background.
            image (Optional[pygame.Surface]): A imagem do background.
                                               Se não fornecida, uma superfície padrão será criada.
            scroll_speed_x (float): Velocidade de rolagem horizontal em pixels por segundo.
            scroll_speed_y (float): Velocidade de rolagem vertical em pixels por segundo.
        """
        # Se nenhuma imagem for fornecida, cria uma superfície grande preta como padrão
        if image is None:
            # Tenta usar um tamanho razoável para um background padrão
            # Em um jogo real, isso viria de uma constante ou configuração.
            default_width, default_height = 800, 600
            temp_image = pygame.Surface((default_width, default_height))
            temp_image.fill((0, 0, 0))  # Fundo preto
            super().__init__(name, x, y, image=temp_image)
        else:
            super().__init__(name, x, y, image=image)

        self._scroll_speed_x: float = scroll_speed_x
        self._scroll_speed_y: float = scroll_speed_y

        # Se for um background rolante que repete, podemos precisar de cópias da imagem
        # Para um background simples que apenas rola e desaparece, uma imagem é suficiente.
        # Para um background que se repete infinitamente, precisaríamos de 2 ou mais cópias
        # e lógica para resetar a posição quando sair da tela.
        # Para esta implementação inicial, vamos focar em uma única imagem que pode rolar.
        # A lógica de repetição será adicionada na `draw` ou `update` se o `scroll_speed` for ativo.
        self._image_width = self.image.get_width()
        self._image_height = self.image.get_height()

    def update(self, delta_time: float) -> None:
        """
        Atualiza o estado do background, aplicando a rolagem.

        Args:
            delta_time (float): Tempo decorrido desde o último frame em segundos.
        """
        self.move()  # Chama o método move para aplicar a rolagem

        # Exemplo de lógica de rolagem contínua para um background que se repete:
        # Se o background rolar para fora da tela, "teleporta" para o outro lado
        # para criar um loop contínuo.
        if self._scroll_speed_x < 0 and self.rect.right <= 0:  # Rolando para a esquerda
            self.rect.x = self._image_width  # Move para a direita da tela
        elif self._scroll_speed_x > 0 and self.rect.left >= self._image_width:  # Rolando para a direita
            self.rect.x = -self._image_width  # Move para a esquerda da tela

        if self._scroll_speed_y < 0 and self.rect.bottom <= 0:  # Rolando para cima
            self.rect.y = self._image_height  # Move para baixo da tela
        elif self._scroll_speed_y > 0 and self.rect.top >= self._image_height:  # Rolando para baixo
            self.rect.y = -self._image_height  # Move para cima da tela

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o background na tela.
        Para backgrounds rolantes repetitivos, pode desenhar múltiplas cópias.

        Args:
            screen (pygame.Surface): A superfície Pygame onde o background será desenhada.
        """
        # Desenha a imagem principal
        screen.blit(self.image, self.rect)

        # Se o background está rolando, desenha uma cópia adjacente para criar um efeito contínuo
        # Isso é uma forma simples de fazer scroll infinito. Dependendo da complexidade,
        # pode-se precisar de mais cópias ou uma superfície maior para o background.
        if self._scroll_speed_x != 0:
            # Desenha uma cópia à direita/esquerda para rolagem horizontal
            if self.rect.x < 0:  # Se está rolando para a esquerda e parte já saiu
                screen.blit(self.image, (self.rect.x + self._image_width, self.rect.y))
            elif self.rect.x > 0:  # Se está rolando para a direita e parte já saiu
                screen.blit(self.image, (self.rect.x - self._image_width, self.rect.y))

        if self._scroll_speed_y != 0:
            # Desenha uma cópia acima/abaixo para rolagem vertical
            if self.rect.y < 0:  # Se está rolando para cima e parte já saiu
                screen.blit(self.image, (self.rect.x, self.rect.y + self._image_height))
            elif self.rect.y > 0:  # Se está rolando para baixo e parte já saiu
                screen.blit(self.image, (self.rect.x, self.rect.y - self._image_height))

    def move(self) -> None:
        """
        Implementa a lógica de movimento (rolagem) do background.
        Esta é a implementação concreta do método abstrato `move` de Entity.
        """
        # Aplica a velocidade de rolagem diretamente à posição do rect.
        # delta_time já foi aplicada no update. Aqui só se move.
        self._rect.x += self._scroll_speed_x
        self._rect.y += self._scroll_speed_y


# Exemplo de uso (para teste local):
if __name__ == "__main__":
    print("Testando a classe Background.")

    # Simula a inicialização do Pygame
    pygame.init()
    # Mocka o display para que `blit` funcione sem erro, embora não visualize nada
    mock_screen = pygame.Surface((800, 600))
    print(f"Tela mock criada com tamanho: {mock_screen.get_rect()}")

    # Criar um background estático
    static_bg = Background(name="StaticBG", x=0, y=0)
    print(f"\nBackground Estático: {static_bg.name}, Posição: {static_bg.rect.topleft}")
    static_bg.update(0.1)  # Atualiza, mas não há rolagem
    static_bg.draw(mock_screen)

    # Criar um background rolante
    # Nota: A imagem mock padrão para o background é 800x600.
    # Para rolagem, a imagem deveria ser maior que a tela ou ter lógica de repetição.
    scrolling_bg = Background(name="ScrollingBG", x=0, y=0, scroll_speed_x=-5)  # Rola para a esquerda
    print(f"\nBackground Rolante: {scrolling_bg.name}, Posição: {scrolling_bg.rect.topleft}")

    for i in range(5):
        print(f"--- Ciclo {i + 1} de rolagem ---")
        scrolling_bg.update(1)  # Simula 1 segundo de delta_time
        scrolling_bg.draw(mock_screen)
        print(f"Posição após update: {scrolling_bg.rect.topleft}")
        # A lógica de repetição move o background de volta quando ele sai da tela
        # No mock, veremos a posição do rect "resetar".