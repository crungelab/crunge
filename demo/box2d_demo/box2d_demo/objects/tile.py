import glm

from crunge.engine.d2.physics.geom import BoxGeom, ChainGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2 import Node2D

from crunge.engine.d2.entity import StaticEntity2D


class Tile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class BoxTile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite, geom=BoxGeom())


class ChainTile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite, geom=ChainGeom())


class GhostTile(Node2D):
    default_vu = SpriteVu
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class RunColliderTile(StaticEntity2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale, model=None, geom=BoxGeom())


class TerrainModel:
    def __init__(self, points: list[tuple[float, float]]) -> None:
        self.points = points

    @property
    def size(self) -> glm.vec2:
        if not self.points:
            return glm.vec2(0.0, 0.0)
        xs, ys = zip(*self.points)
        return glm.vec2(max(xs) - min(xs), max(ys) - min(ys))


class TerrainColliderTile(StaticEntity2D):
    default_vu = None
    def __init__(self, points: list[tuple[float, float]]) -> None:
        model = TerrainModel(points)
        super().__init__(model=model, geom=ChainGeom())


"""
class TerrainColliderTile(StaticEntity2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale, vu=None, model=None, geom=ChainGeom())
"""
