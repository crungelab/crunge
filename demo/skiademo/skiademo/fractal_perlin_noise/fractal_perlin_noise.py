from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo


class FractalPerlinNoiseDemo(Demo):
    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        with self.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            shader = skia.PerlinNoiseShader.make_fractal_noise(0.05, 0.05, 4, 0.0)
            # logger.debug(f"shader: {shader}")

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)


def main():
    FractalPerlinNoiseDemo().run()


if __name__ == "__main__":
    main()
