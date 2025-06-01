from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class DropShadowPage(Page):
    def draw(self, renderer: Renderer):
        with self.canvas_target(renderer) as canvas:
            canvas.draw_color(skia.colors.WHITE)

            filter = skia.ImageFilters.drop_shadow(3, 3, 5, 5, skia.colors.BLACK)
            filter_paint = skia.Paint()
            filter_paint.set_image_filter(filter)

            font = skia.Font()
            font.set_size(120)
            # font.set_typeface(skia.Typeface('Arial'))
            # font.set_typeface(None)
            canvas.draw_string("Hello Skia!", 0, 160, font, filter_paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(DropShadowPage, "drop_shadow", "Drop Shadow"))
