import glm

from crunge.engine.d2.node_2d import Node2D

from .explosion_vu import ExplosionVu

class Explosion(Node2D):
    def __init__(self, position: glm.vec2, color: glm.vec4 = None) -> None:
        if color is None:
            color = glm.vec4(0.0, 0.0, 1.0, 1.0)
        super().__init__(position, scale = glm.vec2(0.005, 0.005))
        self.color = color

    def _seat(self) -> None:
        self.add(ExplosionVu(self.color))
        super()._seat()

"""
class Explosion(Node2D):
    def __init__(self, position: glm.vec2, color: glm.vec4 = glm.vec4(0.0, 0.0, 1.0, 1.0)) -> None:
        super().__init__(position, scale = glm.vec2(0.005, 0.005), vu=ExplosionVu(color))
"""