from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo


class TextDemo(Demo):
    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        with self.canvas_target() as canvas:
            # canvas.clear(0xFF00FF00)  # Clear with a color

            paint = skia.Paint()
            paint.set_color(0xFFFF00FF)
            # font = skia.Font(None, 36)
            font = skia.Font()
            font.set_size(36)
            # font.set_typeface(skia.Typeface('Arial'))
            # font.set_typeface(None)
            canvas.draw_string("Hello Skia!", 10, 32, font, paint)


def main():
    TextDemo().run()


if __name__ == "__main__":
    main()
