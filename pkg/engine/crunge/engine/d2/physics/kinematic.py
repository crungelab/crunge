import math

from loguru import logger
import glm
import pymunk

from .constants import *
from . import Physics, PhysicsEngine2D


class KinematicPhysics(Physics):
    def __init__(self):
        super().__init__(PT_KINEMATIC)

    def create_body(self, node, offset=glm.vec2()):
        logger.debug(f"KinematicPhysics.create_body: {node}")
        position = node.position + offset
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.node = node
        #body.position = tuple(node.position)
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body


class CollisionHandler:
    def __init__(self, handler):
        self.handler = handler
        handler.begin = lambda arbiter, space, data: self.begin(arbiter, space, data)
        handler.pre_solve = lambda arbiter, space, data: self.pre_solve(
            arbiter, space, data
        )
        handler.post_solve = lambda arbiter, space, data: self.post_solve(
            arbiter, space, data
        )
        handler.separate = lambda arbiter, space, data: self.separate(
            arbiter, space, data
        )

    def begin(self, arbiter, space, data):
        return True

    def pre_solve(self, arbiter, space, data):
        pass

    def post_solve(self, arbiter, space, data):
        pass

    def separate(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kshape.body.node.grounded = False
        pass


class KinematicStaticHandler(CollisionHandler):
    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kbody.node.grounded = True
        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity = pymunk.Vec2d(velocity[0], 0)
        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        kbody.position += n * penetration
        return True


class KinematicKinematicHandler(CollisionHandler):
    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kbody.node.grounded = True
        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity = pymunk.Vec2d(velocity[0], 0)
        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        kbody.position += n * penetration
        return True


class KinematicDynamicHandler(CollisionHandler):

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        knode = kbody.node
        knode.grounded = True

        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity = pymunk.Vec2d(velocity[0], 0)

        normal = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        body = arbiter.shapes[1].body
        impulse = arbiter.total_impulse
        position = arbiter.contact_point_set.points[0].point_b
        kbody.position += normal * penetration

        impulse = velocity * 0.005
        impulse = pymunk.Vec2d(impulse[0], 0)
        point = position
        body.apply_impulse_at_local_point(impulse, point)
        kbody.velocity = velocity
        return False


class KinematicPhysicsEngine(PhysicsEngine2D):
    def __init__(self, gravity=GRAVITY):
        super().__init__(gravity)

    def _create(self):
        super()._create()
        self.kinematic_static_handler = KinematicStaticHandler(
            self.space.add_collision_handler(PT_KINEMATIC, PT_STATIC)
        )
        self.kinematic_static_handler = KinematicKinematicHandler(
            self.space.add_collision_handler(PT_KINEMATIC, PT_KINEMATIC)
        )
        self.kinematic_dynamic_handler = KinematicDynamicHandler(
            self.space.add_collision_handler(PT_KINEMATIC, PT_DYNAMIC)
        )
