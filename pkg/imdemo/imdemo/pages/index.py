from crunge import imgui

from imdemo.page import Page


class Index(Page):
    def draw(self):
        super().draw()
        imgui.begin("Index")

        imgui.text("Welcome to the imgui Demo!")
        
        imgui.end()

def install(app):
    app.add_page(Index, "index", "Index")