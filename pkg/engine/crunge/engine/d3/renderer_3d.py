from typing import TYPE_CHECKING

from crunge import wgpu

from ..renderer import Renderer
from ..viewport import Viewport

if TYPE_CHECKING:
    from .camera_3d import Camera3D

class Renderer3D(Renderer):
    def __init__(self, viewport: Viewport, camera: "Camera3D") -> None:
        super().__init__(viewport)
        camera.viewport = viewport
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera = camera

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def begin(self):
        if self.viewport.use_msaa:
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
                    # clear_value=wgpu.Color(.5, .5, .5, 1),
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

        '''
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
        '''

        self.encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        self.pass_enc: wgpu.RenderPassEncoder = self.encoder.begin_render_pass(
            renderpass
        )
        #self.pass_enc.set_bind_group(0, self.camera.bind_group)
        #self.viewport.camera_adapter.bind(self.pass_enc)
        self.camera.bind(self.pass_enc)

    def end(self):
        self.pass_enc.end()
        commands = self.encoder.finish()
        self.device.queue.submit(1, commands)
