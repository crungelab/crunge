from loguru import logger

from ....renderer import Renderer
from ....vu_group import VuGroup

from .. import SpriteVu


class SpriteVuGroup(VuGroup[SpriteVu]):
    def __init__(self):
        super().__init__()
        self.is_render_group = False

    def draw(self, renderer: Renderer) -> None:
        for sprite in self.members:
            #logger.debug(f"SpriteGroup.draw: {sprite}")
            frustrum = renderer.camera_2d.frustum
            if sprite.bounds.intersects(frustrum):
                sprite.draw(renderer)

    '''
    def draw(self, renderer: Renderer) -> None:
        for sprite in self.members:
            projection = renderer.camera_2d.projection
            if sprite.aabb.intersects(projection):
                sprite.draw(renderer)
    '''

    def update(self, delta_time: float) -> None:
        for sprite in self.members:
            sprite.update(delta_time)
