from ...renderer import Renderer
from ...vu_group import VuGroup

from .base_sprite_group import BaseSpriteGroup
from .base_sprite_vu import BaseSpriteVu


class BaseSpriteVuGroup[VuT: BaseSpriteVu](VuGroup[VuT]):
    """A batch of sprite-like vus sharing one model group — the group whose
    uniform buffer their models are members of."""

    def __init__(self, model_group: BaseSpriteGroup, is_managed: bool = False) -> None:
        super().__init__(is_managed=is_managed)
        self.is_dynamic_group = False
        #self.is_render_group = False
        self.model_group = model_group

    def _draw(self) -> None:
        renderer = Renderer.get_current()
        frustum = renderer.camera_2d.frustum
        for vu in self.members:
            if vu.bounds.intersects(frustum):
                vu.draw()
