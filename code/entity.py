import pygame
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class Entity(ABC):
    """
    Classe base abstrata para todas as entidades do jogo.
    Define a interface comum para objetos que precisam ser atualizados e desenhados.
    """

    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            width: Optional[int] = None,
            height: Optional[int] = None,
            image: Optional[pygame.Surface] = None,
            color: Optional[Tuple[int, int, int]] = None
    ):
        self._name: str = name
        self._image: pygame.Surface
        self._rect: pygame.Rect

        if image:
            self._image = image
            self._rect = self._image.get_rect(topleft=(x, y))
        else:
            if width is None or height is None:
                raise ValueError("Se 'image' não for fornecido, 'width' e 'height' devem ser especificados.")

            self._image = pygame.Surface((width, height), pygame.SRCALPHA)
            self._image.fill(color if color else (255, 255, 255, 255))
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
        self._rect = self._image.get_rect(topleft=self._rect.topleft)

    @property
    def rect(self) -> pygame.Rect:
        """Retorna o objeto Pygame.Rect da entidade."""
        return self._rect

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Método abstrato para atualizar o estado da entidade (ex: posição, animação, lógica).
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Método abstrato para desenhar a entidade na tela.
        """
        pass

    @abstractmethod
    def move(self) -> None:
        """
        Método abstrato para lidar com a lógica de movimento da entidade.
        """
        pass