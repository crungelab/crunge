import glm

from .sprite_node import SpriteNode

class Beacon():
    def __init__(self, node: SpriteNode, type: str):
        self.node: SpriteNode = node
        self.type: str = type

    @property
    def position(self) -> glm.vec2:
        return self.node.position

    @position.setter
    def position(self, val: glm.vec2):
        self.node.position = val

    @property
    def x(self) -> float:
        return self.node.position.x

    @property
    def y(self) -> float:
        return self.node.position.y
