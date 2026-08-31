from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom, BallGeom, HullGeom


class Obstacle(DynamicEntity2D):
    def __init__(self, position, sprite):
        super().__init__(position, model=sprite)

    @classmethod
    def produce(self, kind, position, sprite):
        node = kinds[kind].produce(position, sprite)
        return node


class Box(Obstacle):
    geom = BoxGeom()

    def __init__(self, position, sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position, sprite):
        return Box(position, sprite)


class Ball(Obstacle):
    geom = BallGeom()

    def __init__(self, position, sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, sprite):
        return Ball(sprite.position, sprite)


class Rock(Obstacle):
    geom = HullGeom()

    def __init__(self, position=(0, 0), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, sprite):
        return Rock(sprite.position, sprite)


kinds = {
    "block": Box,
    "boxCrate": Box,
    "boxCrate_double": Box,
    "Ball": Ball,
    "RockBig1": Rock,
}
