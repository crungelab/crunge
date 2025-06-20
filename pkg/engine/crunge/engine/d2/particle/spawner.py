import math
import random

from ...color import Color
from ...uniforms import cast_tuple4f
from ..uniforms_2d import Vec2

class Spawner:
    def __call__(self, particle):
        raise NotImplementedError

class RadialBurstSpawner(Spawner):
    def __init__(self, color: Color = (1.0, 0.5, 0.0, 1.0), lifespan: float = 100.0):
        super().__init__()
        self.color = color
        self.lifespan = lifespan

    def __call__(self, particle):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5)
        particle.position = Vec2(0.0, 0.0)
        particle.velocity = Vec2(math.cos(angle) * speed, math.sin(angle) * speed)
        particle.color = cast_tuple4f(self.color)
        particle.age = 0.0
        particle.lifespan = self.lifespan
