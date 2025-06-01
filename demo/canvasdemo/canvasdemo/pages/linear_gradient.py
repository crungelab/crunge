from loguru import logger

from crunge import skia
from crunge import imgui
from crunge.engine import Renderer, App
from crunge.engine.color import Color, rgba_tuple_to_argb_int
from crunge.demo import PageChannel

from ..page import Page


class LinearGradientPage(Page):
    def reset(self):
        super().reset()
        self.color_1 = Color.BLUE.value
        self.color_2 = Color.YELLOW.value

    def draw(self, renderer: Renderer):
        imgui.begin("Linear Gradient")
        changed, self.color_1 = imgui.color_edit4("Color 1", self.color_1)
        changed, self.color_2 = imgui.color_edit4("Color 2", self.color_2)
        if imgui.button("Reset"):
            self.reset()
        imgui.end()

        with self.canvas_target(renderer) as canvas:
            gradient_paint = skia.Paint()
            # logger.debug(f"gradient_paint: {gradient_paint}")

            shader = skia.GradientShader.make_linear(
                [skia.Point(0, 0), skia.Point(256.0, 256.0)],
                #[0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
                [rgba_tuple_to_argb_int(self.color_1), rgba_tuple_to_argb_int(self.color_2)]
                # [0, 1],
                # skia.TileMode.K_CLAMP,
            )

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(LinearGradientPage, "linear_gradient", "Linear Gradient"))