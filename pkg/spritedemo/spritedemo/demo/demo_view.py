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

class DemoView(ImGuiView):
#class DemoView(engine.View):
    def __init__(self, scene: Scene, width: int, height: int) -> None:
        super().__init__()
        self.scene = scene
        self.width = width
        self.height = height
        
        self.create_camera()

        self.depth_texture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(width, height),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

    def create_camera(self):
        self.camera = Camera2D(glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height))

    def draw(self, renderer: SceneRenderer):
        #logger.debug("View.draw()")

        attachment = wgpu.RenderPassColorAttachment(
            view=renderer.texture_view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
        )

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depth_texture.create_view(),
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=attachment,
            depth_stencil_attachment=depthStencilAttach,
        )

        commands = wgpu.CommandBuffer()
        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        renderer.pass_enc = pass_enc
        renderer.camera = self.camera
        self.scene.draw(renderer)
        pass_enc.end()
        commands = encoder.finish()

        self.device.queue.submit(1, commands)

        super().draw(renderer)
