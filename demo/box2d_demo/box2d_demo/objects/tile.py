import glm

from box2d_demo.physics.geom import BoxGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2 import Node2D

from box2d_demo.entity import StaticEntity2D


class Tile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, vu=SpriteVu(sprite), model=sprite)

class BoxTile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, vu=SpriteVu(sprite), model=sprite, geom=BoxGeom())

class GhostTile(Node2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        super().__init__(position, vu=SpriteVu(sprite), model=sprite)

class RunColliderTile(StaticEntity2D):
    """Invisible merged collider spanning a run of tiles. No sprite/vu -
    GhostTile already handles rendering for each tile in the run; this
    exists purely to give the run a single seamless BoxGeom instead of
    one per tile."""
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        # ASSUMPTION: StaticEntity2D/Node2D accepts vu=None, model=None for
        # a physics-only, non-rendered body. Every existing entity in this
        # codebase (Tile, BoxTile, Chassis, Wheel) always passes a vu, so
        # this pattern is unconfirmed - if it errors, the fallback is
        # passing a real SpriteVu(sprite) here too and just accepting the
        # stretched texture as a (harmless but ugly) debug visual, or
        # checking whether Node2D exposes a NullVu / visible=False flag.
        #super().__init__(position, scale=scale, vu=None, model=None, geom=BoxGeom())
        super().__init__(position, scale=scale, vu=None, model=None, geom=BoxGeom())