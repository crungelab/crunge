import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader

from box2d_demo.entity import DynamicEntity2D
from box2d_demo.physics.geom import BallGeom


class Ball(DynamicEntity2D):
    def __init__(self, position: glm.vec2) -> None:
        sprite = SpriteLoader().load(":resources:/tiled/items/coinGold.png")
        scale = glm.vec2(.5, .5)
        super().__init__(position, scale=scale, vu=SpriteVu(), model=sprite, geom=BallGeom())
