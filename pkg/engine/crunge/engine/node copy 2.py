from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

from loguru import logger

from .signal import Signal
from .base_node import BaseNode
from .chip import Chip
from .vu import Vu

if TYPE_CHECKING:
    from .model import Model

T_Node = TypeVar("T_Node", bound="Node")


class Node(BaseNode, Generic[T_Node]):
    """A node in the scene graph.

    The vu is no longer a special slot — it is a chip like any other, so
    creation, enabling, drawing, updating and teardown all come from the
    chip walk in BaseNode. `vu` is kept as a named accessor onto the chip
    map, since that is how most call sites want to talk about it.
    """

    def __init__(
        self,
        vu: Vu | None = None,
        model: "Model | None" = None,
        chips: list[Chip[Any]] | None = None,
    ) -> None:
        super().__init__(chips)
        self._vu: "Vu" = None
        self._model: "Model | None" = None
        self.parent: "Node[T_Node] | None" = None
        self.children: list["Node[T_Node]"] = []

        # TODO: transform_changed belongs on Node2D/Node3D. Node has no
        # transform, so a chip that connects here on a plain Node is
        # listening to a signal that can never fire.
        self.transform_changed: Signal["Node[T_Node]"] = Signal()
        self.model_changed: Signal["Node[T_Node]"] = Signal()

        self.model = model
        self.vu = vu
        """
        if vu is not None:
            self.vu = vu
            if model is not None:
                vu.model = model
                vu.sprite = model
        self.model = model

        self.add(vu) if vu is not None else None
        """
        self.visible = True

    # -- properties ----------------------------------------------------

    
    """
    @property
    def vu(self) -> Vu | None:
        return self.get(Vu)

    @vu.setter
    def vu(self, value: Vu | None) -> None:
        old = self.get(Vu)
        if old is value:
            return
        if old is not None:
            self.remove(old)
            old.destroy()
        if value is not None:
            self.add(value)
    """

    @property
    def vu(self) -> "Vu":
        return self._vu

    @vu.setter
    def vu(self, value: "Vu"):
        old = self._vu
        if old is not None and old is not value:
            old.destroy()
        self._vu = value
        if value is None:
            return

        if self._model is not None:
            value.model = self._model
            value.sprite = self._model

        #self._sync_lifetime(value)
        self.add(value)
        #logger.debug(f"Node.vu set: {value}, lifetime: {value._lifetime}")

    @property
    def model(self) -> "Model | None":
        return self._model

    @model.setter
    def model(self, value: "Model | None") -> None:
        self._model = value
        if value is None:
            return
        self.model_changed.emit(self)

    # -- lifetime ------------------------------------------------------

    def create_children(self) -> None:
        super().create_children()  # chips created and plugged
        for child in list(self.children):
            child.create()

    def enable_children(self) -> None:
        super().enable_children()  # chips enabled
        for child in list(self.children):
            child.enable()

    def reset_children(self) -> None:
        super().reset_children()  # chips reset
        for child in list(self.children):
            child.reset()

    def _disable(self) -> None:
        for child in list(self.children):
            child.disable()
        super()._disable()  # chips disabled

    def _destroy(self) -> None:
        logger.debug(f"Destroying node: {self}")
        if self.parent is not None and not self.parent.is_destroying:
            self.parent.remove_child(self)
        super()._destroy()

    def destroy_children(self) -> None:
        for child in list(self.children):
            child.destroy()
        self.children.clear()
        super().destroy_children()  # chips destroyed

    # -- tree ----------------------------------------------------------

    def add_child(self, child: "Node[T_Node]") -> "Node[T_Node]":
        child.parent = self
        self.children.append(child)
        self.on_child_added(child)
        child.on_added()
        self._sync_lifetime(child)
        return child

    def on_child_added(self, child: "Node[T_Node]") -> None:
        """Parent-side notification. Child is attached but not yet created."""

    def on_added(self) -> None:
        """Self-side notification. Parent is set; lifetime not yet synced."""

    def remove_child(self, child: "Node[T_Node]") -> None:
        child.disable()
        self.on_child_removed(child)
        child.on_removed()
        child.parent = None
        self.children.remove(child)

    def on_child_removed(self, child: "Node[T_Node]") -> None:
        """Parent-side notification. Child is disabled but still attached."""

    def on_removed(self) -> None:
        """Self-side notification. Parent is still set."""

    def add_children(self, children: list["Node[T_Node]"]) -> None:
        for child in children:
            self.add_child(child)

    def remove_children(self, children: list["Node[T_Node]"]) -> None:
        for child in children:
            self.remove_child(child)

    def clear(self) -> None:
        """Detach all children. They remain created and re-addable."""
        for child in list(self.children):
            self.remove_child(child)

    def sort_children(
        self, key: Callable[["Node[T_Node]"], object], reverse: bool = False
    ) -> None:
        """
        Sorts the children list based on a key function.

        :param key: A lambda function that defines the sorting key.
        :param reverse: Whether to sort in reverse order. Default is False.
        """
        self.children.sort(key=key, reverse=reverse)

    # -- frame ---------------------------------------------------------
    #
    # `_draw` and `_update` come from BaseNode and broadcast to the chips.
    # Nothing to add here; Node only owns the walk over children.

    def draw(self) -> None:
        if not self.visible:
            return
        self._draw()
        self.draw_children()

    def draw_children(self) -> None:
        for child in self.children:
            self.draw_child(child)

    def draw_child(self, child: "Node[T_Node]") -> None:
        child.draw()

    def render(self) -> None:
        self.draw()

    def update(self, delta_time: float) -> None:
        self._update(delta_time)
        self.update_children(delta_time)

    def update_children(self, delta_time: float) -> None:
        for child in self.children:
            self.update_child(child, delta_time)

    def update_child(self, child: "Node[T_Node]", delta_time: float) -> None:
        child.update(delta_time)