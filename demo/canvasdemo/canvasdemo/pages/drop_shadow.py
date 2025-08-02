from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class DropShadowPage(Page):
    def _draw(self):
        renderer = Renderer.get_current()
        with renderer.canvas_target() as canvas:
            canvas.draw_color(skia.colors.WHITE)

            filter = skia.ImageFilters.drop_shadow(3, 3, 5, 5, skia.colors.BLACK)
            filter_paint = skia.Paint()
            filter_paint.set_image_filter(filter)

            font = skia.Font()
            font.set_size(120)
            # font.set_typeface(skia.Typeface('Arial'))
            # font.set_typeface(None)
            canvas.draw_string("Hello Skia!", 0, 160, font, filter_paint)
        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(DropShadowPage, "drop_shadow", "Drop Shadow"))
