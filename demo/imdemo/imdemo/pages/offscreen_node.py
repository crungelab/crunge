import glm

from crunge import imgui

from crunge.engine import RenderOptions, App
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.resource.texture import Texture2D

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2 import Node2D
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.camera_2d import Camera2D
from crunge.demo import Page, PageChannel


class OffscreenNodePage(Page):
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
        self.sprite_vu = SpriteVu(sprite)
        self.node = Node2D(vu=self.sprite_vu).enable()

    def _draw(self):
        imgui.begin(self.title)
        size = self.target_viewport.width, self.target_viewport.height
        imgui.image(imgui.TextureRef(self.texture.id), size)
        imgui.end()

        with self.easel.frame():
            with self.renderer.frame():
                with self.renderer.render_pass():
                    self.draw_node()

        super()._draw()

    def draw_node(self):
        self.node.draw()

def install(app: App):
    app.add_channel(
        PageChannel(OffscreenNodePage, "offscreen_node", "Offscreen Node")
    )
