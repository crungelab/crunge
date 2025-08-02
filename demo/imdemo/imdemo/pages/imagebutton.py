import random

from crunge.engine import Renderer, App
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from crunge import imgui
from crunge.demo import Page, PageChannel


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

    def _draw(self):
        imgui.begin("Image Button")
        if imgui.image_button("Image Button", self.texture.id, (self.texture.size.x, self.texture.size.y)):
            self.message = MESSAGES[random.randint(0, len(MESSAGES)-1)]
        imgui.text(self.message)
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(ImageButton, "imagebutton", "Image Button"))
