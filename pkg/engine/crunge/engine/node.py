from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any

#if TYPE_CHECKING:
from .vu import Vu

from .dispatcher import Dispatcher


T_Node = TypeVar("T_Node")
T_Vu = TypeVar("T_Vu", "Vu", None)
T_Renderer = TypeVar("T_Renderer")

class Node(Dispatcher, Generic[T_Node, T_Vu, T_Renderer]):
    def __init__(self, vu: T_Vu = None) -> None:
        super().__init__()
        self.vu: T_Vu = vu
        self.parent: "Node[T_Node]" = None
        self.children: List["Node[T_Node]"] = []

    '''
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
    '''

    def clear(self):
        for child in self.children:
            child.clear()
        self.children.clear()

    def destroy(self):
        if self.parent:
            self.parent.detach(self)
        for child in self.children:
            child.destroy()
        self.clear()

    def attach(self, child: "Node[T_Node]"):
        child.parent = self
        self.children.append(child)
        child.on_attached()

    def on_attached(self):
        pass

    def detach(self, child: "Node[T_Node]"):
        child.parent = None
        self.children.remove(child)
        child.on_detached()

    def on_detached(self):
        pass

    def add_children(self, children: list["Node[T_Node]"]):
        for child in children:
            self.attach(child)

    def remove_children(self, children: list["Node[T_Node]"]):
        for child in children:
            self.detach(child)


    def sort_children(self, key: Callable[["Node[T_Node]"], Any], reverse: bool = False) -> None:
        """
        Sorts the children list based on a key function.

        :param key: A lambda function that defines the sorting key.
        :param reverse: Whether to sort in reverse order. Default is False.
        """
        self.children.sort(key=key, reverse=reverse)


    def pre_draw(self, renderer: T_Renderer):
        # logger.debug("Node.pre_draw")
        if self.vu is not None:
            self.vu.pre_draw(renderer)
        for child in self.children:
            child.pre_draw(renderer)

    def draw(self, renderer: T_Renderer):
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            child.draw(renderer)

    def post_draw(self, renderer: T_Renderer):
        # logger.debug("Widget.post_draw")
        if self.vu is not None:
            self.vu.post_draw(renderer)
        for child in self.children:
            child.post_draw(renderer)

    def update(self, delta_time: float):
        if self.vu is not None:
            self.vu.update(delta_time)
        for child in self.children:
            child.update(delta_time)