import arcade
from crunge import imgui
from crunge import imgui

from imgui.renderers.arcade import ArcadeRenderer

class MyGui:
    def __init__(self, window):
        self.window = window
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def draw(self):
        imgui.new_frame()

        imgui.set_next_window_pos( (16, 32) )
        imgui.set_next_window_size( (512, 512) )

        imgui.begin("Example: bullets")

        for i in range(10):
            imgui.bullet()

        imgui.end()

        imgui.end_frame()

        imgui.render()

        self.renderer.render(imgui.get_draw_data())


class App(arcade.Window):
    def __init__(self):
        super().__init__(1024, 768, "Test Render")
        self.gui = MyGui(self)

    def on_draw(self):
        arcade.start_render()
        self.gui.render()


def test_render():
    app = App()
    app.on_draw()