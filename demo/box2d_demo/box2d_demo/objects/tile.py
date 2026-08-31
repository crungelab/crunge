import glm

from crunge.engine.d2.physics.geom import HullGeom, BoxGeom, ChainGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.entity import Entity2D
from crunge.engine.d2.physics import StaticPhysics, DynamicPhysics

class Tile(Entity2D):
    geom = HullGeom()
    vu_class = SpriteVu
    physics_class = StaticPhysics
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class BoxTile(Entity2D):
    geom = BoxGeom()
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class ChainTile(Entity2D):
    geom = ChainGeom()
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class GhostTile(Entity2D):
    vu_class = SpriteVu
    physics_class = None
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, model=sprite)


class RunColliderTile(Entity2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale, model=None)


class TerrainModel:
    def __init__(self, points: list[tuple[float, float]]) -> None:
        self.points = points

    @property
    def size(self) -> glm.vec2:
        if not self.points:
            return glm.vec2(0.0, 0.0)
        xs, ys = zip(*self.points)
        return glm.vec2(max(xs) - min(xs), max(ys) - min(ys))


class TerrainColliderTile(Entity2D):
    geom = ChainGeom()
    physics_class = StaticPhysics
    def __init__(self, points: list[tuple[float, float]]) -> None:
        model = TerrainModel(points)
        super().__init__(model=model)
