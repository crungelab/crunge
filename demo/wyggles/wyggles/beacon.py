import glm

from .game_entity import GameEntity

class Beacon():
    def __init__(self, node: GameEntity, type: str):
        self.node: GameEntity = node
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
