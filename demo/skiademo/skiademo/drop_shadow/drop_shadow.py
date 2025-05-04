from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo


class DropShadowDemo(Demo):
    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        with self.canvas_target() as canvas:
            canvas.draw_color(skia.colors.WHITE)

            filter = skia.ImageFilters.drop_shadow(3, 3, 5, 5, skia.colors.BLACK)
            filter_paint = skia.Paint()
            filter_paint.set_image_filter(filter)

            font = skia.Font()
            font.set_size(120)
            # font.set_typeface(skia.Typeface('Arial'))
            # font.set_typeface(None)
            canvas.draw_string("Hello Skia!", 0, 160, font, filter_paint)


def main():
    DropShadowDemo().run()


if __name__ == "__main__":
    main()
