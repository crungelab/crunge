from typing import TYPE_CHECKING, Generator
from typing import Optional

import contextlib
from contextvars import ContextVar

from loguru import logger

from crunge import wgpu
from crunge import skia
from crunge.engine.node import Node

from ..base import Base
from ..viewport import Viewport

if TYPE_CHECKING:
    from ..d2.camera_2d import Camera2D
    from ..d3.camera_3d import Camera3D
    from ..d3.lighting_3d import Lighting3D
    from .task import RenderPlan

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

        self.current_render_pass: RenderPass = None
        self.encoder: wgpu.CommandEncoder = None

        self.plan: "RenderPlan" = None

    @property
    def pass_enc(self) -> wgpu.RenderPassEncoder:
        if not self.current_render_pass:
            raise RuntimeError("No render pass has been started.")
        return self.current_render_pass.pass_enc

    @property
    def canvas(self) -> skia.Canvas:
        return self.viewport.canvas

    @contextlib.contextmanager
    def canvas_target(self):
        yield self.viewport.canvas
        self.viewport.submit_canvas()

    def create_render_pass(self):
        return DefaultRenderPass(self.viewport)

    def make_current(self):
        renderer.set(self)

    @classmethod
    def get_current(cls) -> Optional["Renderer"]:
        return renderer.get()

    @contextlib.contextmanager
    def use(self):
        prev_renderer = self.get_current()
        self.make_current()
        yield self
        if prev_renderer is not None:
            prev_renderer.make_current()

    @contextlib.contextmanager
    def frame(self):
        with self.use():
            self.encoder = self.device.create_command_encoder()
            yield self
            command_buffer = self.encoder.finish()
            self.queue.submit([command_buffer])

    @contextlib.contextmanager
    def render_pass(
        self, render_pass: RenderPass = None
    ) -> Generator[RenderPass, None, None]:
        with self.use():
            self.begin_pass(render_pass)
            yield self.current_render_pass
            self.end_pass()

    def begin_pass(self, render_pass: RenderPass = None):
        if render_pass is not None:
            self.current_render_pass = render_pass
        else:
            self.current_render_pass = self.create_render_pass()

        self.current_render_pass.begin(self.encoder)

        if self.camera_2d is not None:
            self.camera_2d.bind(self.pass_enc)
        elif self.camera_3d is not None:
            self.camera_3d.bind(self.pass_enc)

        if self.lighting_3d is not None:
            self.lighting_3d.bind(self.pass_enc)

    def end_pass(self):
        self.current_render_pass.end(self.encoder)

    def create_plan(self) -> None:
        pass

    def ensure_plan(self) -> None:
        if self.plan is None:
            self.create_plan()

    def render(self, node: Node = None) -> None:
        self.ensure_plan()
        with self.render_pass():
            #node.render()
            node.root_render()
        self.plan.render()
        self.plan.clear()

    """
    def render(self, node: Node = None) -> None:
        self.ensure_plan()
        with self.frame():
            with self.render_pass():
                #node.render()
                node.root_render()
            self.plan.render()
        self.plan.clear()
    """