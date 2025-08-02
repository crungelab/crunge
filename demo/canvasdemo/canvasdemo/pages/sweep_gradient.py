from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class SweepGradientPage(Page):
    def _draw(self):
        canvas = Renderer.get_current().canvas
        
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

        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(SweepGradientPage, "sweep_gradient", "Sweep Gradient"))