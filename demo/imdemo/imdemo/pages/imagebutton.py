import random

from crunge.engine import Renderer
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from crunge import imgui

from ..app import App
from ..page import Page, PageChannel


MESSAGES = [
    "Hey! That tickles!!!",
    "Cut it out!",
    "Wise guy.",
    "Oh no you didn't"
]

class ImageButton(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = ResourceManager().resolve_path(":resources:/robocute.png")
        self.texture = ImageTextureLoader().load(image_path)
        self.message = ''

    def draw(self, renderer: Renderer):
        imgui.begin("Image Button")
        if imgui.image_button("Image Button", self.texture.id, (self.texture.size.x, self.texture.size.y)):
            self.message = MESSAGES[random.randint(0, len(MESSAGES)-1)]
        imgui.text(self.message)
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(ImageButton, "imagebutton", "Image Button")
    app.add_channel(PageChannel(ImageButton, "imagebutton", "Image Button"))
