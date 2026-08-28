from __future__ import annotations

from enum import IntFlag, auto
from typing import TYPE_CHECKING, ClassVar, TypeVar

from .chip import Chip

from .viewport import Viewport
from .easel import Easel
from .renderer import Renderer

if TYPE_CHECKING:
    from .node import Node

T_Node = TypeVar("T_Node", bound="Node")


class Dirt(IntFlag):
    """What a vu owes the next flush.

    One member per thing that gets rebuilt independently. Transform is not
    a member: the node owns the transform and already tracks its own dirty
    state, so a second flag here would be a duplicate source of truth.
    """

    NONE = 0
    GEOMETRY = auto()  # vertex/index data the vu owns
    GPU = auto()  # uniform written into the node buffer


class Vu(Chip[T_Node]):
    """The chip that renders its node.

    Subclasses override `_draw`, not `draw`: `draw` owns the boundary work
    that has to happen before anything is emitted, and calls `_draw` to do
    the actual rendering.

    Listening is scoped to enablement. A disabled vu is not subscribed at
    all, so nothing it owns can be touched while it is not participating in
    the frame, and there is no per-emit `if self.enabled` branch on a hot
    path. `_enable` resyncs against current node state, which covers
    everything that changed while the vu was disconnected.

    Signal handlers record state and mark dirt; they never touch the GPU.
    Rebuilds happen in `flush`, which the owning subclass calls from
    `update` — before the render pass opens, since buffer writes are
    illegal once it has. Each domain clears only on success, so a rebuild
    that runs before its target exists is retried without dragging the
    others along, and the order in which membership, model and transform
    arrive stops mattering.
    """

    # Declared rather than inferred. `draw` is overridden here, so the
    # inference in Chip.__init_subclass__ would say True for every Vu
    # regardless; saying it outright keeps the reason visible.
    draws: ClassVar[bool] = True

    # `update` is deliberately not overridden. A Vu with nothing to rebuild
    # stays out of the update bucket; one that has something gets there by
    # defining `update` and calling `flush` from it.

    def __init__(self) -> None:
        super().__init__()
        self._dirt = Dirt.NONE

    # -- ambient frame state ----------------------------------------------

    @property
    def current_viewport(self) -> Viewport | None:
        return Viewport.get_current()

    @property
    def current_easel(self) -> Easel | None:
        viewport = self.current_viewport
        return viewport.easel if viewport is not None else None

    @property
    def current_renderer(self) -> Renderer | None:
        return Renderer.get_current()

    # -- dirt --------------------------------------------------------------

    @property
    def dirt(self) -> Dirt:
        return self._dirt

    @property
    def dirty(self) -> bool:
        return self._dirt is not Dirt.NONE

    def mark(self, dirt: Dirt) -> None:
        self._dirt |= dirt

    def mark_geometry(self) -> None:
        self.mark(Dirt.GEOMETRY)

    def mark_gpu(self) -> None:
        self.mark(Dirt.GPU)

    def flush(self) -> None:
        """Rebuild whatever is owed. Safe every frame; cheap when clean.

        Explicit per-domain dispatch rather than a table: the order between
        domains is load-bearing, and a rebuild that feeds another has to
        run first. Geometry before the uniform, since vertex data can
        change the extents the uniform describes.
        """
        dirt = self._dirt
        if dirt is Dirt.NONE:
            return

        if dirt & Dirt.GEOMETRY and self._flush_geometry():
            self._dirt &= ~Dirt.GEOMETRY

        if dirt & Dirt.GPU and self._flush_gpu():
            self._dirt &= ~Dirt.GPU

    def _flush_geometry(self) -> bool:
        """Rebuild vertex/index data. Return False if the target is not
        there yet — the flag stays set and retries on the next flush."""
        return True

    def _flush_gpu(self) -> bool:
        """Write the node uniform. Return False if the target is not there
        yet — the flag stays set and retries on the next flush."""
        return True

    # -- listening ---------------------------------------------------------
    def _enable(self) -> None:
        super()._enable()
        if not self.attached:
            return  # standalone vu: no node state to track
        self.listen()
        self.sync()

    """
    def _enable(self) -> None:
        super()._enable()
        self.listen()
        self.sync()
    """

    def _disable(self) -> None:
        self.deafen()
        super()._disable()

    def listen(self) -> None:
        """Subscribe to node state. Signal.connect dedupes, so this is
        idempotent and needs no flag of its own."""
        node = self.node
        node.transform_changed.connect(self.on_transform_changed)
        node.model_changed.connect(self.on_model_changed)

    def deafen(self) -> None:
        node = self._node
        if node is None:
            return
        node.transform_changed.disconnect(self.on_transform_changed)
        node.model_changed.disconnect(self.on_model_changed)

    def sync(self) -> None:
        """Catch up on state that changed while unsubscribed.

        Model first: it is where extents come from, and the transform is
        what gets applied to them. Syncing the transform first applies a
        correct transform to stale extents.
        """
        node = self.node
        if node.model is not None:
            self.on_model_changed(node)
        self.on_transform_changed(node)

    def on_detached(self) -> None:
        self.deafen()
        super().on_detached()

    # -- signals -----------------------------------------------------------
    #
    # Record and mark. No GPU work here — these fire at arbitrary points in
    # the lifecycle, including before the vu has a buffer.

    def on_transform_changed(self, node: T_Node) -> None:
        pass

    def on_model_changed(self, node: T_Node) -> None:
        pass

    # -- frame -------------------------------------------------------------

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        pass