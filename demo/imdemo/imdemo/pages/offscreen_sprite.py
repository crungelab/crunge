import glm

from crunge import imgui
from crunge import skia

from crunge.engine import Renderer, RenderOptions, App
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.viewport.offscreen_viewport import OffscreenViewport
from crunge.engine.resource.texture import Texture2D
from crunge.engine.color import rgba_tuple_to_argb_int
from crunge.engine import colors

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2.renderer_2d import Renderer2D
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.camera_2d import Camera2D
from crunge.demo import Page, PageChannel


class OffscreenSpritePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        self.viewport_size = glm.ivec2(256, 256)
        render_options = RenderOptions(use_depth_stencil=True)
        self.viewport = OffscreenViewport(self.viewport_size, render_options=render_options)
        self.texture = Texture2D(self.viewport.color_texture, self.viewport_size)
        ResourceManager().texture_kit.add(self.texture)

        self.camera = Camera2D()
        self.renderer = Renderer2D(self.viewport, camera=self.camera)

        sprite = self.sprite = SpriteLoader().load(":resources:/robocute.png")
        self.sprite_vu = SpriteVu(sprite).enable()
        self.sprite_vu.update_transform(
            position=glm.vec3(0, 0, 0),
            size=sprite.rect.size,
            rotation=0.0,
            scale=glm.vec3(1, 1, 1),
            depth=0.0
        )

    def _draw(self):
        imgui.begin(self.title)
        size = self.viewport.width, self.viewport.height
        imgui.image(self.texture.id, size)
        imgui.end()

        with self.viewport:
            with self.renderer.render():
                self.draw_sprite()

        super()._draw()

    def draw_sprite(self):
        self.sprite_vu.draw()

def install(app: App):
    app.add_channel(
        PageChannel(OffscreenSpritePage, "offscreen_sprite", "Offscreen Sprite")
    )
