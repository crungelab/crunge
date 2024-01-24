from crunge import imgui

from imdemo.page import Page


class Child(Page):
    def draw(self):
        super().draw()
        imgui.begin("Example: child region")

        #imgui.begin_child("region", (150, -50), border=True)
        imgui.begin_child("region", border=True)
        imgui.text("inside region")
        imgui.end_child()

        imgui.text("outside region")
        imgui.end()

def install(app):
    app.add_page(Child, "child", "Child")
