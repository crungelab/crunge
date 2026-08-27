from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from .chip import Chip

from .viewport import Viewport
from .easel import Easel
from .renderer import Renderer

if TYPE_CHECKING:
    from .node import Node

T_Node = TypeVar("T_Node", bound="Node")


class Vu(Chip[T_Node]):
    """The chip that renders its node.

    Subclasses override `_draw`, not `draw`: `draw` owns the boundary work
    that has to happen before anything is emitted, and calls `_draw` to do
    the actual rendering.
    """

    # Declared rather than inferred. `draw` is overridden here, so the
    # inference in Chip.__init_subclass__ would say True for every Vu
    # regardless; saying it outright keeps the reason visible.
    draws: ClassVar[bool] = True

    # `update` is deliberately not overridden. A Vu that has nothing to do
    # per frame stays out of the update bucket; one that does gets there by
    # defining `update`, same as any other chip.

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

    # -- plug lifecycle ----------------------------------------------------
    _listening: bool = False

    def _enable(self) -> None:
        super()._enable()
        self.listen()

    def on_attached(self, node: "Node[T_Node]") -> None:
        super().on_attached(node)
        self.listen()

    def listen(self) -> None:
        if self._listening or self.node is None:
            return
        self.node.transform_changed.connect(self.on_transform_changed)
        self.node.model_changed.connect(self.on_model_changed)
        self._listening = True

    """
    def plug(self) -> None:
        node = self.node
        node.transform_changed.connect_now(self.on_transform_changed, node)
        if node.model is not None:
            node.model_changed.connect_now(self.on_model_changed, node)
        else:
            node.model_changed.connect(self.on_model_changed)
    """

    def unplug(self) -> None:
        node = self.node
        node.transform_changed.disconnect(self.on_transform_changed)
        node.model_changed.disconnect(self.on_model_changed)

    # -- signals -----------------------------------------------------------

    def on_transform_changed(self, node: T_Node) -> None:
        pass

    def on_model_changed(self, node: T_Node) -> None:
        pass

    # -- frame -------------------------------------------------------------

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        pass