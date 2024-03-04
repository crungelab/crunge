from loguru import logger
import glm
import numpy as np

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge import engine
from crunge.engine.imgui import ImGuiView

from ..constants import *
from ..scene import Scene
from ..scene_renderer import SceneRenderer
from ..camera_2d import Camera2D

#class DemoView(engine.View):

class DemoView(ImGuiView):    
    renderer: SceneRenderer = None
    def __init__(self, scene: Scene, width: int, height: int) -> None:
        super().__init__()
        self.scene = scene
        self.width = width
        self.height = height
        
        self.depth_texture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(width, height),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

        self.create_camera()
        self.create_renderer()


    def create_camera(self):
        self.camera = Camera2D(glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height))

    def create_renderer(self):
        self.renderer = SceneRenderer()
        self.renderer.depth_stencil_view = self.depth_texture.create_view()
        self.renderer.camera = self.camera

    def draw(self, renderer: SceneRenderer):
        #logger.debug("DemoView.draw()")
        self.renderer.texture_view = renderer.texture_view
        with self.renderer:
            self.scene.draw(self.renderer)

        super().draw(renderer)
