from typing import TYPE_CHECKING

from loguru import logger

from crunge.core.chip import Chip
from crunge.core.dispatch import DispatchResult, EVENT_HANDLED
from .event.event_handler import EventHandler

if TYPE_CHECKING:
    from .node import Node


class Brain[T_Node: "Node"](EventHandler, Chip[T_Node]):
    def __init__(self):
        super().__init__()
        self.delta_time = 0

    def dispatch(self, input) -> DispatchResult:
        # logger.debug(f"class:{self.__class__.__name__}, Dispatching input: {input}")
        return super().dispatch(input) or self.handle(input)

    def update(self, delta_time: float):
        self.delta_time = delta_time
