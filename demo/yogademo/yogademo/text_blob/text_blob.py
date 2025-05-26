from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer


class TextBlobDemo(Demo):
    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
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


def main():
    TextBlobDemo().run()


if __name__ == "__main__":
    main()
