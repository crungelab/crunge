from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class ColorsPage(Page):
    def draw(self, renderer: Renderer):
        style = imgui.get_style()
        
        imgui.begin("Colors")
        imgui.columns(4)
        for color in range(0, imgui.Col.COUNT):
            imgui.text(f"Color: {color}")
            imgui.color_button(f"color#{color}", style.colors[color])
            imgui.next_column()

        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(ColorsPage, "colors", "Colors"))
