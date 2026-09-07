from typing import TYPE_CHECKING

from loguru import logger

from .chip import Chip
from .dispatch import DispatchResult, EVENT_HANDLED
from .sdl.event_handler import EventHandler

if TYPE_CHECKING:
    from .node import Node

class Controller[T_Node: "Node"](EventHandler, Chip[T_Node]):
#class Controller(EventHandler, Chip):
    def __init__(self):
        super().__init__()
        self.delta_time = 0

    def activate(self):
        pass

    def deactivate(self):
        pass

    def dispatch(self, event) -> DispatchResult:
        #logger.debug(f"class:{self.__class__.__name__}, Dispatching event: {event}")
        return super().dispatch(event) or self.handle(event)

    def update(self, delta_time: float):
        self.delta_time = delta_time
