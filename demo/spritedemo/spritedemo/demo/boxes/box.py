import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom


class Box(DynamicEntity2D):
    def __init__(self, position: glm.vec2) -> None:
        texture = ImageTextureLoader().load(":images:/boxCrate.png")
        sprite = Sprite(texture)
        vu = SpriteVu(sprite).create()
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, vu=vu, geom=BoxGeom)
