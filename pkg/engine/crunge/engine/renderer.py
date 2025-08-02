from typing import TYPE_CHECKING, List
from typing import Optional

import contextlib
from contextvars import ContextVar

from loguru import logger

from crunge import wgpu
from crunge import skia

from .base import Base
from .viewport import Viewport

if TYPE_CHECKING:
    from .d2.camera_2d import Camera2D
    from .d3.camera_3d import Camera3D
    from .d3.lighting_3d import Lighting3D

from .render_pass import RenderPass, DefaultRenderPass

renderer: ContextVar[Optional["Renderer"]] = ContextVar("renderer", default=None)

class Renderer(Base):
    def __init__(
        self,
        viewport: Viewport,
        camera_2d: "Camera2D" = None,
        camera_3d: "Camera3D" = None,
        lighting_3d: "Lighting3D" = None,
    ) -> None:
        super().__init__()
        self.viewport = viewport
        if camera_2d is not None:
            camera_2d.viewport = viewport
            camera_2d.enable()
        elif camera_3d is not None:
            camera_3d.viewport = viewport
            camera_3d.enable()
        self.camera_2d = camera_2d
        self.camera_3d = camera_3d
        self.lighting_3d = lighting_3d

        #self.render_passes: List[RenderPass] = []
        self.render_passes: List[RenderPass] = [DefaultRenderPass(viewport)]
        self.render_pass: RenderPass = None
        self.render_pass_queue: List[RenderPass] = []
        self.first_pass = True
        self.encoder: wgpu.CommandEncoder = None

    @property
    def pass_enc(self) -> wgpu.RenderPassEncoder:
        if not self.render_pass:
            raise RuntimeError("No render pass has been started.")
        return self.render_pass.pass_enc

    @property
    def canvas(self) -> skia.Canvas:
        return self.viewport.canvas

    def __enter__(self):
        self.make_current()
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.first_pass = False
        self.end()
        command_buffer = self.encoder.finish()
        self.queue.submit([command_buffer])

    def make_current(self):
        """Make the renderer current for the current context."""
        global renderer
        renderer.set(self)

    @classmethod
    def get_current(cls) -> Optional["Renderer"]:
        """Get the current renderer."""
        return renderer.get()
    
    def queue_render_pass(self, render_pass: RenderPass):
        """Queue a render pass to be executed later."""
        self.render_pass_queue.append(render_pass)

    def dequeue_render_pass(self) -> Optional[RenderPass]:
        """Dequeue a render pass from the queue."""
        if self.render_pass_queue:
            return self.render_pass_queue.pop(0)
        return None

    def begin(self):
        self.first_pass = True
        self.render_pass_queue = self.render_passes.copy()
        self.render_pass = self.dequeue_render_pass()
        self.encoder = self.device.create_command_encoder()

        self.begin_pass()

    def begin_pass(self):
        self.render_pass.begin(self.encoder)
        if self.camera_2d is not None:
            self.camera_2d.bind(self.pass_enc)
        elif self.camera_3d is not None:
            self.camera_3d.bind(self.pass_enc)

        if self.lighting_3d is not None:
            self.lighting_3d.bind(self.pass_enc)


    def end(self):
        self.end_pass()
        while (render_pass := self.dequeue_render_pass()) is not None:
            self.render_pass = render_pass
            self.begin_pass()
            self.end_pass()

    def end_pass(self):
        self.render_pass.end(self.encoder)

    @contextlib.contextmanager
    def canvas_target(self):
        yield self.viewport.canvas
        self.viewport.submit_canvas()

    '''
    @contextlib.contextmanager
    def canvas_target(self):
        yield self.viewport.canvas
        recording = self.viewport.recorder.snap()
        if recording:
            insert_info = skia.InsertRecordingInfo()
            insert_info.f_recording = recording
            self.viewport.skia_context.insert_recording(insert_info)
            self.viewport.skia_context.submit(skia.SyncToCpu.K_NO)
            #self.skia_context.submit(skia.SyncToCpu.K_YES)
    '''