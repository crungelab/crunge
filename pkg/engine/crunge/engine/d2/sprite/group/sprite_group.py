from ....renderer import Renderer
from ....vu_group import VuGroup

from .. import Sprite


class SpriteGroup(VuGroup[Sprite]):
    def __init__(self):
        super().__init__()
        self.is_render_group = False

    def draw(self, renderer: Renderer) -> None:
        for sprite in self.members:
            projection = renderer.camera_2d.projection
            if sprite.aabb.intersects(projection):
                sprite.draw(renderer)

    def update(self, delta_time: float) -> None:
        for sprite in self.members:
            sprite.update(delta_time)
