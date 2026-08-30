import glm

from crunge.engine.d2 import Node2D
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.physics import DynamicPhysics
from crunge.engine.d2.physics.geom import HullGeom


class Thing(Node2D):
    default_vu = SpriteVu
    default_geom = HullGeom
    default_physics = DynamicPhysics
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, model=sprite)
