from loguru import logger

from ....renderer import Renderer
from ....vu_group import VuGroup

from .. import SpriteVu


class SpriteVuGroup(VuGroup[SpriteVu]):
    def __init__(self):
        super().__init__()
        self.is_buffered_group = False
        self.is_render_group = False


    '''
    def draw(self, renderer: Renderer) -> None:
        frustum = renderer.camera_2d.frustum
        for vu in self.visuals:
            #logger.debug(f"SpriteVuGroup.draw: {vu}")
            if vu.bounds.intersects(frustum):
                vu.draw(renderer)
    '''
    
    def update(self, delta_time: float) -> None:
        for vu in self.visuals:
            vu.update(delta_time)
