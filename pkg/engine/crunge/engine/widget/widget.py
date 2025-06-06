import math
from typing import Any, Callable

from loguru import logger
import glm

from crunge import yoga

from ..node import Node
from ..part import Part
from ..controller import Controller
from ..renderer import Renderer


class Widget(Node["Widget"]):
    def __init__(self, style: yoga.Style = yoga.Style()) -> None:
        super().__init__()
        self.layout = yoga.Layout()
        self.layout.set_style(style)
        self.layout.set_dirtied_func(self.mark_layout_dirty)
        self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        self._size = glm.ivec2(0, 0)
        self._controller: Controller = None
        self.parts: list[Part] = []
        self.priority = 0
        self.hovered = False
        self.layout_dirty = False

    def _create(self):
        super()._create()

    def mark_layout_dirty(self):
        logger.debug(f"Widget.mark_layout_dirty: {self}")
        self.layout_dirty = True

    def apply_layout(self):
        #logger.debug(f"Widget.apply_layout: {self}")
        if not self.layout_dirty:
            return

        self.on_layout()
        self.layout_dirty = False

        for child in self.children:
            child.apply_layout()

    '''
    def apply_layout(self):
        #logger.debug(f"Widget.apply_layout: {self}")
        if not self.layout.has_new_layout():
            return

        self.on_layout()
        self.layout.mark_layout_seen()

        for child in self.children:
            child.apply_layout()
    '''

    def on_layout(self):
        logger.debug(f"Widget.on_layout: {self}")
        #self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        self._set_size(glm.ivec2(
            self.layout.get_computed_width(), self.layout.get_computed_height()
        ))

    @property
    def style(self) -> yoga.Style:
        return self.layout.get_style()
    
    @style.setter
    def style(self, value: yoga.Style):
        if not isinstance(value, yoga.Style):
            raise TypeError(f"Expected yoga.Style, got {type(value)}")
        self.layout.set_style(value)

    @property
    def position(self) -> glm.ivec2:
        return glm.ivec2(
            self.layout.get_computed_left(), self.layout.get_computed_top()
        )

    @property
    def size(self) -> glm.ivec2:
        return glm.ivec2(
            self.layout.get_computed_width(), self.layout.get_computed_height()
        )

    @property
    def bounds(self) -> yoga.Bounds:
        return self.layout.get_computed_bounds()

    def _set_size(self, value: glm.ivec2) -> bool:
        logger.debug(f"Widget._set_size: {self}, {value}")
        if not isinstance(value, glm.ivec2):
            raise TypeError(f"Expected glm.ivec2, got {type(value)}")
        changed = self._size != value
        self._size = value

        if changed:
            logger.debug(f"Widget size changed: {self}, {self.size}")
            self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
            self.on_size()

        return changed

    @size.setter
    def size(self, value: glm.ivec2):
        self.layout.set_width(value.x)
        self.layout.set_height(value.y)
        #self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        self._set_size(value)

    '''
    @size.setter
    def size(self, value: glm.ivec2):
        if not isinstance(value, glm.ivec2):
            raise TypeError(f"Expected glm.ivec2, got {type(value)}")
        changed = self._size != value
        self._size = value
        self.layout.set_width(value.x)
        self.layout.set_height(value.y)
        self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)

        if changed:
            logger.debug(f"Widget size changed: {self}, {self.size}")
            self.on_size()
    '''

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
        # logger.debug(f"Widget.dispatch: {self}, {self.children}, {event}")
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
            # child.draw(renderer)
            self.draw_child(renderer, child)

    def draw_child(self, renderer: Renderer, child: "Widget"):
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

    def on_attached(self):
        #logger.debug(f"Widget.on_attached: {self}")
        #logger.debug(f"Parent: {self.parent}")
        #logger.debug(f"Widget layout: {self.layout}")
        #logger.debug(f"Parent layout: {self.parent.layout}")
        self.parent.layout.add_child(self.layout)
        super().on_attached()  # Call the parent method to ensure proper attachment behavior

    def hit_test(self, x: float, y: float) -> bool:
        position = self.position
        size = self.size
        if position.x <= x <= position.x + size.x and position.y <= y <= position.y + size.y:
            return True
        return False