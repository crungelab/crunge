from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class RoundedRectanglePage(Page):
    def _draw(self):
        canvas = Renderer.get_current().canvas

        paint = skia.Paint()
        paint.set_color(0xFFFFFFFF)
        paint.set_anti_alias(True)

        rect = skia.Rect(10, 10, 210, 110)
        canvas.draw_round_rect(rect, 20, 20, paint)

        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(RoundedRectanglePage, "rounded_rectangle", "Rounded Rectangle"))