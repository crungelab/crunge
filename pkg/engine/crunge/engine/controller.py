from .base import Base, DispatchResult, EVENT_HANDLED
from .sdl.event_handler import EventHandler


class Controller(EventHandler, Base):
    def __init__(self):
        super().__init__()
        self.delta_time = 0

    def activate(self):
        pass

    def deactivate(self):
        pass

    def dispatch(self, event) -> DispatchResult:
        if super().dispatch(event) is not None:  # Base: descend
            return EVENT_HANDLED
        return self.handle(event)

    def update(self, delta_time: float):
        self.delta_time = delta_time
