from loguru import logger

from ...renderer import Renderer
from ...vu_group import VuGroup

from . import SpriteVu
from . import SpriteGroup


class SpriteVuGroup(VuGroup[SpriteVu]):
    def __init__(self, sprite_group: SpriteGroup) -> None:
        super().__init__()
        self.is_dynamic_group = False
        self.is_render_group = False
        self.sprite_group = sprite_group

    def _draw(self) -> None:
        renderer = Renderer.get_current()
        frustum = renderer.camera_2d.frustum
        for vu in self.members:
            if vu.bounds.intersects(frustum):
                vu.draw()

    # `update` dropped: it was identical to VuGroup's.