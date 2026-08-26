from typing import Optional
import contextlib
from contextvars import ContextVar
from enum import Enum, auto

from loguru import logger

from crunge import wgpu
from crunge import skia

from .base import Base
from .easel import Easel

current_composition: ContextVar[Optional["Composition"]] = ContextVar(
    "current_composition", default=None
)


class DrawApi(Enum):
    NONE = auto()
    GPU = auto()
    CANVAS = auto()


class Composition(Base):
    """Assembles one frame's drawing onto an Easel.

    Owns the command encoder and the API boundary. Anything that draws
    declares which API it needs; the composition flushes the other one
    first, so GPU execution order matches traversal order.
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
        if self._api is not DrawApi.GPU:
            raise RuntimeError("Encoder accessed outside a gpu() scope.")
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
        """Flush whatever drew last. Called once by the owner."""
        if self._api is DrawApi.GPU:
            self.flush_gpu()
        elif self._api is DrawApi.CANVAS:
            self.flush_canvas()
        self._api = DrawApi.NONE

    # -- context -----------------------------------------------------

    @classmethod
    def get_current(cls) -> Optional["Composition"]:
        return current_composition.get()

    @contextlib.contextmanager
    def use(self):
        token = current_composition.set(self)
        try:
            yield self
        finally:
            current_composition.reset(token)


@contextlib.contextmanager
def compose(easel: Easel):
    """Open a Composition over an Easel for one frame.

    Convenience over the parts: Easel.begin/end, Composition(easel),
    use() and finish() all remain public for cases this doesn't fit.
    """
    easel.begin()
    try:
        composition = Composition(easel)
        with composition.use():
            yield composition
        composition.finish()
    finally:
        easel.end()