from loguru import logger

from crunge.shell.imgui import ImGuiView

class DemoView(ImGuiView):
    def __init__(self, layers=[]):
        super().__init__(layers=layers)

    def create(self, window):
        super().create(window)
        return self