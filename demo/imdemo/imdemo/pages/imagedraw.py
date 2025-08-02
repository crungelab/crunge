from crunge import imgui
from crunge.imgui import rel

from crunge.engine import Renderer, App
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from crunge.demo import Page, PageChannel


class ImageDraw(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = ResourceManager().resolve_path(":resources:/robocute.png")
        self.texture = ImageTextureLoader().load(image_path)

    def _draw(self):
        imgui.begin("Image Draw")
        draw_list = imgui.get_window_draw_list()
        pos = rel(0,0)
        pos2 = self.texture.size[0] + pos[0], self.texture.size[1] + pos[1]
        draw_list.add_image(self.texture.id, pos, pos2)
        imgui.end()
        super()._draw()


class ImageRoundedDraw(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = ResourceManager().resolve_path(":resources:/robocute.png")
        self.texture = ImageTextureLoader().load(image_path)

    def _draw(self):
        imgui.begin("Image Rounded Draw")
        draw_list = imgui.get_window_draw_list()
        pos = rel(0,0)
        pos2 = self.texture.size[0] + pos[0], self.texture.size[1] + pos[1]
        #draw_list.add_image(self.texture.id, pos, pos2)
        #draw_list.add_image_rounded(texture_id, (20, 35), (180, 80), col=imgui.get_color_u32_rgba(0.5,0.5,1,1), rounding=10)
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_image_rounded(self.texture.id, pos, pos2, (0,0), (1,1), color, rounding=10)
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(ImageDraw, "imagedraw", "Image Draw"))
    app.add_channel(PageChannel(ImageRoundedDraw, "imageroundeddraw", "Image Rounded Draw"))
