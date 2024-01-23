from crunge import imgui
from crunge.imgui.impl.arcade import ArcadeGui

import arcade

class App(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Button Example", resizable=True)
        self.gui = ArcadeGui(self)
        imgui.set_next_window_pos( (16, 32) )
        imgui.set_next_window_size( (512, 512) )

    def on_draw(self):
        arcade.start_render()

        imgui.new_frame()

        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()

        imgui.end_frame()

        self.gui.render()


app = App()
arcade.run()
