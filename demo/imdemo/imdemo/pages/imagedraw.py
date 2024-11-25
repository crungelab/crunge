from crunge import imgui
from crunge.imgui import rel

from crunge.engine import Renderer
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from imdemo.page import Page


class ImageDraw(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = ResourceManager().resolve_path(":resources:/robocute.png")
        self.texture = ImageTextureLoader().load(image_path)

    def draw(self, renderer: Renderer):
        imgui.begin("Image example")
        draw_list = imgui.get_window_draw_list()
        pos = rel(0,0)
        pos2 = self.texture.size[0] + pos[0], self.texture.size[1] + pos[1]
        draw_list.add_image(self.texture.id, pos, pos2)
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(ImageDraw, "imagedraw", "Image Draw")
