import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom


class Box(DynamicEntity2D):
    def __init__(self, position: glm.vec2) -> None:
        sprite = SpriteLoader().load(":images:/boxCrate.png")
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, vu=SpriteVu(), model=sprite, geom=BoxGeom())
