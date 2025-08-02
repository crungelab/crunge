import glm

from crunge import imgui
from crunge import skia

from crunge.engine import Renderer, App
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.viewport.offscreen_viewport import OffscreenViewport
from crunge.engine.resource.texture import Texture2D
from crunge.engine.color import rgba_tuple_to_argb_int
from crunge.engine import colors

from crunge.demo import Page, PageChannel


class OffscreenPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        self.color_1 = colors.BLUE
        self.color_2 = colors.YELLOW

        self.viewport_size = glm.ivec2(512, 256)
        self.viewport = OffscreenViewport(self.viewport_size)
        self.texture = Texture2D(
            self.viewport.color_texture,
            self.viewport_size
        )
        ResourceManager().texture_kit.add(self.texture)
        self.renderer = Renderer(self.viewport)

    def _draw(self):
        imgui.begin(self.title)
        size = self.viewport.width, self.viewport.height
        imgui.image(self.texture.id, size)
        imgui.end()

        with self.viewport:
            self.draw_radial_gradient()

        super()._draw()

    def draw_radial_gradient(self):
        #renderer = Renderer.get_current()
        renderer = self.renderer
        canvas = renderer.canvas

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

        renderer.viewport.submit_canvas()

def install(app: App):
    app.add_channel(PageChannel(OffscreenPage, "offscreen", "Offscreen"))
