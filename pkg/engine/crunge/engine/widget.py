from typing import List

from loguru import logger
import glm

from .dispatcher import Dispatcher
from .controller import Controller
from .renderer import Renderer
from .vu import Vu
from .gfx import Gfx

class Widget(Dispatcher):
    def __init__(self, size = glm.ivec2()) -> None:
        super().__init__()
        self.size = size
        self.children: List["Widget"] = []
        self.controller: Controller = None
        self.vu: Vu = None

    @property
    def width(self):
        return self.size.x
    
    @property
    def height(self):
        return self.size.y

    def resize(self, size: glm.ivec2):
        self.size = size

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

    def create(self):
        pass

    def add_child(self, child: "Widget"):
        self.children.append(child)

    def remove_child(self, child: "Widget"):
        self.children.remove(child)

    def dispatch(self, event):
        #logger.debug(f"Widget.dispatch: {self}, {self.children}")
        #for child in self.children:
        for child in self.children[::-1]:
            if child.dispatch(event):
                return True
        if self.controller is not None:
            return self.controller.dispatch(event) and super().dispatch(event)
        return super().dispatch(event)

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