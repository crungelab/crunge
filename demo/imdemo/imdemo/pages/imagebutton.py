import random

from crunge.core.utils import as_capsule

from crunge.engine import Renderer
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from crunge import imgui

from imdemo.page import Page

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
        #if imgui.image_button(self.texture.glo.value, self.texture.size):
        #if imgui.image_button("Image Button", self.texture.glo.value, self.texture.size):
        if imgui.image_button("Image Button", self.texture.id, (self.texture.size.x, self.texture.size.y)):
        #if imgui.image_button("Image Button", as_capsule(self.texture.view), self.texture.size):
            self.message = MESSAGES[random.randint(0, len(MESSAGES)-1)]
        imgui.text(self.message)
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(ImageButton, "imagebutton", "Image Button")
