from typing import TYPE_CHECKING
import contextlib

from loguru import logger

from crunge import wgpu
from crunge import skia

from .base import Base
from .viewport import Viewport

if TYPE_CHECKING:
    from .d2.camera_2d import Camera2D
    from .d3.camera_3d import Camera3D


class Renderer(Base):
    def __init__(
        self,
        viewport: Viewport,
        camera_2d: "Camera2D" = None,
        camera_3d: "Camera3D" = None,
    ) -> None:
        super().__init__()
        self.viewport = viewport
        if camera_2d is not None:
            camera_2d.viewport = viewport
        elif camera_3d is not None:
            camera_3d.viewport = viewport
        self.camera_2d = camera_2d
        self.camera_3d = camera_3d

        self.pass_enc: wgpu.RenderPassEncoder = None

        # Skia
        self.skia_context = skia.create_context(self.gfx.instance, self.gfx.device)
        recorder_options = skia.create_standard_recorder_options()
        self.recorder = self.skia_context.make_recorder(recorder_options)

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()
        return self

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
                )
            ]

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=self.viewport.depth_stencil_texture_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        self.encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        self.pass_enc: wgpu.RenderPassEncoder = self.encoder.begin_render_pass(
            renderpass
        )

        if self.camera_2d is not None:
            self.camera_2d.bind(self.pass_enc)
        elif self.camera_3d is not None:
            self.camera_3d.bind(self.pass_enc)

    def end(self):
        self.pass_enc.end()
        command_buffer = self.encoder.finish()
        self.queue.submit([command_buffer])

    @contextlib.contextmanager
    def canvas_target(self):
        target = self.viewport.color_texture
        skia_surface = skia.create_surface(target, self.recorder)
        canvas = skia_surface.get_canvas()
        yield canvas
        recording = self.recorder.snap()
        if recording:
            insert_info = skia.InsertRecordingInfo()
            insert_info.f_recording = recording
            self.skia_context.insert_recording(insert_info)
            #self.skia_context.submit(skia.SyncToCpu.K_NO)
            self.skia_context.submit(skia.SyncToCpu.K_YES)
