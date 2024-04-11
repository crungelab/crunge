from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Tooltip(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: tooltip")
        imgui.button("Click me!")
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.text("This button is clickable.")
            imgui.text("This button has full window tooltip.")
            tex_id = imgui.get_io().fonts.tex_id
            imgui.image(tex_id, (512, 64), border_col=(1, 0, 0, 1))
            imgui.end_tooltip()
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Tooltip, "tooltip", "Tooltip")
