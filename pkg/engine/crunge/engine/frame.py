from typing import Optional

import contextlib
from contextvars import ContextVar

from loguru import logger

from crunge import yoga

from .widget import Widget
from .display import Display


current_frame: ContextVar[Optional["Frame"]] = ContextVar(
    "current_frame", default=None
)


class Frame(Widget):
    def __init__(self, style: yoga.Style = yoga.Style(), display: Display = None) -> None:
        super().__init__(style)
        self._display = display
        self.display_stack: list[Display] = []

    """
    def reset(self):
        super().reset()
        if self.display is not None:
            self.display.reset()
    """

    def make_current(self):
        current_frame.set(self)

    @classmethod
    def get_current(cls) -> Optional["Frame"]:
        return current_frame.get()

    @contextlib.contextmanager
    def use(self):
        prev_frame = self.get_current()
        self.make_current()
        yield self
        if prev_frame is not None:
            prev_frame.make_current()

    @property
    def display(self) -> Display:
        return self._display

    @display.setter
    def display(self, display: Display) -> None:
        self.make_current() # TODO: This should be in _enable() or similar, not channel setter

        if display is None:
            raise ValueError("Display cannot be None")

        if self._display is not None and self._display != display:
            self._display.disable()
            self.remove_child(self._display)

        self._display = display
        
        self.children.clear()

        self.add_child(display)
        self.on_display()

    def on_display(self):
        if self._display is not None:
            self._display.enable()
            self._display.reset()

    def _create(self):
        super()._create()
        logger.debug("Frame.create")
        if self._display is not None:
            self.display = self._display

    def push_display(self, new_display: Display) -> None:
        # logger.debug('push_display')
        self.display_stack.append(self.display)
        self.display = new_display

    def pop_display(self) -> Display:
        # logger.debug('pop_display')
        if self.display:
            self.display.disable()
        self.display = self.display_stack.pop()
        return self.display
