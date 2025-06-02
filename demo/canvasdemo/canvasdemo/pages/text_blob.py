from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class TextBlobPage(Page):
    def draw(self, renderer: Renderer):
        with renderer.canvas_target() as canvas:
            # canvas.clear(0xFF00FF00)  # Clear with a color

            paint = skia.Paint()
            paint.set_color(0xFFFF00FF)
            # font = skia.Font(None, 36)
            font = skia.Font()
            font.set_size(36)
            # font.set_typeface(skia.Typeface('Arial'))
            # font.set_typeface(None)
            blob = skia.TextBlob.make_from_string("Hello Skia!", font)
            canvas.draw_text_blob(blob, 10, 32, paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(TextBlobPage, "text_blob", "Text Blob"))
