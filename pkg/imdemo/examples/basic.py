from crunge import imgui
from crunge.imgui.impl.ludi import LudiGui

from crunge import engine

class App(ludi.Window):
    def __init__(self):
        super().__init__(800, 600, "Button Example", resizable=True)
        self.gui = LudiGui(self)
        imgui.set_next_window_pos( (16, 32) )
        imgui.set_next_window_size( (512, 512) )

    def draw(self):
        ludi.start_render()

        imgui.new_frame()

        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()

        imgui.end_frame()

        self.gui.render()


app = App()
ludi.run()
