import glm

from crunge import imgui

from crunge.engine import RenderOptions, App, RenderFrame
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.resource.texture import Texture2D

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.camera_2d import Camera2D
from crunge.demo import Page, PageChannel


class OffscreenSpritePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        easel_size = glm.ivec2(256, 256)
        render_options = RenderOptions(use_depth_stencil=True)
        self.easel = OffscreenEasel(easel_size, render_options=render_options)
        self.target_viewport = Viewport(self.easel)
        self.texture = Texture2D(self.easel.color_texture, easel_size)
        ResourceManager().texture_kit.add(self.texture)

        self.camera = Camera2D()
        self.renderer = Renderer2D(self.target_viewport, camera=self.camera)

        sprite = self.sprite = SpriteLoader().load("${resources}/robocute.png")
        self.sprite_vu = SpriteVu(sprite).enable()
        self.sprite_vu.update_transform(
            position=glm.vec3(0, 0, 0),
            size=sprite.size,
            rotation=0.0,
            scale=glm.vec3(1, 1, 1),
            depth=0.0
        )

    def _draw(self):
        with self.easel.frame():
            encoder = self.device.create_command_encoder()
            frame = RenderFrame(self.easel, encoder)
            with frame.use():
                with self.renderer.render_pass():
                    self.draw_sprite()
            self.queue.submit([encoder.finish()])

        imgui.begin(self.title)
        size = self.target_viewport.width, self.target_viewport.height
        imgui.image(imgui.TextureRef(self.texture.id), size)
        imgui.end()

        super()._draw()

    """
    def _draw(self):
        imgui.begin(self.title)
        size = self.target_viewport.width, self.target_viewport.height
        imgui.image(imgui.TextureRef(self.texture.id), size)
        imgui.end()

        with self.easel.frame():
            with self.renderer.frame():
                with self.renderer.render_pass():
                    self.draw_sprite()

        super()._draw()
    """

    def draw_sprite(self):
        self.sprite_vu.draw()

def install(app: App):
    app.add_channel(
        PageChannel(OffscreenSpritePage, "offscreen_sprite", "Offscreen Sprite")
    )
