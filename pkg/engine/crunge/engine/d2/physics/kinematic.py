import math

import pymunk
from pymunk.vec2d import Vec2d

from .constants import *
from . import Physics, PhysicsMeta, PhysicsEngine
from .draw_options import DrawOptions

class KinematicPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_KINEMATIC)

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model, offset=None):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.node = model
        body.position = tuple(model.position)
        body.angle = math.radians(model.angle)
        return body

class CollisionHandler:
    def __init__(self, handler):
        self.handler = handler
        handler.begin = lambda arbiter, space, data: self.begin(arbiter, space, data)
        handler.pre_solve = lambda arbiter, space, data: self.pre_solve(arbiter, space, data)
        handler.post_solve = lambda arbiter, space, data: self.post_solve(arbiter, space, data)
        handler.separate = lambda arbiter, space, data: self.separate(arbiter, space, data)

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
            velocity = Vec2d(velocity[0], 0)
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
            velocity = Vec2d(velocity[0], 0)
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
            velocity = Vec2d(velocity[0], 0)

        normal = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        body = arbiter.shapes[1].body
        impulse = arbiter.total_impulse
        position = arbiter.contact_point_set.points[0].point_b
        kbody.position += normal * penetration

        impulse = velocity * .005
        impulse = Vec2d(impulse[0], 0)
        point = position
        body.apply_impulse_at_local_point(impulse, point)
        kbody.velocity = velocity
        return False

class KinematicPhysicsEngine(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, draw_options: DrawOptions = None):
        super().__init__(gravity, draw_options=draw_options)
    '''
    def _create(self):
        self.kinematic_static_handler = KinematicStaticHandler(self.space.add_collision_handler(PT_KINEMATIC, PT_STATIC))
        self.kinematic_static_handler = KinematicKinematicHandler(self.space.add_collision_handler(PT_KINEMATIC, PT_KINEMATIC))
        self.kinematic_dynamic_handler = KinematicDynamicHandler(self.space.add_collision_handler(PT_KINEMATIC, PT_DYNAMIC))
    '''