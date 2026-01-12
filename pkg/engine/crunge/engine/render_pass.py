from typing import TYPE_CHECKING, List
from typing import Generic, TypeVar, Optional

import contextlib

from loguru import logger

from crunge import wgpu

from .base import Base
from .viewport import Viewport

if TYPE_CHECKING:
    from .renderer import Renderer

T = TypeVar("T", bound="Renderer")

class RenderPass(Generic[T], Base):
    def __init__(self, viewport: Viewport, first: bool = False) -> None:
        super().__init__()
        self.viewport = viewport
        self.first = first
        self.pass_enc: wgpu.RenderPassEncoder = None

    def begin(self, encoder: wgpu.CommandEncoder):
        raise NotImplementedError("Subclasses must implement the begin method.")

    def end(self, encoder: wgpu.CommandEncoder):
        self.pass_enc.end()


class DefaultRenderPass(RenderPass["Renderer"]):
    def __init__(self, viewport: Viewport) -> None:
        super().__init__(viewport, first=True)

    def begin(self, encoder: wgpu.CommandEncoder):
        if self.viewport.render_options.use_msaa:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.viewport.msaa_texture_view,
                    resolve_target=self.viewport.color_texture_view,
                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]
        else:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.viewport.color_texture_view,
                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]
        '''
        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=self.viewport.depth_stencil_texture_view,
            #depth_load_op=wgpu.LoadOp.CLEAR,
            depth_load_op=wgpu.LoadOp.CLEAR if self.first else wgpu.LoadOp.LOAD,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )
        '''

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            #depth_stencil_attachment=depth_stencil_attachment,
        )

        self.pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(
            renderpass
        )
