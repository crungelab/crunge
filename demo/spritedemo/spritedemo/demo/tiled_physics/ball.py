import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BallGeom


class Ball(DynamicEntity2D):
    def __init__(self, position: glm.vec2) -> None:
        texture = ImageTextureLoader().load(":resources:/tiled/items/coinGold.png")
        sprite = Sprite(texture)
        vu = SpriteVu(sprite).create()
        scale = glm.vec2(.5, .5)
        super().__init__(position, scale=scale, vu=vu, geom=BallGeom)
        self.size = self.size * .5
