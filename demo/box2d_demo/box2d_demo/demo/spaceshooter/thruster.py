from loguru import logger

import glm

from crunge import box2d as b2

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
            body = self.body
            world_force = body.get_world_vector(b2.Vec2(*self.force))
            world_point = body.get_world_point(b2.Vec2(*self.position))
            body.apply_force(world_force, world_point, True)
            #force = b2.Vec2(*self.force * 10)
            #body.apply_force_to_center(force, True)
            body.set_angular_velocity(self.angular_velocity)

            #logger.debug(f"body mass: {body.get_mass()}")
            #logger.debug(f"body type: {body.get_type()}")
