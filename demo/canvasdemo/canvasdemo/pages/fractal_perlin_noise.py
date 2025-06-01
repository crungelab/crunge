from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class FractalPerlinNoisePage(Page):
    def draw(self, renderer: Renderer):
        with self.canvas_target(renderer) as canvas:
            gradient_paint = skia.Paint()

            shader = skia.PerlinNoiseShader.make_fractal_noise(0.05, 0.05, 4, 0.0)
            # logger.debug(f"shader: {shader}")

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(FractalPerlinNoisePage, "fractal_perlin_noise", "Fractal Perlin Noise"))