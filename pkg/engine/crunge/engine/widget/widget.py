from loguru import logger
import glm

from crunge import yoga

from ..sdl.event_handler import EventHandler
from ..node import Node
from ..dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED
#from ..controller import Controller
from ..gfx_access import GfxAccess

class Widget(EventHandler, GfxAccess, Node["Widget"]):
    def __init__(self, style: yoga.Style = yoga.Style()) -> None:
        super().__init__()
        self._size = glm.ivec2(0, 0)
        #self._controller: Controller = None
        self.priority = 0
        self.hovered = False
        # Layout
        self.introduced = False
        self.layout_dirty = False
        self.layout = yoga.Layout()
        self.layout.set_style(style)
        self.layout.set_dirtied_func(self.mark_layout_dirty)

    def intro(self) -> None:
        pass

    def mark_layout_dirty(self) -> None:
        logger.debug(f"Widget.mark_layout_dirty: {self}")
        self.layout_dirty = True

    def apply_layout(self) -> None:
        # logger.debug(f"Widget.apply_layout: {self}")
        if not self.layout.has_new_layout():
            return

        self.on_layout()
        self.layout.mark_layout_seen()

        for child in self.children:
            child.apply_layout()

    def on_layout(self) -> None:
        # logger.debug(f"Widget.on_layout: {self}")
        self._set_size(
            glm.ivec2(
                self.layout.get_computed_width(), self.layout.get_computed_height()
            )
        )
        if not self.introduced:
            self.intro()
            self.introduced = True

    @property
    def style(self) -> yoga.Style:
        return self.layout.get_style()

    @style.setter
    def style(self, value: yoga.Style) -> None:
        if not isinstance(value, yoga.Style):
            raise TypeError(f"Expected yoga.Style, got {type(value)}")
        self.layout.set_style(value)

    @property
    def position(self) -> glm.ivec2:
        return glm.ivec2(
            self.layout.get_computed_left(), self.layout.get_computed_top()
        )

    @property
    def global_position(self) -> glm.ivec2:
        if self.parent is None:
            return glm.ivec2(0, 0)

        return self.parent.global_position + self.position

    @property
    def bounds(self) -> yoga.Bounds:
        return self.layout.get_computed_bounds()

    @property
    def size(self) -> glm.ivec2:
        return glm.ivec2(
            self.layout.get_computed_width(), self.layout.get_computed_height()
        )

    def _set_size(self, value: glm.ivec2) -> bool:
        changed = self._size != value
        self._size = glm.ivec2(value)

        if changed:
            self.on_size()

        return changed

    @size.setter
    def size(self, value: glm.ivec2) -> None:
        self.layout.set_width(value.x)
        self.layout.set_height(value.y)
        self._set_size(value)

    def on_size(self) -> None:
        pass

    @property
    def width(self) -> int:
        return self.size.x

    @width.setter
    def width(self, value: int) -> None:
        self.size = glm.ivec2(value, self._size.y)

    @property
    def height(self) -> int:
        return self.size.y

    @height.setter
    def height(self, value: int) -> None:
        self.size = glm.ivec2(self._size.x, value)

    def dispatch(self, event) -> DispatchResult:
        for child in reversed(self.children):
            if child.dispatch(event):
                return EVENT_HANDLED
        return super().dispatch(event) or self.handle(event)

    '''
    def dispatch(self, event) -> DispatchResult:
        for child in reversed(self.children):
            if child.dispatch(event) is not None:
                return EVENT_HANDLED
        if super().dispatch(event) is not None:
            return EVENT_HANDLED
        return self.handle(event)
    '''

    '''
    @property
    def controller(self) -> Controller:
        return self._controller

    @controller.setter
    def controller(self, controller: Controller) -> None:
        if controller == self._controller:
            return
        if self._controller:
            self._controller.disable()
        self._controller = controller
        if controller is None:
            return
        controller.enable()

    def _create(self) -> None:
        super()._create()
        if self._controller is not None:
            self._controller.create()

    def _enable(self) -> None:
        super()._enable()
        if self.controller is not None:
            self.controller.enable()

    def _disable(self) -> None:
        super()._disable()
        if self.controller is not None:
            self.controller.disable()

    def dispatch(self, event) -> DispatchResult:
        for child in reversed(self.children):
            if child.dispatch(event) is not None:
                return EVENT_HANDLED
        if self.controller is not None and self.controller.dispatch(event) is not None:
            return EVENT_HANDLED
        return self.handle(event)

    def update(self, delta_time: float) -> None:
        # logger.debug("Widget.update")
        if self.controller is not None:
            self.controller.update(delta_time)
        for child in self.children:
            child.update(delta_time)
    '''

    def on_added(self) -> None:
        # logger.debug(f"Widget.on_added: {self}")
        # logger.debug(f"Parent: {self.parent}")
        # logger.debug(f"Widget layout: {self.layout}")
        # logger.debug(f"Parent layout: {self.parent.layout}")
        self.parent.layout.add_child(self.layout)
        super().on_added()

    def on_removed(self) -> None:
        if self.parent is not None:
            self.parent.layout.remove_child(self.layout)
        super().on_removed()

    def hit_test(self, x: float, y: float) -> bool:
        position = self.global_position
        size = self.size
        if (
            position.x <= x <= position.x + size.x
            and position.y <= y <= position.y + size.y
        ):
            return True
        return False
