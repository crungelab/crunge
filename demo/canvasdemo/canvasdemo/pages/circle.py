from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class CirclePage(Page):
    def _draw(self):
        renderer = Renderer.get_current()
        with renderer.canvas_target() as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_circle(skia.Point(10, 10), 10, paint)
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(CirclePage, "circle", "Circle"))