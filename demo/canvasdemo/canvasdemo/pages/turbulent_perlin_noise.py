from loguru import logger

from crunge import skia
from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class TurbulentPerlinNoisePage(Page):
    def reset(self):
        self.base_frequency_x = 0.05
        self.base_frequency_y = 0.05
        self.num_octaves = 4
        self.seed = 0.0

    def draw(self, renderer: Renderer):
        imgui.begin("Turbulent Perlin Noise")
        changed, self.base_frequency_x = imgui.drag_float(
            "Base Frequency X",
            self.base_frequency_x,
            0.001,  # step
            0.0,  # min
            1.0,  # max
        )
        changed, self.base_frequency_y = imgui.drag_float(
            "Base Frequency Y",
            self.base_frequency_y,
            0.001,  # step
            0.0,  # min
            1.0,  # max
        )
        changed, self.num_octaves = imgui.drag_int(
            "Number of Octaves", self.num_octaves, 1, 1, 10
        )
        changed, self.seed = imgui.drag_float("Seed", self.seed, 0.01, 0.0, 1.0)
        if imgui.button("Reset"):
            self.reset()
        imgui.end()

        with renderer.canvas_target() as canvas:
            gradient_paint = skia.Paint()

            # shader = skia.PerlinNoiseShader.make_turbulence(0.05, 0.05, 4, 0.0)
            shader = skia.PerlinNoiseShader.make_turbulence(
                self.base_frequency_x,
                self.base_frequency_y,
                self.num_octaves,
                self.seed,
            )

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            # canvas.draw_paint(paint)
        super().draw(renderer)


def install(app: App):
    app.add_channel(
        PageChannel(
            TurbulentPerlinNoisePage, "turbulent_perlin_noise", "Turbulent Perlin Noise"
        )
    )
