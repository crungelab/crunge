from typing import TYPE_CHECKING, TypeVar, Generic, Callable

from loguru import logger

if TYPE_CHECKING:
    from .vu import Vu
    from .model import Model

from .signal import Signal
from .dispatcher import Dispatcher

T_Node = TypeVar("T_Node", bound="Node")


class Node(Dispatcher, Generic[T_Node]):
    def __init__(self, vu: "Vu" = None, model=None) -> None:
        super().__init__()
        self._vu: "Vu" = None
        self._model: "Model" = None
        self.parent: "Node[T_Node]" = None
        self.children: list["Node[T_Node]"] = []

        self.transform_changed: Signal["Node[T_Node]"] = Signal()
        self.model_changed: Signal["Node[T_Node]"] = Signal()

        self.vu = vu
        self.model = model
        self.visible = True

    # -- properties ----------------------------------------------------

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
        value.node = self
        self._sync_lifetime(value)
        #logger.debug(f"Node.vu set: {value}, lifetime: {value._lifetime}")

    @property
    def model(self) -> "Model":
        return self._model

    @model.setter
    def model(self, value: "Model"):
        self._model = value
        if value is None:
            return
        self.model_changed.emit(self)

    # -- lifetime ------------------------------------------------------

    def create_children(self) -> None:
        super().create_children()
        if self._vu is not None:
            self._vu.create()
        for child in list(self.children):
            #logger.debug(f"Creating child: {child}")
            child.create()

    def _enable(self) -> None:
        super()._enable()
        if self._vu is not None:
            self._vu.enable()
        for child in list(self.children):
            child.enable()

    def enable_children(self) -> None:
        super().enable_children()
        for child in list(self.children):
            #logger.debug(f"Creating child: {child}")
            child.enable()

    def reset_children(self) -> None:
        super().reset_children()
        for child in list(self.children):
            #logger.debug(f"Resetting child: {child}")
            child.reset()

    def _disable(self) -> None:
        for child in list(self.children):
            child.disable()
        if self._vu is not None:
            self._vu.disable()
        super()._disable()

    """
    def _destroy(self):
        logger.debug(f"Destroying node: {self}")
        if self.parent:
            self.parent.remove_child(self)
        if self.vu:
            self.vu.destroy()
        for child in self.children:
            child.destroy()
        self.clear()
        super()._destroy()
    """
    def _destroy(self) -> None:
        logger.debug(f"Destroying node: {self}")
        if self.parent is not None and not self.parent.is_destroying:
            self.parent.remove_child(self)
        if self.vu:
            self.vu.destroy()

        super()._destroy()

    def destroy_children(self) -> None:
        for child in list(self.children):
            child.destroy()
        self.children.clear()
        super().destroy_children()

    """
    def _destroy(self) -> None:
        logger.debug(f"Destroying node: {self}")
        if self.parent is not None and not self.parent.is_destroying:
            self.parent.remove_child(self)
        super()._destroy()

    def destroy_children(self) -> None:
        for child in list(self.children):
            child.parent = None
            child.destroy()
        self.children.clear()
        if self._vu is not None:
            self._vu.destroy()
            self._vu = None
        super().destroy_children()
    """

    # -- tree ----------------------------------------------------------

    def add_child(self, child: "Node[T_Node]") -> "Node[T_Node]":
        child.parent = self
        self.children.append(child)
        self.on_child_added(child)
        child.on_added()
        self._sync_lifetime(child)
        logger.debug(f"Added child: {child} to parent: {self}, lifetime: {child._lifetime}")
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

    def draw(self) -> None:
        if not self.visible:
            return
        self._draw()
        self.draw_children()

    def _draw(self) -> None:
        if self._vu is not None:
            self._vu.draw()

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

    def _update(self, delta_time: float) -> None:
        if self._vu is not None:
            self._vu.update(delta_time)

    def update_children(self, delta_time: float) -> None:
        for child in self.children:
            self.update_child(child, delta_time)

    def update_child(self, child: "Node[T_Node]", delta_time: float) -> None:
        child.update(delta_time)