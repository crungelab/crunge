from loguru import logger
import glm
import numpy as np

from crunge import wgpu
from crunge.wgpu import utils

from crunge import engine
from crunge.engine.imgui import ImGuiView

from .constants import *
from .base import Base
from .scene import Scene
from .scene_renderer import SceneRenderer
from .camera import Camera


# class View(engine.View):
class View(ImGuiView):
    def __init__(self, scene: Scene, width: int, height: int) -> None:
        super().__init__()
        self.scene = scene
        self.width = width
        self.height = height
        self.size = glm.ivec2(width, height)
        self.camera = Camera(width, height)
        self.create_depth_stencil_view()

    def create_depth_stencil_view(self):
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(self.size.x, self.size.y),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )
        self.depth_stencil_view = self.depthTexture.create_view()

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.create_depth_stencil_view()

    def draw(self, renderer: SceneRenderer):
        # logger.debug("View.draw()")

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
                # clear_value=wgpu.Color(.5, .5, .5, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depth_stencil_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        renderer.pass_enc = pass_enc
        renderer.camera = self.camera
        self.scene.draw(renderer)
        pass_enc.end()
        commands = encoder.finish()

        self.device.queue.submit(1, commands)

        super().draw(renderer)
