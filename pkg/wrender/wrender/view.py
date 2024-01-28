from loguru import logger
import glm
import numpy as np

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge import shell
from crunge.shell.imgui import ImGuiView

from .constants import *
from .base import Base
from .scene import Scene
from .camera import Camera

#class View(shell.View):
class View(ImGuiView):
    def __init__(self, scene: Scene, width: int, height: int) -> None:
        super().__init__()
        self.scene = scene
        self.width = width
        self.height = height
        self.camera = Camera(width, height)

        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(width, height),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

    def draw(self):
        #logger.debug("View.draw()")

        attachment = wgpu.RenderPassColorAttachment(
            view=self.ctx.texture_view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
            #clear_value=wgpu.Color(.5, .5, .5, 1),
        )

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depthTexture.create_view(),
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
        self.scene.draw(self.camera, pass_enc)
        pass_enc.end()
        commands = encoder.finish()

        self.device.queue.submit(1, commands)
        #exit()
