from .... import Renderer

from ... import Node2D
from ..sprite_layer import SpriteLayer

from .instanced_sprite_vu_group import InstancedSpriteVuGroup

class InstancedSpriteLayer(SpriteLayer):
    def __init__(self, name: str = "SpriteInstanceLayer", count: int = 32) -> None:
        super().__init__(name)
        self.vu_group = InstancedSpriteVuGroup(count).create()

    def draw(self, renderer: Renderer) -> None:
        self.vu_group.draw(renderer)

    def attach(self, node: Node2D) -> None:
        self.vu_group.append(node.vu)
        super().attach(node)

    '''
    def detach(self, node: Node2D) -> None:
        self.vu_group.remove(node.vu)
        super().detach(node)
    '''