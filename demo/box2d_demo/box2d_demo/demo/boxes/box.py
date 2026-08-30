import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader

from crunge.engine.d2 import Node2D
from crunge.engine.d2.physics import DynamicPhysics
from crunge.engine.d2.physics.geom import BoxGeom


class Box(Node2D):
    def __init__(self, position: glm.vec2) -> None:
        sprite = SpriteLoader().load("${images}/boxCrate.png")
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, model=sprite)

    def _seat(self) -> None:
        super()._seat()
        self.add(SpriteVu())
        self.add(DynamicPhysics(BoxGeom()))
