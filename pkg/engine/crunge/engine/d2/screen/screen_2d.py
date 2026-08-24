from loguru import logger
import glm

from crunge.engine.imgui import ImGuiScreen

from ..renderer.renderer_2d import Renderer2D

from ..camera_2d import Camera2D

from ..overlay.scratch_overlay import ScratchOverlay


class Screen2D(ImGuiScreen):
    def __init__(self) -> None:
        super().__init__()
