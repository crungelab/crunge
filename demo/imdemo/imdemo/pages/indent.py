from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Indent(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: item indenting")

        imgui.text("Some text with bullets:")

        imgui.bullet_text("Bullet A")
        imgui.indent()
        imgui.bullet_text("Bullet B (first indented)")
        imgui.bullet_text("Bullet C (indent continues)")
        imgui.unindent()
        imgui.bullet_text("Bullet D (indent cleared)")

        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Indent, "indent", "Indent")

