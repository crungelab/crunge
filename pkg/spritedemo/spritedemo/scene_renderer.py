from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .camera_2d import Camera2D

from crunge import wgpu, engine

#from .camera_2d import Camera2D

class SceneRenderer(engine.Renderer):
    def __init__(self) -> None:
        super().__init__()
        self.encoder: wgpu.CommandEncoder = None
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera: "Camera2D" = None

    def __enter__(self):
        self.begin()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def begin(self):
        attachment = wgpu.RenderPassColorAttachment(
            view=self.texture_view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
        )

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depth_stencil_view,
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

        self.encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        self.pass_enc: wgpu.RenderPassEncoder = self.encoder.begin_render_pass(renderpass)

    def end(self):
        self.pass_enc.end()
        commands = self.encoder.finish()
        self.device.queue.submit(1, commands)
