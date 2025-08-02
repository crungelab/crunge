from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class RectanglePage(Page):
    def _draw(self):
        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(RectanglePage, "rectangle", "Rectangle"))