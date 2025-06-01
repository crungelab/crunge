from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class ConicalGradientPage(Page):
    def draw(self, renderer: Renderer):
        with self.canvas_target(renderer) as canvas:
            gradient_paint = skia.Paint()

            shader = skia.GradientShader.make_two_point_conical(
                skia.Point(128.0, 128.0),
                128.0,
                skia.Point(128.0, 16.0),
                16.0,
                [0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
            )
            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(ConicalGradientPage, "conical_gradient", "Conical Gradient"))
