from loguru import logger

from crunge.engine.imgui import ImGuiScreen


class Screen2D(ImGuiScreen):
    def __init__(self) -> None:
        super().__init__()
