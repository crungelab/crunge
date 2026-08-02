import math
import random

import glm


from crunge.engine.d2.node_2d import Node2D


class Coin(Node2D):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position, sprite):
        kind = sprite.properties["class"]
        node = kinds[kind].produce(position, sprite)
        # print(model)
        # print(vars(sprite))
        # print(kind)
        # print(sprite.points)
        return node


class Gem(Coin):
    def __init__(self, position=glm.vec2(), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position=glm.vec2(), sprite=None):
        return Gem(position, sprite)


kinds = {"coin": Gem}
