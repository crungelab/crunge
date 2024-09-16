import glm

from crunge.engine.d2.node_2d import Node2D

from .explosion_vu import ExplosionVu

class Explosion(Node2D):
    def __init__(self, position: glm.vec2, size: glm.vec2, color: glm.vec4 = glm.vec4(0.0, 0.0, 1.0, 1.0)) -> None:
        super().__init__(position, size, vu=ExplosionVu(color))
