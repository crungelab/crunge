from loguru import logger

from ..scene.layer.render_layer_2d import RenderLayer2D

from .sprite_vu import SpriteVu
from .sprite_vu_group import SpriteVuGroup
from .dynamic.dynamic_sprite_group import DynamicSpriteGroup
from .instanced.instanced_sprite_program import InstancedSpriteProgram


class SpriteRenderLayer(RenderLayer2D):
    def __init__(
        self,
        name: str = "SpriteRenderLayer",
        count: int = 32,
        sprite_group: DynamicSpriteGroup = None,
        is_managed: bool = False,
    ) -> None:
        self.count = count
        self.sprite_group = sprite_group
        logger.debug(
            f"SpriteRenderLayer: {name}, count: {count}, sprite_group: {sprite_group}"
        )
        super().__init__(name, is_managed=is_managed)

    def register_vu_groups(self) -> None:
        # Bound to locals, deliberately. A lambda reaching through self would
        # close the cycle layer -> render_group -> factories -> closure ->
        # layer, and under gc.disable() with gen-0-only collection that
        # survives once the layer is promoted. Same shape as the use()
        # bound-method leak.
        count = self.count
        sprite_group = self.sprite_group

        self.root_render_group.register(
            SpriteVu,
            lambda: SpriteVuGroup(count, sprite_group, InstancedSpriteProgram()),
        )
