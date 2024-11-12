import glm

from crunge.engine.d2.sprite import Sprite, SpriteMaterial

from ...model_2d import DynamicModel2D
from ...geom import BoxGeom

class Thing(DynamicModel2D):
    def __init__(self, position: glm.vec2, texture) -> None:
        super().__init__(geom=BoxGeom)
        material = SpriteMaterial(texture)
        self.vu = Sprite(material).create()
        self.position = position
        self.size = glm.vec2(texture.size.x, texture.size.y) * .25
        self.scale = glm.vec2(.25, .25)
