from .base import Base
from .dispatcher import Dispatcher

class Controller(Dispatcher):
    def __init__(self):
        super().__init__()
        self.delta_time = 0

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self, delta_time: float):
        self.delta_time = delta_time
