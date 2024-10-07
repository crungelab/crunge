from loguru import logger
import glm

from crunge import wgpu
from crunge.wgpu import utils

from crunge.engine.imgui import ImGuiView

from .renderer_2d import Renderer2D
from .camera_2d import Camera2D

from .scratch_layer import ScratchLayer

class View2D(ImGuiView):
    #renderer: Renderer2D = None

    def __init__(self, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scratch: ScratchLayer = None
        #self.depthTexture: wgpu.Texture = None
        #self.depth_stencil_view: wgpu.TextureView = None
        self.camera: Camera2D = None

    def _create(self, window):
        super()._create(window)
        self.scratch = ScratchLayer().create(self)
        self.add_layer(self.scratch)

        #self.create_depth_stencil_view()
        self.create_camera()
        self.create_renderer()

    '''
    def create_depth_stencil_view(self):
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(self.size.x, self.size.y),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )
        self.depth_stencil_view = self.depthTexture.create_view()
    '''

    def on_size(self):
        super().on_size()
        size = self.size
        if self.camera is not None:
            self.camera.size = glm.vec2(size)
        #self.create_depth_stencil_view()
        self.renderer = self.create_renderer()

    '''
    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.camera.size = glm.vec2(size)
        self.create_depth_stencil_view()
        self.renderer = self.create_renderer()
    '''

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer2D(self.camera)
        #self.renderer.depth_stencil_view = self.depth_stencil_view
        return self.renderer

    def draw(self, renderer: Renderer2D):
        # logger.debug("DemoView.draw()")
        #self.renderer.texture_view = renderer.texture_view
        self.renderer.viewport = renderer.viewport
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)

        #super().draw(renderer)
