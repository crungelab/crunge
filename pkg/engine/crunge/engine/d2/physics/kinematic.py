import math
from enum import Enum

from loguru import logger
import glm
import pymunk

from .constants import *
from . import Physics, PhysicsEngine2D

class KinematicState(Enum):
    GROUNDED = 0
    JUMPING = 1
    CLIMBING = 2
    FALLING = 3
    MOUNTED = 4


class KinematicPhysics(Physics):
    def __init__(self, position=glm.vec2()):
        super().__init__(PT_KINEMATIC, position)

    def create_body(self, node):
        logger.debug(f"KinematicPhysics.create_body: {node}")
        position = node.position + self.position
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.node = node
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body


class CollisionHandler:
    def __init__(self, space: pymunk.Space, collision_type_a: int, collision_type_b: int):
        space.on_collision(
            collision_type_a, collision_type_b, begin=self.begin, pre_solve=self.pre_solve,
            post_solve=self.post_solve, separate=self.separate
        )

    def begin(self, arbiter, space, data):
        return True

    def pre_solve(self, arbiter, space, data):
        pass

    def post_solve(self, arbiter, space, data):
        pass

    def separate(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        #kshape.body.node.grounded = False
        kshape.body.node.kinematic_state = KinematicState.FALLING


class KinematicStaticHandler(CollisionHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__(space, PT_KINEMATIC, PT_STATIC)

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kbody.node.kinematic_state = KinematicState.GROUNDED
        
        velocity = kbody.velocity
        
        if velocity[1] < 0:
            velocity = pymunk.Vec2d(velocity[0], 0)
            
        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        kbody.position += n * penetration
        return True


class KinematicKinematicHandler(CollisionHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__(space, PT_KINEMATIC, PT_KINEMATIC)

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        #kbody.node.grounded = True
        kbody.node.kinematic_state = KinematicState.GROUNDED
        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity = pymunk.Vec2d(velocity[0], 0)
        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        kbody.position += n * penetration
        return True


class KinematicDynamicHandler(CollisionHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__(space, PT_KINEMATIC, PT_DYNAMIC)

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        knode = kbody.node
        knode.kinematic_state = KinematicState.GROUNDED

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
        self.kinematic_static_handler = KinematicStaticHandler(self.space)
        self.kinematic_static_handler = KinematicKinematicHandler(self.space)
        self.kinematic_dynamic_handler = KinematicDynamicHandler(self.space)
