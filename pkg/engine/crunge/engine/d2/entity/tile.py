from loguru import logger

import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2 import Node2D

from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.scene.layer import GraphLayer2D


class Tile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class GhostTile(Node2D):
    vu_class = SpriteVu
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class TileLayer(GraphLayer2D):
    def __init__(self, name):
        super().__init__(name)
