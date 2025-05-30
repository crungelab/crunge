from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class DrawCallbackPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        def draw_text(draw_list, cmd):
            clip = cmd.clip_rect
            left = clip[0]
            bottom = self.window.height - clip[3]

            #arcade.draw_text("Simple line of text in 20 point", left, bottom, arcade.color.WHITE, 20)

        draw_list = imgui.get_window_draw_list()

        draw_list.add_callback(draw_text, None)

        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(DrawCallbackPage, "drawcallback", "Draw Callback"))
