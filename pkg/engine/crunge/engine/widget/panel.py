from loguru import logger

from crunge import skia

from . import Widget
from ..renderer import Renderer


class Panel(Widget):
    def __init__(self, paint: skia.Paint = None, **kwargs):
        super().__init__(**kwargs)
        if paint is None:
            paint = skia.Paint()
            #paint.set_color(0xFFFFFFFF)
            paint.set_color(0xFF181A1B)

        self.paint = paint

    def _draw(self):
        canvas = Renderer.get_current().canvas

        position = self.global_position
        size = self.size

        canvas.draw_rect(skia.Rect(position.x, position.y, size.x, size.y), self.paint)
        super()._draw()
