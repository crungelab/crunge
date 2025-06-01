from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class LinearGradientPage(Page):
    def draw(self, renderer: Renderer):
        with self.canvas_target(renderer) as canvas:
            gradient_paint = skia.Paint()
            # logger.debug(f"gradient_paint: {gradient_paint}")

            shader = skia.GradientShader.make_linear(
                [skia.Point(0, 0), skia.Point(256.0, 256.0)],
                [0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
                # [0, 1],
                # skia.TileMode.K_CLAMP,
            )

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(LinearGradientPage, "linear_gradient", "Linear Gradient"))