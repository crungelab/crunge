from loguru import logger

from crunge.engine.imgui import ImGuiView

class DemoView(ImGuiView):
    def __init__(self, layers=[]):
        super().__init__(layers=layers)
