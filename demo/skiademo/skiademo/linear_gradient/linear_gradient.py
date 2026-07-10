from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer


class LinearGradientDemo(Demo):
    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            shader = skia.Shader.create_linear_gradient(
                skia.Point(0.0, 0.0), skia.Point(256.0, 256.0),
                [
                    skia.colors4f.BLUE,
                    skia.colors4f.YELLOW,
                ],
                [],  # even positions
                skia.TileMode.K_CLAMP,
                None,
            )

            '''
            shader = skia.GradientShader.make_linear(
                [skia.Point(0, 0), skia.Point(256.0, 256.0)],
                [0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
                # [0, 1],
                # skia.TileMode.K_CLAMP,
            )
            '''

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)


def main():
    LinearGradientDemo().run()


if __name__ == "__main__":
    main()
