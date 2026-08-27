from typing import Optional

import contextlib
from contextvars import ContextVar

from loguru import logger

from crunge import yoga

from .widget import Widget
from .display import Display

current_frame: ContextVar[Optional["Frame"]] = ContextVar("current_frame", default=None)


class Frame(Widget):
    def __init__(
        self, style: yoga.Style = yoga.Style(), display: Display = None
    ) -> None:
        super().__init__(style)
        self._display = display
        self.display_stack: list[Display] = []

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
        self.switch_display(display)

    # --- switching -------------------------------------------------------

    def switch_display(self, display: Display) -> None:
        """Make `display` current. The outgoing display is suspended, not destroyed."""
        if display is None:
            raise ValueError("Display cannot be None")

        self.make_current()  # TODO: belongs in _enable(), not here

        outgoing = self._display
        if outgoing is not None and outgoing is not display:
            self.suspend_display(outgoing)

        self._display = display
        self.resume_display(display)
        self.on_display()

    def replace_display(self, display: Display) -> None:
        """Switch to `display` and destroy the one being replaced."""
        outgoing = self._display
        self.switch_display(display)
        if outgoing is not None and outgoing is not display:
            outgoing.destroy()

    def suspend_display(self, display: Display) -> None:
        display.disable()
        self.remove_child(display)

    def resume_display(self, display: Display) -> None:
        if display.parent is not self:
            self.add_child(display)
        display.enable()
        display.reset()

    def on_display(self):
        pass

    # --- lifecycle -------------------------------------------------------

    def _create(self):
        super()._create()
        logger.debug("Frame.create")
        if self._display is not None:
            self.switch_display(self._display)

    def _destroy(self):
        for display in reversed(self.display_stack):
            display.destroy()
        self.display_stack.clear()
        super()._destroy()

    # --- stack -----------------------------------------------------------

    def push_display(self, display: Display) -> None:
        if self._display is not None:
            self.display_stack.append(self._display)
        self.switch_display(display)

    def pop_display(self) -> Optional[Display]:
        if not self.display_stack:
            logger.warning("pop_display: display stack is empty")
            return None
        outgoing = self._display
        self.switch_display(self.display_stack.pop())
        return outgoing
