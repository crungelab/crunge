from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class TextPage(Page):
    def reset(self):
        self.font = skia.Font()
        self.font.set_size(36)

    def _draw(self):
        canvas = Renderer.get_current().canvas
        
        # canvas.clear(0xFF00FF00)  # Clear with a color

        paint = skia.Paint()
        paint.set_color(0xFFFF00FF)
        canvas.draw_string("Hello Skia!", 10, 32, self.font, paint)

        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(TextPage, "text", "Text"))
    logger.debug("TextPage installed")