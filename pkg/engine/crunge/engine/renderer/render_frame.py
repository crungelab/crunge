# render_frame.py
from typing import Optional
import contextlib
from contextvars import ContextVar

from crunge import wgpu

from ..base import Base
from ..easel import Easel

current_render_frame: ContextVar[Optional["RenderFrame"]] = ContextVar(
    "current_render_frame", default=None
)


class RenderFrame(Base):
    """Per-frame render state. Carries; does not decide."""

    def __init__(self, easel: Easel, encoder: wgpu.CommandEncoder) -> None:
        super().__init__()
        self.easel = easel
        self.encoder = encoder
        self.cleared = False

    def make_current(self):
        current_render_frame.set(self)

    @classmethod
    def get_current(cls) -> Optional["RenderFrame"]:
        return current_render_frame.get()

    @contextlib.contextmanager
    def use(self):
        prev = self.get_current()
        self.make_current()
        yield self
        if prev is not None:
            prev.make_current()
