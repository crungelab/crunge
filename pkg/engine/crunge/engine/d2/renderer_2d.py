from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

from loguru import logger

from crunge import wgpu
from ..renderer import Renderer
from ..viewport import Viewport

if TYPE_CHECKING:
    from .camera_2d import Camera2D


class Renderer2D(Renderer):
    def __init__(self, viewport: Viewport, camera: "Camera2D") -> None:
        super().__init__(viewport)
        camera.viewport = viewport
        self.camera = camera
        self.encoder: wgpu.CommandEncoder = None
        self.pass_enc: wgpu.RenderPassEncoder = None

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def begin(self):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=self.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.viewport.depth_stencil_texture_view,
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

        self.encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        self.pass_enc: wgpu.RenderPassEncoder = self.encoder.begin_render_pass(
            renderpass
        )
        self.camera.bind(self.pass_enc)

    def end(self):
        self.pass_enc.end()
        commands = self.encoder.finish()
        self.device.queue.submit(1, commands)
