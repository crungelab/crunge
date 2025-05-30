from typing import Any, Callable

from loguru import logger
import glm

from .node import Node
from .part import Part
from .controller import Controller
from .renderer import Renderer


class Pane(Node["Pane"]):
    def __init__(self, size = glm.ivec2()) -> None:
        super().__init__()
        self._size = size
        self._controller: Controller = None
        self.parts: list[Part] = []
        self.priority = 0

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value: glm.ivec2):
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

    def enable(self):
        super().enable()
        if self.controller is not None:
            self.controller.enable()

    def disable(self):
        super().disable()
        if self.controller is not None:
            self.controller.disable()
    
    def dispatch(self, event):
        #logger.debug(f"Widget.dispatch: {self}, {self.children}, {event}")
        for child in self.children[::-1]:
            if child.dispatch(event):
                return True
        if self.controller is not None:
            self.controller.dispatch(event)
        return super().dispatch(event)

    def draw(self, renderer: Renderer):
        # logger.debug("Widget.draw")
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            #child.draw(renderer)
            self.draw_child(renderer, child)

    def draw_child(self, renderer: Renderer, child: "Pane"):
        child.draw(renderer)

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