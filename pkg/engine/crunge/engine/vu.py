from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from .chip import Chip

from .viewport import Viewport
from .easel import Easel
from .renderer import Renderer

if TYPE_CHECKING:
    from .node import Node
    from .vu_group import VuGroup

T_Node = TypeVar("T_Node", bound="Node")


class Vu(Chip[T_Node]):
    """The chip that renders its node.

    Subclasses override `_draw`, not `draw`: `draw` owns the boundary work
    that has to happen before anything is emitted, and calls `_draw` to do
    the actual rendering.

    Dirt tracking and enable-scoped listening come from Chip. What Vu adds
    is the specific subscription — transform and model — and the draw.
    """

    # Declared rather than inferred. `draw` is overridden here, so the
    # inference in Chip.__init_subclass__ would say True for every Vu
    # regardless; saying it outright keeps the reason visible.
    draws: ClassVar[bool] = True

    # `update` is deliberately not overridden. A Vu with nothing to rebuild
    # stays out of the update bucket; one that has something gets there by
    # defining `update` and calling `flush` from it.

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

    # -- listening ---------------------------------------------------------

    def listen(self) -> None:
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
        """Model first: it is where extents come from, and the transform is
        what gets applied to them. Syncing the transform first applies a
        correct transform to stale extents."""
        node = self.node
        if node.model is not None:
            self.on_model_changed(node)
        self.on_transform_changed(node)

    # -- group -------------------------------------------------------------
    @property
    def group(self) -> "VuGroup":
        return self._group

    @group.setter
    def group(self, value: "VuGroup"):
        self._group = value
        self.on_group()

    def on_group(self) -> None:
        pass

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