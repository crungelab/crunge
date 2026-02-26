import math

from loguru import logger
import glm
from crunge import box2d

from .constants import *
from . import Physics, PhysicsWorld2D
#from .collision import CollisionHandler
from .physics import MotionState


class KinematicPhysics(Physics):
    def __init__(self, position=glm.vec2()):
        super().__init__(PT_KINEMATIC, position)

    def create_body(self, node):
        logger.debug(f"KinematicPhysics.create_body: {node}")
        position = node.position + self.position
        body = box2d.Body(body_type=box2d.Body.KINEMATIC)
        body.node = node
        body.position = box2d.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body

"""
class KinematicCollisionHandler(CollisionHandler):
    def separate(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kshape.body.node.motion_state = MotionState.FALLING


class KinematicStaticHandler(CollisionHandler):
    def __init__(self, space: box2d.World):
        super().__init__(space, PT_KINEMATIC, PT_STATIC)

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kbody.node.motion_state = MotionState.GROUNDED

        velocity = kbody.velocity

        if velocity[1] < 0:
            velocity = box2d.Vec2d(velocity[0], 0)

        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        kbody.position += n * penetration
        return True


class KinematicKinematicHandler(KinematicCollisionHandler):
    def __init__(self, space: box2d.World):
        super().__init__(space, PT_KINEMATIC, PT_KINEMATIC)

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kbody.node.motion_state = MotionState.GROUNDED
        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity = box2d.Vec2d(velocity[0], 0)
        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        kbody.position += n * penetration
        return True


class KinematicDynamicHandler(KinematicCollisionHandler):
    def __init__(self, space: box2d.World):
        super().__init__(space, PT_KINEMATIC, PT_DYNAMIC)

    # def pre_solve(self, arbiter, space, data):
    def post_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        knode = kbody.node
        knode.motion_state = MotionState.GROUNDED

        velocity = kbody.velocity

        if velocity[1] < 0:
            velocity = box2d.Vec2d(velocity[0], 0)

        normal = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        body = arbiter.shapes[1].body

        if body.is_sleeping:
            body.activate()

        impulse = arbiter.total_impulse
        position = arbiter.contact_point_set.points[0].point_b
        kbody.position += normal * penetration

        impulse = velocity * 0.005
        impulse = box2d.Vec2d(impulse[0], 0)
        point = position
        body.apply_impulse_at_local_point(impulse, point)
        kbody.velocity = velocity
        return False
"""

class KinematicPhysicsEngine(PhysicsWorld2D):
    def __init__(self, gravity=GRAVITY):
        super().__init__(gravity)

    def _create(self):
        super()._create()
        #self.kinematic_static_handler = KinematicStaticHandler(self.space)
        #self.kinematic_kinematic_handler = KinematicKinematicHandler(self.space)
        #self.kinematic_dynamic_handler = KinematicDynamicHandler(self.space)
