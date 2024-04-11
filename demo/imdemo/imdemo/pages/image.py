from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class ImagePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = self.wnd.resource_path / 'robocute.png'
        self.texture = self.gfx.load_texture(image_path)
        self.texture_view = self.texture.create_view()

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        size = self.texture.get_width(), self.texture.get_height()
        imgui.image(self.texture_view, size)
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(ImagePage, "image", "Image")
