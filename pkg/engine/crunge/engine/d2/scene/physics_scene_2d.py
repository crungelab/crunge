from .scene_2d import Scene2D
from ..physics import PhysicsWorld2D


class PhysicsScene2D(Scene2D):
    def __init__(self, physics_engine: PhysicsWorld2D) -> None:
        super().__init__()
        self.physics_engine = physics_engine
        self.physics_engine.make_current()
