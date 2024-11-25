from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader


from imdemo.page import Page


class ImagePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = ResourceManager().resolve_path(":resources:/robocute.png")
        self.texture = ImageTextureLoader().load(image_path)

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        size = self.texture.width, self.texture.height
        imgui.image(self.texture.id, size)
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(ImagePage, "image", "Image")
