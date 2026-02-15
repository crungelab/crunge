from typing import TYPE_CHECKING, List
import contextlib


from loguru import logger

from crunge import wgpu

from ...viewport import Viewport
from ...renderer.render_pass import RenderPass

if TYPE_CHECKING:
    from .renderer_2d import Renderer2D

class RenderPass2D(RenderPass["Renderer2D"]):
    def __init__(self, viewport: Viewport, first: bool = False) -> None:
        super().__init__(viewport=viewport, first=first)

    def begin(self, encoder: wgpu.CommandEncoder):
        if self.viewport.render_options.use_msaa:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.viewport.msaa_texture_view,
                    resolve_target=self.viewport.color_texture_view,
                    #load_op=wgpu.LoadOp.CLEAR,
                    load_op=wgpu.LoadOp.CLEAR if self.first else wgpu.LoadOp.LOAD,
                    #load_op=wgpu.LoadOp.LOAD,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]
        else:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.viewport.color_texture_view,
                    #load_op=wgpu.LoadOp.CLEAR,
                    load_op=wgpu.LoadOp.CLEAR if self.first else wgpu.LoadOp.LOAD,
                    #load_op=wgpu.LoadOp.LOAD,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=self.viewport.depth_stencil_texture_view,
            #depth_load_op=wgpu.LoadOp.CLEAR,
            depth_load_op=wgpu.LoadOp.CLEAR if self.first else wgpu.LoadOp.LOAD,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        self.pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(
            renderpass
        )
