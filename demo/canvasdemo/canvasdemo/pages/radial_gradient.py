from loguru import logger

from crunge import skia
from crunge import imgui
from crunge.engine import Renderer, App
from crunge.engine.color import rgba_tuple_to_argb_int
from crunge.engine import colors
from crunge.demo import PageChannel

from ..page import Page


class RadialGradientPage(Page):
    def reset(self):
        super().reset()
        self.color_1 = colors.BLUE
        self.color_2 = colors.YELLOW

    def _draw(self):
        imgui.begin("Radial Gradient")
        changed, self.color_1 = imgui.color_edit4("Color 1", self.color_1)
        changed, self.color_2 = imgui.color_edit4("Color 2", self.color_2)
        if imgui.button("Reset"):
            self.reset()
        imgui.end()

        canvas = Renderer.get_current().canvas
        
        gradient_paint = skia.Paint()

        shader = skia.GradientShader.make_radial(
            skia.Point(128.0, 128.0),
            180.0,
            #[0xFF0000FF, 0xFFFFFF00],  # Blue, Yellow in #ARGB
            [rgba_tuple_to_argb_int(self.color_1), rgba_tuple_to_argb_int(self.color_2)]
            # [0, 1],
            # 2,
            # skia.TileMode.K_CLAMP,
        )

        gradient_paint.set_shader(shader)
        canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)

        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(RadialGradientPage, "radial_gradient", "Radial Gradient"))