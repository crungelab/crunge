from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class CirclePage(Page):
    def draw(self, renderer: Renderer):
        with renderer.canvas_target() as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_circle(skia.Point(10, 10), 10, paint)
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(CirclePage, "circle", "Circle"))