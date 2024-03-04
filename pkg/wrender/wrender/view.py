from loguru import logger
import glm
import numpy as np

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge import engine
from crunge.engine.imgui import ImGuiView

from .constants import *
from .base import Base
from .scene import Scene
from .scene_renderer import SceneRenderer
from .camera import Camera

#class View(engine.View):
class View(ImGuiView):
    def __init__(self, scene: Scene, width: int, height: int) -> None:
        super().__init__()
        self.scene = scene
        self.width = width
        self.height = height
        self.camera = Camera(width, height)

        self.depth_texture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(width, height),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

    def draw(self, renderer: SceneRenderer):
        #logger.debug("View.draw()")

        attachment = wgpu.RenderPassColorAttachment(
            view=renderer.texture_view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
            #clear_value=wgpu.Color(.5, .5, .5, 1),
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

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        renderer.pass_enc = pass_enc
        renderer.camera = self.camera
        self.scene.draw(renderer)
        pass_enc.end()
        commands = encoder.finish()

        self.device.queue.submit(1, commands)

        super().draw(renderer)
