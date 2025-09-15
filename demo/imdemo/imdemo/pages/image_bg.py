from crunge import imgui

from crunge.engine import Renderer, App
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader


from crunge.demo import Page, PageChannel


class ImageBgPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = ResourceManager().resolve_path(":resources:/robocute.png")
        self.texture = ImageTextureLoader().load(image_path)

    def _draw(self):
        imgui.begin(self.title)
        size = self.texture.width, self.texture.height
        imgui.image_with_bg(imgui.TextureRef(self.texture.id), size, bg_col=(0.2, 0.2, 0.2, 1), tint_col=(1, 0, 1, 1))
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(ImageBgPage, "image_bg", "Image with Background"))
