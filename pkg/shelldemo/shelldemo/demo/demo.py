import sys, time
from loguru import logger


from crunge import as_capsule

from crunge import sdl
from crunge import shell

from crunge import wgpu, imgui
import crunge.wgpu.utils as utils

from .demo_view import DemoView

class Demo(shell.App):
    kWidth = 1024
    kHeight = 768

    def __init__(self, view=DemoView()):
        super().__init__(
            self.kWidth,
            self.kHeight,
            self.__class__.__name__,
            view=view,
            resizable=True,
        )

    def draw(self):
        super().draw()
        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()
