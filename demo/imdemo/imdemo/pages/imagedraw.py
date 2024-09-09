from crunge import imgui
from crunge.imgui import rel

from imdemo.page import Page


class ImageDraw(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        image_path = window.resource_root / 'robocute.png'
        self.texture = window.ctx.load_texture(image_path, flip=False)

    def draw(self):
        super().draw()
        imgui.begin("Image example")
        draw_list = imgui.get_window_draw_list()
        pos = rel(0,0)
        pos2 = self.texture.size[0] + pos[0], self.texture.size[1] + pos[1]
        draw_list.add_image(self.texture.glo.value, pos, pos2)
        imgui.end()

def install(app):
    app.add_page(ImageDraw, "imagedraw", "Image Draw")
