import glm

from crunge.engine.d2.sprite import Sprite
from crunge.engine.loader.texture_loader import TextureLoader

from ...model_2d import DynamicModel2D
from ...geom import BoxGeom

class Box(DynamicModel2D):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(geom=BoxGeom)
        texture = TextureLoader().load(":images:/boxCrate.png")
        self.vu = Sprite(texture)
        self.position = position
        self.size = glm.vec2(texture.size.x, texture.size.y) * .25
