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
        renderer = Renderer.get_current()
        canvas = renderer.canvas

        position = self.global_position
        size = self.size

        canvas.draw_rect(skia.Rect(position.x, position.y, size.x, size.y), self.paint)
        super()._draw()

    '''
    def _draw(self):
        try:
            canvas = renderer.canvas
            bounds = self.bounds
            left = bounds.left
            top = bounds.top
            width = bounds.width
            height = bounds.height
            #logger.debug(f"Node Layout: Left={left}, Top={top}, Width={width}, Height={height}")
            canvas.draw_rect(skia.Rect(left, top, width, height), self.paint)
        except(Exception) as e:
            logger.error(f"Unexpected error drawing panel: {e}")
        super()._draw()
    '''