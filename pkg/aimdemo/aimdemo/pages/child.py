from crunge import imgui

from aimdemo.page import Page


class Child(Page):
    def draw(self):
        imgui.begin("Example: child region")

        #imgui.begin_child("region", (150, -50), border=True)
        imgui.begin_child("region", border=True)
        imgui.text("inside region")
        imgui.end_child()

        imgui.text("outside region")
        imgui.end()

def install(app):
    app.add_page(Child, "child", "Child")
