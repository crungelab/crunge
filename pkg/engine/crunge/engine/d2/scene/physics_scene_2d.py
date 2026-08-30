from .scene_2d import Scene2D
from ..physics import PhysicsWorld2D


class PhysicsScene2D(Scene2D):
    def __init__(self, world: PhysicsWorld2D) -> None:
        super().__init__()
        self.world = world
        self.world.make_current()
