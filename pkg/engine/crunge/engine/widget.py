from typing import Any, Callable

from loguru import logger

from .math import Size2i
from .dispatcher import Dispatcher
from .part import Part
from .controller import Controller
from .renderer import Renderer
from .vu import Vu
from .gfx import Gfx

class Widget(Dispatcher):
    def __init__(self, size = Size2i()) -> None:
        super().__init__()
        #self.size = size
        self._size = size
        self.parent = None
        self.children: list["Widget"] = []
        self._controller: Controller = None
        self.vu: Vu = None
        self.parts: list[Part] = []
        self.priority = 0

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value: Size2i):
        changed = self._size != value
        self._size = value
        if changed:
            self.on_size()

    def on_size(self):
        pass

    @property
    def width(self):
        return self.size.x
    
    @width.setter
    def width(self, value):
        self.size.x = value
    
    @property
    def height(self):
        return self.size.y
    
    @height.setter
    def height(self, value):
        self.size.y = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def controller(self) -> Controller:
        return self._controller

    @controller.setter
    def controller(self, controller: Controller):
        if controller == self._controller:
            return
        if self._controller:
            self._controller.disable()
        self._controller = controller
        controller.enable()

    @property
    def gfx(self):
        return Gfx()

    @property
    def instance(self):
        return self.gfx.instance

    @property
    def device(self):
        return self.gfx.device

    @property
    def queue(self):
        return self.gfx.queue

    def enable(self):
        super().enable()
        if self.controller is not None:
            self.controller.enable()

    def disable(self):
        super().disable()
        if self.controller is not None:
            self.controller.disable()

    def add_child(self, child: "Widget"):
        child.parent = self
        self.children.append(child)

    def add_children(self, children: list["Widget"]):
        for child in children:
            self.add_child(child)

    def remove_child(self, child: "Widget"):
        self.children.remove(child)

    def remove_children(self, children: list["Widget"]):
        for child in children:
            self.remove_child(child)

    def clear(self):
        self.children.clear()

    def sort_children(self, key: Callable[["Widget"], Any], reverse: bool = False) -> None:
        """
        Sorts the children list based on a key function.

        :param key: A lambda function that defines the sorting key.
        :param reverse: Whether to sort in reverse order. Default is False.
        """
        self.children.sort(key=key, reverse=reverse)

    
    def dispatch(self, event):
        #logger.debug(f"Widget.dispatch: {self}, {self.children}")
        for child in self.children[::-1]:
            if child.dispatch(event):
                return True
        if self.controller is not None:
            self.controller.dispatch(event)
        return super().dispatch(event)

    '''
    def dispatch(self, event):
        #logger.debug(f"Widget.dispatch: {self}, {self.children}")
        #for child in self.children:
        for child in self.children[::-1]:
            if child.dispatch(event):
                return True
        if self.controller is not None:
            return self.controller.dispatch(event) and super().dispatch(event)
        return super().dispatch(event)
    '''

    def pre_draw(self, renderer: Renderer):
        # logger.debug("Widget.pre_draw")
        if self.vu is not None:
            self.vu.pre_draw(renderer)
        for child in self.children:
            child.pre_draw(renderer)

    def draw(self, renderer: Renderer):
        # logger.debug("Widget.draw")
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            #child.draw(renderer)
            self.draw_child(renderer, child)

    def draw_child(self, renderer: Renderer, child: "Widget"):
        child.draw(renderer)

    def post_draw(self, renderer: Renderer):
        # logger.debug("Widget.post_draw")
        if self.vu is not None:
            self.vu.post_draw(renderer)
        for child in self.children:
            child.post_draw(renderer)

    def update(self, delta_time: float):
        # logger.debug("Widget.update")
        if self.controller is not None:
            self.controller.update(delta_time)
        for child in self.children:
            child.update(delta_time)

    def add_part(self, part: Part):
        self.parts.append(part)
        part.widget = self

    def remove_part(self, part: Part):
        self.parts.remove(part)
        part.widget = None

    def get_part(self, part_type: type[Part]):
        for part in self.parts:
            if isinstance(part, part_type):
                return part
        return None