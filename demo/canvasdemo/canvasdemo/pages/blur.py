from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class BlurPage(Page):
    def reset(self):
        self.font = skia.Font()
        self.font.set_size(120)
        # self.font.set_typeface(skia.Typeface('Arial'))
        # self.font.set_typeface(None)

    def _draw(self):
        canvas = Renderer.get_current().canvas
        canvas.draw_color(skia.colors.WHITE)

        #filter = skia.ImageFilters.drop_shadow(3, 3, 5, 5, skia.colors.BLACK)
        filter = skia.ImageFilters.blur(5, 5)
        filter_paint = skia.Paint()
        filter_paint.set_image_filter(filter)

        canvas.draw_string("Hello Skia!", 0, 160, self.font, filter_paint)
        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(BlurPage, "blur", "Blur"))
