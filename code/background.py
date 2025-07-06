import pygame
from typing import Optional, Tuple
from .entity import Entity


class Background(Entity):
    """
    Representa o plano de fundo do jogo. Herda de Entity.
    Pode ser estático ou ter lógica de rolagem (scrolling).
    """

    def __init__(
            self,
            name: str = "GameBackground",
            x: int = 0,
            y: int = 0,
            image: Optional[pygame.Surface] = None,
            scroll_speed_x: float = 0,
            scroll_speed_y: float = 0
    ):
        if image is None:
            default_width, default_height = 800, 600
            temp_image = pygame.Surface((default_width, default_height))
            temp_image.fill((0, 0, 0))
            super().__init__(name, x, y, image=temp_image)
        else:
            super().__init__(name, x, y, image=image)

        self._scroll_speed_x: float = scroll_speed_x
        self._scroll_speed_y: float = scroll_speed_y
        self._image_width = self.image.get_width()
        self._image_height = self.image.get_height()

    def update(self, delta_time: float) -> None:
        """
        Atualiza o estado do background, aplicando a rolagem.
        """
        self.move()

        if self._scroll_speed_x < 0 and self.rect.right <= 0:
            self.rect.x = self._image_width
        elif self._scroll_speed_x > 0 and self.rect.left >= self._image_width:
            self.rect.x = -self._image_width

        if self._scroll_speed_y < 0 and self.rect.bottom <= 0:
            self.rect.y = self._image_height
        elif self._scroll_speed_y > 0 and self.rect.top >= self._image_height:
            self.rect.y = -self._image_height

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o background na tela.
        """
        screen.blit(self.image, self.rect)

        if self._scroll_speed_x != 0:
            if self.rect.x < 0:
                screen.blit(self.image, (self.rect.x + self._image_width, self.rect.y))
            elif self.rect.x > 0:
                screen.blit(self.image, (self.rect.x - self._image_width, self.rect.y))

        if self._scroll_speed_y != 0:
            if self.rect.y < 0:
                screen.blit(self.image, (self.rect.x, self.rect.y + self._image_height))
            elif self.rect.y > 0:
                screen.blit(self.image, (self.rect.x, self.rect.y - self._image_height))

    def move(self) -> None:
        """
        Implementa a lógica de movimento (rolagem) do background.
        """
        self._rect.x += self._scroll_speed_x
        self._rect.y += self._scroll_speed_y