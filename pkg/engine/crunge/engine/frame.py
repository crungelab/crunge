from loguru import logger

from crunge import yoga

from .widget import Widget
from .screen import Screen


class Frame(Widget):
    def __init__(self, style: yoga.Style = yoga.Style(), screen: Screen = None) -> None:
        super().__init__(style)
        self._screen = screen
        self.screen_stack: list[Screen] = []

    @property
    def screen(self) -> Screen:
        return self._screen

    @screen.setter
    def screen(self, screen: Screen) -> None:
        if self._screen is not None and self._screen != screen:
            self._screen.disable()
            self.remove_child(self._screen)

        self._screen = screen
        self.children.clear()
        self.add_child(screen)
        self.on_screen()

    def on_screen(self):
        pass

    def _create(self):
        super()._create()
        logger.debug("Frame.create")
        if self._screen is not None:
            self.screen = self._screen

    def push_screen(self, new_screen: Screen) -> None:
        # logger.debug('push_screen')
        self.screen_stack.append(self.screen)
        self.screen = new_screen

    def pop_screen(self) -> Screen:
        # logger.debug('pop_screen')
        if self.screen:
            self.screen.disable()
        self.screen = self.screen_stack.pop()
        return self.screen
