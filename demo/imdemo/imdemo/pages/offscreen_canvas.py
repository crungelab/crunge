import glm

from crunge import imgui
from crunge import skia

from crunge.engine import App, colors
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.resource.texture import Texture2D

from crunge.demo import Page, PageChannel


class OffscreenCanvasPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        self.color_1 = colors.BLUE
        self.color_2 = colors.YELLOW

        easel_size = glm.ivec2(512, 256)
        self.easel = OffscreenEasel(easel_size)

        self.target_viewport = Viewport(self.easel)
        self.texture = Texture2D(
            self.easel.color_texture, easel_size
        )
        ResourceManager().texture_kit.add(self.texture)

    def _draw(self):
        imgui.begin(self.title)
        size = self.target_viewport.width, self.target_viewport.height
        imgui.image(imgui.TextureRef(self.texture.id), size)
        imgui.end()

        with self.easel.frame():
            self.draw_radial_gradient()

        super()._draw()

    def draw_radial_gradient(self):
        canvas = self.easel.canvas

        gradient_paint = skia.Paint()

        shader = skia.Shader.create_radial_gradient(
            skia.Point(128.0, 128.0),
            180.0,
            [skia.Color4f(*self.color_1), skia.Color4f(*self.color_2)],
        )

        gradient_paint.set_shader(shader)
        canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)

        self.easel.submit_canvas()


def install(app: App):
    app.add_channel(
        PageChannel(OffscreenCanvasPage, "offscreen_canvas", "Offscreen Canvas")
    )
