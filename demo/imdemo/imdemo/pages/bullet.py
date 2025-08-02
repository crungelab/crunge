from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Bullet(Page):
    def _draw(self):
        imgui.begin(self.title)
        for i in range(10):
            imgui.bullet()
        imgui.end()
        super()._draw()


class BulletText(Page):
    def _draw(self):
        imgui.begin(self.title)
        imgui.bullet_text("Bullet 1")
        imgui.bullet_text("Bullet 2")
        imgui.bullet_text("Bullet 3")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Bullet, "bullet", "Bullets"))
    app.add_channel(PageChannel(BulletText, "bullettext", "Bullets with Text"))