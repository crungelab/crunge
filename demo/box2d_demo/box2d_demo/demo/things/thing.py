import glm

from crunge.engine.d2.entity import Entity2D
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.physics import DynamicPhysics
from crunge.engine.d2.physics.geom import HullGeom


class Thing(Entity2D):
    geom = HullGeom()
    vu_class = SpriteVu
    physics_class = DynamicPhysics
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, model=sprite)
