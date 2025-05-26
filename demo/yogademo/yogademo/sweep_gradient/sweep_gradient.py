from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer


class SweepGradientDemo(Demo):
    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            shader = skia.GradientShader.make_sweep(
                128.0,
                128.0,
                [
                    skia.colors.CYAN,
                    skia.colors.MAGENTA,
                    skia.colors.YELLOW,
                    skia.colors.CYAN,
                ],
            )
            # logger.debug(f"shader: {shader}")

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)


def main():
    SweepGradientDemo().run()


if __name__ == "__main__":
    main()
