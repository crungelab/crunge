import glm

from crunge.engine.d2.sprite import Sprite
#from crunge.engine.resource.texture_kit import TextureKit
from crunge.engine.loader.texture_loader import TextureLoader
from crunge.engine.resource.resource_manager import ResourceManager

from ...model_2d import DynamicModel2D
from ...geom import BoxGeom

class Box(DynamicModel2D):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(geom=BoxGeom)
        #path = ResourceManager().root / "images" / "boxCrate.png"
        path = "{images}/boxCrate.png"
        #texture = TextureKit().load(path)
        texture = TextureLoader().load(path)
        self.vu = Sprite(texture)
        self.position = position
        self.size = glm.vec2(texture.size.x, texture.size.y) * .25
