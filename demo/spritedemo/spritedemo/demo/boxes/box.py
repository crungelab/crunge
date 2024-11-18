import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from ...model_2d import DynamicModel2D
from ...geom import BoxGeom


class Box(DynamicModel2D):
    def __init__(self, position: glm.vec2) -> None:
        texture = ImageTextureLoader().load(":images:/boxCrate.png")
        sprite = Sprite(texture)
        vu = SpriteVu(sprite).create()
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, vu=vu, geom=BoxGeom)
