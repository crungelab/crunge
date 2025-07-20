from loguru import logger

from ....renderer import Renderer
from ....vu_group import VuGroup

from .. import SpriteVu


class SpriteVuGroup(VuGroup[SpriteVu]):
    def __init__(self):
        super().__init__()
        self.is_render_group = False

    def draw(self, renderer: Renderer) -> None:
        for sprite in self.visuals:
            #logger.debug(f"SpriteGroup.draw: {sprite}")
            frustum = renderer.camera_2d.frustum
            if sprite.bounds.intersects(frustum):
                sprite.draw(renderer)

    def update(self, delta_time: float) -> None:
        for sprite in self.visuals:
            sprite.update(delta_time)
