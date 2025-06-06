from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer


class RectangleDemo(Demo):
    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)


def main():
    RectangleDemo().run()


if __name__ == "__main__":
    main()
