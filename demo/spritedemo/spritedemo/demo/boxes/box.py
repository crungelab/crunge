import glm

from ...sprite import Sprite
#from ...node_2d import Node2D
from ...model_2d import DynamicModel2D
from ...texture_kit import TextureKit
from ...resource_kit import ResourceKit
from ...geom import BoxGeom

class Box(DynamicModel2D):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(geom=BoxGeom)
        path = ResourceKit().root / "images" / "boxCrate.png"
        texture = TextureKit().load(path)
        self.vu = Sprite(texture)
        self.position = position
        self.size = texture.size * .25
        #self.size = texture.size
