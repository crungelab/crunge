from typing import TYPE_CHECKING


from loguru import logger

from crunge import wgpu

from ...easel import Easel
from ...renderer.render_pass import RenderPass

if TYPE_CHECKING:
    from .renderer_2d import Renderer2D


class RenderPass2D(RenderPass["Renderer2D"]):
    def __init__(self, easel: Easel, clear: bool = False) -> None:
        super().__init__(easel=easel, clear=clear)

    def begin(self, encoder: wgpu.CommandEncoder):
        # logger.debug(f"clear={self.clear}")
        # load_op=wgpu.LoadOp.CLEAR
        # load_op = wgpu.LoadOp.LOAD
        load_op = wgpu.LoadOp.CLEAR if self.clear else wgpu.LoadOp.LOAD
        clear_value = wgpu.Color(0, 0, 0, 1)
        # clear_value = wgpu.Color(0.1, 0.1, 0.1, 1)

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

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=self.easel.depth_stencil_texture_view,
            # depth_load_op=wgpu.LoadOp.CLEAR if self.first else wgpu.LoadOp.LOAD,
            depth_load_op=load_op,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        self.pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
