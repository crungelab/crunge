from typing import Optional, List
from ctypes import sizeof

import contextlib
from contextvars import ContextVar

from loguru import logger
import glm

from crunge import wgpu
from crunge import skia

from .base import Base
from .signal import Signal
from .math import Rect2i  # ASSUMPTION: import path
from .uniforms import ViewportUniform, cast_vec2
from .easel import Easel

current_viewport: ContextVar[Optional["Viewport"]] = ContextVar(
    "current_viewport", default=None
)


class Viewport(Base):
    """A rectangular region to render into, relative to its parent.

    A Viewport that owns an Easel is the origin of a new coordinate space:
    its global_rect.position is always (0, 0), and its Easel is resized to
    match its own size. A Viewport that inherits its parent's Easel is
    positioned relative to that parent's global_rect.
    """

    def __init__(
        self,
        easel: Easel = None,
        rect: Rect2i = None,
    ):
        super().__init__()
        self._easel = easel  # None => inherit from parent
        self._rect = rect  # None => fill parent (or own easel)
        self._parent: Optional["Viewport"] = None
        self.children: List["Viewport"] = []

        self._global_rect: Rect2i = None
        self._global_rect_dirty = True
        self._resizing_easel = False

        self.rect_changed: Signal[Rect2i] = Signal()

        self.create_buffers()
        self.update_gpu()

        if self._easel is not None:
            self._easel.size_changed.connect(self.on_easel_size)

    # -- hierarchy ---------------------------------------------------

    @property
    def parent(self) -> Optional["Viewport"]:
        return self._parent

    def add_child(self, child: "Viewport") -> "Viewport":
        child._parent = self
        self.children.append(child)
        child.invalidate()
        return child

    def remove_child(self, child: "Viewport") -> None:
        self.children.remove(child)
        child._parent = None
        child.invalidate()

    @property
    def easel(self) -> Optional[Easel]:
        if self._easel is not None:
            return self._easel
        if self._parent is not None:
            return self._parent.easel
        return None

    @property
    def owns_easel(self) -> bool:
        return self._easel is not None

    # -- geometry ----------------------------------------------------

    @property
    def rect(self) -> Rect2i:
        return self._rect

    @rect.setter
    def rect(self, value: Rect2i):
        self._rect = value
        self.invalidate()

    @property
    def global_rect(self) -> Rect2i:
        if self._global_rect_dirty:
            self._global_rect = self._compute_global_rect()
            self._global_rect_dirty = False
        return self._global_rect

    @property
    def size(self) -> glm.ivec2:
        return self.global_rect.size

    @property
    def width(self) -> int:
        return self.global_rect.width

    @property
    def height(self) -> int:
        return self.global_rect.height

    def _compute_global_rect(self) -> Rect2i:
        if self.owns_easel:
            if self._rect is None:
                size = self._easel.size  # easel authoritative
            else:
                size = self._rect.size  # viewport authoritative
            return Rect2i(0, 0, size.x, size.y)

        if self._parent is None:
            # Detached, or root over an inherited easel that doesn't exist yet.
            if self._rect is not None:
                return self._rect
            return Rect2i(0, 0, 0, 0)

        pr = self._parent.global_rect
        if self._rect is None:
            return Rect2i(pr.x, pr.y, pr.width, pr.height)
        return Rect2i(
            pr.x + self._rect.x,
            pr.y + self._rect.y,
            self._rect.width,
            self._rect.height,
        )

    def _inherited_size(self) -> glm.ivec2:
        if self._parent is not None:
            return self._parent.global_rect.size
        if self._easel is not None:
            return self._easel.size
        return glm.ivec2(0, 0)

    # -- invalidation ------------------------------------------------

    def invalidate(self) -> None:
        """Mark this subtree's global_rect stale, then notify.

        Two phases on purpose: every descendant is marked dirty before any
        signal fires, so a listener that synchronously reads global_rect
        anywhere in the tree sees a consistent result.
        """
        self._invalidate_subtree()
        self._notify_subtree()

    def _invalidate_subtree(self) -> None:
        self._global_rect_dirty = True
        for child in tuple(self.children):
            child._invalidate_subtree()

    def _notify_subtree(self) -> None:
        rect = self.global_rect
        # Only push down when this viewport is the authority.
        if self.owns_easel and self._rect is not None and self._easel.size != rect.size:
            self._easel.size = rect.size
        self.update_gpu()
        self.rect_changed.emit(rect)
        for child in tuple(self.children):
            child._notify_subtree()

    def on_easel_size(self, size: glm.ivec2) -> None:
        if self._resizing_easel:
            return
        self.invalidate()

    # -- skia --------------------------------------------------------

    @contextlib.contextmanager
    def canvas(self) -> skia.Canvas:
        """Scope the easel's canvas to this viewport's rect."""
        canvas = self.easel.canvas
        rect = self.global_rect
        canvas.save()
        canvas.clip_rect(  # ASSUMPTION: skia binding
            skia.Rect.make_xywh(rect.x, rect.y, rect.width, rect.height)
        )
        canvas.translate(rect.x, rect.y)
        yield canvas
        canvas.restore()

    # -- context -----------------------------------------------------

    def make_current(self):
        current_viewport.set(self)

    @classmethod
    def get_current(cls) -> Optional["Viewport"]:
        return current_viewport.get()

    @contextlib.contextmanager
    def use(self):
        prev = self.get_current()
        self.make_current()
        yield self
        if prev is not None:
            prev.make_current()

    # -- gpu ---------------------------------------------------------

    def create_buffers(self):
        self.uniform_buffer_size = sizeof(ViewportUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Viewport Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def update_gpu(self):
        logger.debug(f"Viewport: update_gpu: {self.global_rect}")
        uniform = ViewportUniform()
        uniform.size = cast_vec2(self.global_rect.size)
        self.device.queue.write_buffer(self.uniform_buffer, 0, uniform)
