from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer


class TurbulentPerlinNoiseDemo(Demo):
    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            shader = skia.PerlinNoiseShader.make_turbulence(0.05, 0.05, 4, 0.0)

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)


def main():
    TurbulentPerlinNoiseDemo().run()


if __name__ == "__main__":
    main()
