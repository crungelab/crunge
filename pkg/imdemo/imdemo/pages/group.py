from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Group(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: item groups")

        imgui.begin_group()
        imgui.text("First group (buttons):")
        imgui.button("Button A")
        imgui.button("Button B")
        imgui.end_group()

        imgui.same_line(spacing=50)

        imgui.begin_group()
        imgui.text("Second group (text and bullet texts):")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet B")
        imgui.end_group()

        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Group, "group", "Group")
