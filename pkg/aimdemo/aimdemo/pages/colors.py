from crunge import imgui

from aimdemo.page import Page


class ColorsPage(Page):
    def draw(self):
        style = imgui.get_style()
        
        imgui.begin("Colors")
        imgui.columns(4)
        for color in range(0, imgui.COL_COUNT):
            imgui.text(f"Color: {color}")
            imgui.color_button(f"color#{color}", style.colors[color])
            imgui.next_column()

        imgui.end()

def install(app):
    app.add_page(ColorsPage, "colors", "Colors")
