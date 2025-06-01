from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class RectanglePage(Page):
    def draw(self, renderer: Renderer):
        with self.canvas_target(renderer) as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(RectanglePage, "rectangle", "Rectangle"))