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
        self.sprite_group = sprite_group

        # Mounted on the root, so the chip walk drives create, enable,
        # update, draw and destroy. Was a free-standing object the layer
        # enabled by hand in the constructor and forwarded draw to — and
        # never forwarded update to, which is why rebatching never ran.
        self.vu_group = self.root.add(InstancedSpriteVuGroup(count, sprite_group))

    # `_draw` is not overridden. GraphLayer._draw walks the root, which
    # draws its chips — the group among them — and then its children. The
    # old override drew only the group and skipped the node tree entirely.

    def attach(self, node: Node2D) -> None:
        vu = node.vu
        if vu is not None:
            # Before add_child: Vu2D._create reads group.is_render_group to
            # decide manual_draw, so the group has to be set before the node's
            # lifetime starts.
            self.vu_group.append(vu)
        # Vu-less nodes still join the graph. Ghost tiles and other invisible
        # collision nodes have no visual by design.
        super().attach(node)

    def detach(self, node: Node2D) -> None:
        if node.vu is not None:
            self.vu_group.remove(node.vu)
        super().detach(node)