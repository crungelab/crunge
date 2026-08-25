from typing import Optional
import contextlib
from contextvars import ContextVar
from enum import Enum, auto

from loguru import logger

from crunge import wgpu
from crunge import skia

from ..base import Base
from ..easel import Easel

current_render_frame: ContextVar[Optional["RenderFrame"]] = ContextVar(
    "current_render_frame", default=None
)


class DrawApi(Enum):
    NONE = auto()
    GPU = auto()
    CANVAS = auto()


class RenderFrame(Base):
    """Per-frame render state.

    Owns the encoder and the API boundary. Anything that draws declares
    which API it needs; the frame flushes the other one first so that GPU
    execution order matches traversal order.
    """

    def __init__(self, easel: Easel) -> None:
        super().__init__()
        self.easel = easel
        self.cleared = False
        self._api = DrawApi.NONE
        self._encoder: wgpu.CommandEncoder = None

    # -- encoder -----------------------------------------------------

    @property
    def encoder(self) -> wgpu.CommandEncoder:
        if self._encoder is None:
            self._encoder = self.device.create_command_encoder()
        return self._encoder

    def flush_gpu(self) -> None:
        if self._encoder is None:
            return
        self.queue.submit([self._encoder.finish()])
        self._encoder = None

    def flush_canvas(self) -> None:
        self.easel.submit_canvas()

    # -- boundary ----------------------------------------------------

    def require(self, api: DrawApi) -> None:
        """Declare which API is about to draw, flushing the other first."""
        if api is self._api:
            return
        if self._api is DrawApi.GPU:
            self.flush_gpu()
        elif self._api is DrawApi.CANVAS:
            self.flush_canvas()
        self._api = api

    @contextlib.contextmanager
    def gpu(self):
        self.require(DrawApi.GPU)
        yield self.encoder

    @contextlib.contextmanager
    def canvas(self):
        self.require(DrawApi.CANVAS)
        yield self.easel.canvas

    def finish(self) -> None:
        """Flush whatever drew last. Called once by the frame owner."""
        if self._api is DrawApi.GPU:
            self.flush_gpu()
        elif self._api is DrawApi.CANVAS:
            self.flush_canvas()
        self._api = DrawApi.NONE

    # -- context -----------------------------------------------------

    def make_current(self):
        current_render_frame.set(self)

    @classmethod
    def get_current(cls) -> Optional["RenderFrame"]:
        return current_render_frame.get()

    @contextlib.contextmanager
    def use(self):
        token = current_render_frame.set(self)
        try:
            yield self
        finally:
            current_render_frame.reset(token)