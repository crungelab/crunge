from typing import TYPE_CHECKING

from loguru import logger

from crunge import yoga

from ..widget import Widget
from ..vu import Vu

if TYPE_CHECKING:
    from ..window import Window
    from ..display import Display


class Overlay(Widget):
    def __init__(self, name: str, priority: int = 0, style: yoga.Style = None) -> None:
        if style is None:
            style = (
                yoga.StyleBuilder()
                .position_type(yoga.PositionType.ABSOLUTE)
                .size_percent(100, 100)
                .position(yoga.Edge.LEFT, 0)
                .position(yoga.Edge.TOP, 0)
                .build()
            )
        '''
        style = (
            yoga.StyleBuilder()
            .position_type(yoga.PositionType.ABSOLUTE)
            .size_percent(100, 100)
            .position(yoga.Edge.LEFT, 0)
            .position(yoga.Edge.TOP, 0)
            .build()
        )
        '''

        super().__init__(style, priority=priority)

        # This also works
        """
        self.layout.set_position_type(yoga.PositionType.ABSOLUTE)
        self.layout.set_width_percent(100)
        self.layout.set_height_percent(100)
        self.layout.set_position(yoga.Edge.LEFT, 0)
        self.layout.set_position(yoga.Edge.TOP, 0)
        """

        self.name = name
        self.window: "Window" = None
        self.display: "Display" = None
