from loguru import logger

from ... import Node2D
from ...scene.layer.graph_layer_2d import GraphLayer2D

from .instanced_sprite_vu_group import InstancedSpriteVuGroup
from ..dynamic.dynamic_sprite_group import DynamicSpriteGroup


class InstancedSpriteLayer(GraphLayer2D):
    def __init__(
        self,
        name: str = "SpriteInstanceLayer",
        count: int = 32,
        sprite_group: DynamicSpriteGroup = None,
    ) -> None:
        super().__init__(name)
        logger.debug(
            f"InstancedSpriteLayer: {name}, count: {count}, sprite_group: {sprite_group}"
        )
        self.vu_group = InstancedSpriteVuGroup(count, sprite_group).enable()
        self.sprite_group = sprite_group

    def _draw(self) -> None:
        self.vu_group.draw()

    def _render(self) -> None:
        self.vu_group.draw()

    def attach(self, node: Node2D) -> None:
        self.vu_group.append(node.vu)
        super().attach(node)

    def detach(self, node: Node2D) -> None:
        self.vu_group.remove(node.vu)
        super().detach(node)
