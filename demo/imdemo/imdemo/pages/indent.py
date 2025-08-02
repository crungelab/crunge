from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Indent(Page):
    def _draw(self):
        imgui.begin("Example: item indenting")

        imgui.text("Some text with bullets:")

        imgui.bullet_text("Bullet A")
        imgui.indent()
        imgui.bullet_text("Bullet B (first indented)")
        imgui.bullet_text("Bullet C (indent continues)")
        imgui.unindent()
        imgui.bullet_text("Bullet D (indent cleared)")

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Indent, "indent", "Indent"))
