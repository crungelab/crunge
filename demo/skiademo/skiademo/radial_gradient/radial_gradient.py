from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo


class RadialGradientDemo(Demo):
    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        with self.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            shader = skia.GradientShader.make_radial(
                skia.Point(128.0, 128.0),
                180.0,
                [0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
                # [0, 1],
                # 2,
                # skia.TileMode.K_CLAMP,
            )

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)


def main():
    RadialGradientDemo().run()


if __name__ == "__main__":
    main()
