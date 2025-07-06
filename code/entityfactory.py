import pygame
import os
from typing import Dict, Any, Tuple
from .entity import Entity
from .background import Background

class EntityFactory:
    _ENTITY_RESOURCES: Dict[str, Dict[str, Any]] = {
        "Background": {
            "image_filename": "menubg.png",
            "default_size": (800, 600),
            "default_color": (0, 0, 0, 255)
        },
        "Player": {
            "image_filename": "playerwalk1.png",
            "default_size": (50, 50),
            "default_color": (0, 255, 0, 255)
        },
        "Enemy": {
            "image_filename": "enemy1walk1.png",
            "default_size": (40, 40),
            "default_color": (255, 0, 0, 255)
        }
    }

    @staticmethod
    def _load_image(image_filename: str, default_size: Tuple[int, int],
                    default_color: Tuple[int, int, int, int]) -> pygame.Surface:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, '..', 'asset', image_filename)
        try:
            image = pygame.image.load(image_path).convert_alpha()
            return image
        except (pygame.error, Exception):
            fallback_image = pygame.Surface(default_size, pygame.SRCALPHA)
            fallback_image.fill(default_color)
            return fallback_image

    @staticmethod
    def create_entity(entity_type: str, *args, **kwargs) -> Entity:
        resource_info = EntityFactory._ENTITY_RESOURCES.get(entity_type)
        if not resource_info:
            raise ValueError(f"Tipo de entidade desconhecido: '{entity_type}'.")

        image_filename = kwargs.pop('image_filename', resource_info.get('image_filename'))
        image = None
        if image_filename:
            image = EntityFactory._load_image(image_filename, resource_info.get('default_size'),
                                              resource_info.get('default_color'))

        kwargs['image'] = image
        if 'name' not in kwargs and not args:
            kwargs['name'] = entity_type

        if entity_type == "Background":
            return Background(*args, **kwargs)
        else:
            raise NotImplementedError(f"A criação para o tipo '{entity_type}' não foi implementada.")