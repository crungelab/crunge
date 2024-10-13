from loguru import logger
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine.imgui import ImGuiView

from ..math import Size2i
from .scene_2d import Scene2D
from .renderer_2d import Renderer2D
from .camera_2d import Camera2D
from .view_2d import View2D

class SceneView2D(View2D):
    renderer: Renderer2D = None

    def __init__(self, scene: Scene2D, size=Size2i()) -> None:
        super().__init__(size)
        self.scene = scene
