from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any

from loguru import logger

if TYPE_CHECKING:
    from .vu import Vu
    from .model import Model

from .dispatcher import Dispatcher

T_Node = TypeVar("T_Node", bound="Node")


class NodeListener(Generic[T_Node]):
    '''
    def on_node_attached(self, node: "Node[T_Node]") -> None:
        pass

    def on_node_detached(self, node: "Node[T_Node]") -> None:
        pass
    '''

    def on_node_transform_change(self, node: "Node[T_Node]") -> None:
        pass

    def on_node_model_change(self, node: "Node[T_Node]") -> None:
        pass


class Node(Dispatcher, Generic[T_Node]):
    def __init__(self, vu: "Vu" = None, model=None) -> None:
        super().__init__()
        self._vu: "Vu" = None
        self._model: "Model" = None
        self.parent: "Node[T_Node]" = None
        self.children: List["Node[T_Node]"] = []
        self.listeners: List[NodeListener[T_Node]] = []

        self.vu = vu
        self.model = model
        self.visible = True

    @property
    def vu(self) -> "Vu":
        return self._vu

    @vu.setter
    def vu(self, value: "Vu"):
        self._vu = value
        if value is None:
            return
        value.node = self
        value.enable()

    @property
    def model(self) -> "Model":
        return self._model

    @model.setter
    def model(self, value: "Model"):
        self._model = value
        if value is None:
            return
        for listener in self.listeners:
            listener.on_node_model_change(self)

    def add_listener(self, listener: NodeListener[T_Node]) -> None:
        self.listeners.append(listener)

    def remove_listener(self, listener: NodeListener[T_Node]) -> None:
        self.listeners.remove(listener)

    def clear(self):
        for child in self.children:
            child.clear()
        self.children.clear()

    def destroy(self):
        logger.debug(f"Destroying node: {self}")
        if self.parent:
            self.parent.remove_child(self)
        if self.vu:
            self.vu.destroy()
        for child in self.children:
            child.destroy()
        self.clear()

    def _enable(self) -> None:
        super()._enable()
        if self.vu is not None:
            self.vu.enable()
        for child in self.children:
            child.enable()

    def _disable(self):
        super()._disable()
        if self.vu is not None:
            self.vu.disable()
        for child in self.children:
            child.disable()

    def add_child(self, child: "Node[T_Node]"):
        child.parent = self
        self.children.append(child)
        child.on_added()
        return child

    def on_added(self):
        self.enable()

    def remove_child(self, child: "Node[T_Node]"):
        child.on_removed()
        child.parent = None
        # if child in self.children:
        self.children.remove(child)

    def on_removed(self):
        pass

    def add_children(self, children: list["Node[T_Node]"]):
        for child in children:
            self.add_child(child)

    def remove_children(self, children: list["Node[T_Node]"]):
        for child in children:
            self.remove_child(child)

    def sort_children(
        self, key: Callable[["Node[T_Node]"], Any], reverse: bool = False
    ) -> None:
        """
        Sorts the children list based on a key function.

        :param key: A lambda function that defines the sorting key.
        :param reverse: Whether to sort in reverse order. Default is False.
        """
        self.children.sort(key=key, reverse=reverse)

    """
    def _draw(self):
        logger.debug("Node.draw")
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            child.draw(renderer)
    """

    def draw(self):
        if not self.visible:
            return
        self._draw()

    def _draw(self):
        if self.vu is not None:
            self.vu.draw()
        for child in self.children:
            # child.draw()
            self.draw_child(child)

    def draw_child(self, child: "Node[T_Node]"):
        child.draw()

    def update(self, delta_time: float):
        if self.vu is not None:
            self.vu.update(delta_time)
        for child in self.children:
            child.update(delta_time)
