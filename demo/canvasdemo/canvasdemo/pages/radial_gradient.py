from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class RadialGradientPage(Page):
    def draw(self, renderer: Renderer):
        with self.canvas_target(renderer) as canvas:
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
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(RadialGradientPage, "radial_gradient", "Radial Gradient"))