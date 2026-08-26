from typing import TYPE_CHECKING, Optional, Generator

import contextlib
from contextvars import ContextVar

from loguru import logger

from crunge import wgpu
from crunge import skia
from crunge.engine.node import Node

from ..base import Base
from ..viewport import Viewport
from ..easel import Easel
from .. import Composition, DrawApi

if TYPE_CHECKING:
    from ..d2.camera_2d import Camera2D
    from ..d3.camera_3d import Camera3D
    from ..d3.lighting_3d import Lighting3D
    from .task import RenderPlan

from .render_pass import RenderPass, DefaultRenderPass

current_renderer: ContextVar[Optional["Renderer"]] = ContextVar(
    "current_renderer", default=None
)


class Renderer(Base):
    def __init__(
        self,
        viewport: Viewport,
        camera_2d: "Camera2D" = None,
        camera_3d: "Camera3D" = None,
        lighting_3d: "Lighting3D" = None,
        clear: bool = True,
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

        self.plan: "RenderPlan" = None
        self.clear: bool = clear

    @property
    def easel(self) -> Easel:
        return self.viewport.easel

    @property
    def composition(self) -> Composition:
        composition = Composition.get_current()
        if composition is None:
            raise RuntimeError("No composition is current.")
        return composition

    @property
    def pass_enc(self) -> wgpu.RenderPassEncoder:
        if not self.current_render_pass:
            raise RuntimeError("No render pass has been started.")
        return self.current_render_pass.pass_enc

    @property
    def canvas(self) -> skia.Canvas:
        return self.easel.canvas

    @contextlib.contextmanager
    def canvas_target(self):
        with self.composition.canvas() as canvas:
            yield canvas

    def create_render_pass(self, clear: bool) -> RenderPass:
        return DefaultRenderPass(self.easel, clear=clear)

    @classmethod
    def get_current(cls) -> Optional["Renderer"]:
        return current_renderer.get()

    @contextlib.contextmanager
    def use(self):
        token = current_renderer.set(self)
        try:
            yield self
        finally:
            current_renderer.reset(token)

    @contextlib.contextmanager
    def render_pass(
        self, render_pass: RenderPass = None
    ) -> Generator[RenderPass, None, None]:
        with self.use():
            self.begin_pass(render_pass)
            try:
                yield self.current_render_pass
            finally:
                self.end_pass()

    def begin_pass(self, render_pass: RenderPass = None):
        composition = self.composition
        composition.require(DrawApi.GPU)

        if render_pass is not None:
            self.current_render_pass = render_pass
        else:
            clear = self.clear and not composition.cleared
            self.current_render_pass = self.create_render_pass(clear)
            if clear:
                composition.cleared = True

        self.current_render_pass.begin(composition.encoder)
        self.apply_viewport()
        self.bind()

    def apply_viewport(self) -> None:
        easel = self.easel
        r = self.viewport.global_rect
        x = max(0, min(r.x, easel.width))
        y = max(0, min(r.y, easel.height))
        w = max(0, min(r.width, easel.width - x))
        h = max(0, min(r.height, easel.height - y))
        self.pass_enc.set_viewport(x, y, w, h, 0.0, 1.0)
        self.pass_enc.set_scissor_rect(x, y, w, h)

    def bind(self) -> None:
        if self.camera_2d is not None:
            self.camera_2d.bind(self.pass_enc)
        elif self.camera_3d is not None:
            self.camera_3d.bind(self.pass_enc)

        if self.lighting_3d is not None:
            self.lighting_3d.bind(self.pass_enc)

    def end_pass(self):
        self.current_render_pass.end(self.composition.encoder)
        self.current_render_pass = None

    def create_plan(self) -> None:
        pass

    def ensure_plan(self) -> None:
        if self.plan is None:
            self.create_plan()

    def render(self, node: Node = None) -> None:
        self.ensure_plan()
        with self.render_pass():
            node.render()
        self.plan.render()
        self.plan.clear()