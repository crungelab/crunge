from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer


class ConicalGradientDemo(Demo):
    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            shader = skia.create_two_point_conical_gradient(
                skia.Point(128.0, 128.0),
                128.0,
                skia.Point(128.0, 16.0),
                16.0,
                [
                    skia.Color4f.from_color(0xFF0000FF),  # Blue in #ARGB
                    skia.Color4f.from_color(0xFFFFFF00),  # Yellow in #ARGB
                ],
                [],  # even positions
                skia.TileMode.K_CLAMP,
                None,
            )

            '''
            shader = skia.GradientShader.make_two_point_conical(
                skia.Point(128.0, 128.0),
                128.0,
                skia.Point(128.0, 16.0),
                16.0,
                [0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
            )
            '''
            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)


def main():
    ConicalGradientDemo().run()


if __name__ == "__main__":
    main()
