from loguru import logger

import glm

from crunge.engine.d2.node_2d import Node2D

class Thruster(Node2D):
    def __init__(self, body, position: glm.vec2, force: glm.vec2, angular_velocity: float = 0) -> None:
        super().__init__(position)
        self.body = body
        self.active = False
        self.force = force
        self.angular_velocity = angular_velocity

    def on(self):
        self.active = True

    def off(self):
        self.active = False

    def update(self, dt):
        super().update(dt)
        if self.active:
            self.body.apply_force_at_local_point(tuple(self.force), tuple(self.position))
            self.body.angular_velocity = self.angular_velocity
