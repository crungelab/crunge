from crunge.engine.d2.physics import PhysicsWorld2D


class World(PhysicsWorld2D):
    def __init__(self):
        super().__init__(gravity=(0, 0))
        global world_instance
        world_instance = self

world_instance: World = None
