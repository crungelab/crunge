from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class SweepGradientPage(Page):
    def _draw(self):
        canvas = Renderer.get_current().canvas
        
        gradient_paint = skia.Paint()

        shader = skia.Shader.create_sweep_gradient(
            skia.Point(128.0, 128.0),
            [
                skia.colors4f.CYAN,
                skia.colors4f.MAGENTA,
                skia.colors4f.YELLOW,
                skia.colors4f.CYAN,
            ],
        )
        # logger.debug(f"shader: {shader}")

        gradient_paint.set_shader(shader)
        canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)

        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(SweepGradientPage, "sweep_gradient", "Sweep Gradient"))