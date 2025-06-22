from typing import TYPE_CHECKING

from loguru import logger

from crunge import yoga

if TYPE_CHECKING:
    from .view import View

from .widget import Widget
from .vu import Vu


class ViewLayer(Widget):
    def __init__(self, name: str, priority: int = 0, vu: Vu = None) -> None:
        style = (
            yoga.StyleBuilder()
            .position_type(yoga.PositionType.ABSOLUTE)
            .size_percent(100, 100)
            .position(yoga.Edge.LEFT, 0)
            .position(yoga.Edge.TOP, 0)
            .build()
        )

        super().__init__(style)

        # This also works
        '''
        self.layout.set_position_type(yoga.PositionType.ABSOLUTE)
        self.layout.set_width_percent(100)
        self.layout.set_height_percent(100)
        self.layout.set_position(yoga.Edge.LEFT, 0)
        self.layout.set_position(yoga.Edge.TOP, 0)
        '''

        self.name = name
        self.priority = priority
        self.view: "View" = None
        self.vu = vu

    def set_view(self, view):
        self.view = view
        return self

    def _create(self):
        super()._create()
        # logger.debug("Layer.create")
        # self.size = self.view.size

    @property
    def window(self):
        return self.view.window
