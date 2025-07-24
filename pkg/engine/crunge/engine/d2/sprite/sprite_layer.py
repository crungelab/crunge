from ... import Renderer

from .. import Node2D
from ..scene_layer_2d import SceneLayer2D

from .sprite_vu_group import SpriteVuGroup
from .sprite_group import SpriteGroup

class SpriteLayer(SceneLayer2D):
    def __init__(self, name: str = "SpriteInstanceLayer", count: int = 32) -> None:
        super().__init__(name)
        self.vu_group: SpriteVuGroup = None
        self.sprite_group: SpriteGroup = None

    def attach(self, node: Node2D) -> None:
        self.vu_group.append(node.vu)
        super().attach(node)

    '''
    def detach(self, node: Node2D) -> None:
        self.vu_group.remove(node.vu)
        super().detach(node)
    '''