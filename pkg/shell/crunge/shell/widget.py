from typing import List

from loguru import logger

from .dispatcher import Dispatcher
from .controller import Controller
from .render_context import RenderContext
from .gfx import Gfx

class Widget(Dispatcher):
    def __init__(self, width=0, height=0) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.children: List["Widget"] = []
        self.controller: Controller = None

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

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def dispatch(self, event):
        #logger.debug(f"Widget.dispatch: {self}, {self.children}")
        for child in self.children:
            if not child.dispatch(event):
                return False
        if self.controller is not None:
            return self.controller.dispatch(event) and super().dispatch(event)
        return super().dispatch(event)

    def pre_draw(self):
        # logger.debug("Widget.pre_draw")
        for child in self.children:
            child.pre_draw()

    def draw(self):
        # logger.debug("Widget.draw")
        for child in self.children:
            child.draw()

    def post_draw(self):
        # logger.debug("Widget.post_draw")
        for child in self.children:
            child.post_draw()

    def render(self, context: RenderContext):
        # logger.debug("Widget.render")
        for child in self.children:
            child.render(context)

    def update(self, delta_time: float):
        # logger.debug("Widget.update")
        if self.controller is not None:
            self.controller.update(delta_time)
        for child in self.children:
            child.update(delta_time)