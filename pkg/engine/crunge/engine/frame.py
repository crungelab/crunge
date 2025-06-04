from loguru import logger
import glm

from .widget import Widget
from .view import View


class Frame(Widget):
    def __init__(self, size=glm.ivec2(), view: View = None) -> None:
        super().__init__(size)
        self._view = view
        self.view_stack: list[View] = []

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view: View):
        self._view = view
        self.children.clear()
        self.attach(view)
        view.enable()

    def on_size(self):
        super().on_size()
        if self.view is not None:
            self.view.size = self.size

    def _create(self):
        super()._create()
        logger.debug("Frame.create")
        if self._view is not None:
            self._view.config(window=self).create()
            self.view = self._view

    def push_view(self, new_view):
        #logger.debug('push_view')
        self.view_stack.append(self.view)
        self.view = new_view

    def pop_view(self):
        #logger.debug('pop_view')
        if self.view:
            self.view.disable()
        self.view = self.view_stack.pop()
