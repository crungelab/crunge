import glm

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import Sprite


class Pole(Node2D):
    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, model=sprite)
        self.collected = False


class Flag(Node2D):
    def __init__(self, position: glm.vec2, sprite: Sprite):
        super().__init__(position, model=sprite)
        self.collected = False

    @classmethod
    def produce(self, kind, position: glm.vec2, sprite: Sprite):
        node = kinds[kind].produce(position, sprite)
        return node

    def collect(self):
        return True

class FlagGreen(Flag):
    @classmethod
    def produce(self, position: glm.vec2, sprite: Sprite):
        return FlagGreen(position, sprite)


class FlagYellow(Flag):
    @classmethod
    def produce(self, position: glm.vec2, sprite: Sprite):
        return FlagYellow(position, sprite)


class FlagRed(Flag):
    @classmethod
    def produce(self, position: glm.vec2, sprite: Sprite):
        return FlagRed(position, sprite)


kinds = {
    "Pole": Pole,
    "FlagGreen": FlagGreen,
    "FlagYellow": FlagYellow,
    "FlagRed": FlagRed,
}
