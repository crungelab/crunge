from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Tooltip(Page):
    def _draw(self):
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
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Tooltip, "tooltip", "Tooltip"))
