from .base import Base


class PhysicsEngine(Base):
    def __init__(self):
        super().__init__()

    def update(self, delta_time=1 / 60.0):
        pass
