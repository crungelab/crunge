from typing import TYPE_CHECKING, List
from typing import Generic, TypeVar, Optional

import contextlib

from loguru import logger

from crunge import wgpu

from ..base import Base
from ..easel import Easel

if TYPE_CHECKING:
    from . import Renderer

T = TypeVar("T", bound="Renderer")

class RenderPass(Generic[T], Base):
    def __init__(self, easel: Easel, clear: bool = False) -> None:
        super().__init__()
        self.easel = easel
        self.clear = clear
        self.pass_enc: wgpu.RenderPassEncoder = None

    def begin(self, encoder: wgpu.CommandEncoder):
        raise NotImplementedError("Subclasses must implement the begin method.")

    def end(self, encoder: wgpu.CommandEncoder):
        self.pass_enc.end()


class DefaultRenderPass(RenderPass["Renderer"]):
    def __init__(self, easel: Easel, clear: bool = False) -> None:
        super().__init__(easel, clear=clear)

    def begin(self, encoder: wgpu.CommandEncoder):
        load_op = wgpu.LoadOp.CLEAR if self.clear else wgpu.LoadOp.LOAD
        clear_value = wgpu.Color(0, 0, 0, 1)

        if self.easel.render_options.use_msaa:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.easel.msaa_texture_view,
                    resolve_target=self.easel.color_texture_view,
                    load_op=load_op,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=clear_value,
                )
            ]
        else:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.easel.color_texture_view,
                    load_op=load_op,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=clear_value,
                )
            ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        self.pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)

"""
class DefaultRenderPass(RenderPass["Renderer"]):
    def __init__(self, easel: Easel, clear: bool = False) -> None:
        super().__init__(easel=easel, clear=clear)

    def begin(self, encoder: wgpu.CommandEncoder):
        if self.easel.render_options.use_msaa:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.easel.msaa_texture_view,
                    resolve_target=self.easel.color_texture_view,
                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]
        else:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=self.easel.color_texture_view,
                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        self.pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(
            renderpass
        )
"""