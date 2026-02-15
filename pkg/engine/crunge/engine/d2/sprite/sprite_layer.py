from .. import Node2D
from ..scene.layer.graph_layer_2d import GraphLayer2D

from .sprite_vu_group import SpriteVuGroup
from .sprite_group import SpriteGroup

class SpriteLayer(GraphLayer2D):
    def __init__(self, name: str = "SpriteInstanceLayer", count: int = 32) -> None:
        super().__init__(name)
        self.vu_group: SpriteVuGroup = None
        self.sprite_group: SpriteGroup = None

    def attach(self, node: Node2D) -> None:
        super().attach(node)
        self.vu_group.append(node.vu)

    def detach(self, node: Node2D) -> None:
        super().detach(node)
        self.vu_group.remove(node.vu)
