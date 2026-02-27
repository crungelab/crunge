import math

from loguru import logger
import glm
from crunge import box2d

from crunge.engine.d2 import Vu2D

from crunge.engine.math import Rect2

from ..physics import globe
from ..physics.constants import DEFAULT_MASS, GRAVITY
from ..physics import StaticPhysics, DynamicPhysics, GroupPhysics
from ..physics.physics import MotionState
from ..physics.geom import HullGeom, GroupGeom

from .entity_2d import Entity2D


class PhysicsEntity2D(Entity2D):
    def __init__(
        self,
        position=glm.vec2(),
        rotation=0.0,
        scale=glm.vec2(1.0),
        vu: Vu2D = None,
        model=None,
        brain=None,
        physics=StaticPhysics(),
        geom=HullGeom(),
    ):
        super().__init__(position, rotation, scale, vu, model, brain)
        self.body: box2d.Body | None = None
        self.shapes: list[box2d.Shape] = []
        self._physics = physics
        self.geom = geom
        self.mass = DEFAULT_MASS
        self.motion_state = MotionState.GROUNDED

    @property
    def grounded(self):
        return self.motion_state == MotionState.GROUNDED

    @property
    def jumping(self):
        return self.motion_state == MotionState.JUMPING

    @property
    def climbing(self):
        return self.motion_state == MotionState.CLIMBING

    @property
    def falling(self):
        return self.motion_state == MotionState.FALLING

    @property
    def mounted(self):
        return self.motion_state == MotionState.MOUNTED

    @property
    def velocity(self):
        return self.body.velocity

    @velocity.setter
    def velocity(self, value: glm.vec2):
        self.body.velocity = value

    @property
    def physics(self):
        return self._physics

    @physics.setter
    def physics(self, physics):
        if self._physics:
            self._physics = physics
            self.remove_shapes()
            self.body = self.create_body()
            self.shapes = self.create_shapes()
            self.add_shapes()
        else:
            self._physics = physics

    def _create(self):
        super()._create()
        self.body = self.create_body()
        self.shapes = self.create_shapes()
        self.add_shapes()

    def destroy(self):
        self.remove_shapes()
        super().destroy()

    def update(self, delta_time: float):
        if self.body:
            body_position = glm.vec2(self.body.position.x, self.body.position.y)
            rotated_offset = glm.rotate(self.physics.position, self.body.angle)
            self.position = body_position - rotated_offset
            self.angle = self.body.angle
            # logger.debug(f"position: {self.position}")
            # logger.debug(f"angle: {self.angle}")
        super().update(delta_time)

    def create_body(self):
        return self.physics.create_body(self)

    def create_shapes(self, clip: Rect2 = None):
        return self.geom.create_shapes(self, clip=clip)

    def add_shapes(self):
        for shape in self.shapes:
            self.add_shape(shape)

    def add_shape(self, shape):
        # logger.debug(f"shape: {shape}")
        # shape.collision_type = self.physics.kind
        # logger.debug(f"shape.collision_type: {shape.collision_type}")
        #globe.physics_engine.space.add(self.body, shape)
        pass

    def remove_shapes(self):
        for shape in self.shapes:
            globe.physics_engine.space.remove(self.body, shape)

    def get_tx_point(self, offset: glm.vec2):
        body_pos = self.body.position
        angle = self.body.angle
        tx = glm.mat4()
        tx = glm.rotate(tx, angle, glm.vec3(0, 0, 1))
        rel_pos = tx * glm.vec4(offset.x, offset.y, 0, 1)
        pos = rel_pos + glm.vec4(body_pos.x, body_pos.y, 0, 1)
        return glm.vec2(pos)

    @property
    def geom_transform(self):
        a = self.scale.x
        d = self.scale.y
        position = -self.physics.position
        tx = position.x
        ty = position.y
        #t = box2d.Transform(a=a, d=d, tx=tx, ty=ty)
        t = box2d.Transform(box2d.Vec2(tx, ty), box2d.Rot(angle=0))
        # logger.debug(f"t: {t}")
        return t


class PhysicsGroup2D(PhysicsEntity2D):
    id_counter = 1

    def __init__(
        self, position=glm.vec2(), physics=GroupPhysics(), geom=GroupGeom()
    ):
        super().__init__(position, physics=physics, geom=geom)
        self.id_counter += 1
        self.id = self.id_counter
        self.nodes: list[PhysicsEntity2D] = []

    def add_node(self, node: PhysicsEntity2D):
        node.group = self
        self.nodes.append(node)
        return node

    def _create(self):
        super()._create()
        for node in self.nodes:
            node.gid = self.id
            self.layer.attach(node)

    def update(self, delta_time: float):
        points = [node.position for node in self.nodes]
        if points:
            centroid = glm.vec2(
                sum(point.x for point in points) / len(points),
                sum(point.y for point in points) / len(points),
            )
        else:
            centroid = glm.vec2(0, 0)  # Default centroid if the list is empty
        self.position = centroid
        return super().update(delta_time)


class StaticEntity2D(PhysicsEntity2D):
    def __init__(
        self,
        position=glm.vec2(),
        rotation=0.0,
        scale=glm.vec2(1.0),
        vu=None,
        model=None,
        brain=None,
        physics=StaticPhysics(),
        geom=HullGeom(),
    ):
        super().__init__(position, rotation, scale, vu, model, brain, physics, geom)


class DynamicEntity2D(PhysicsEntity2D):
    def __init__(
        self,
        position=glm.vec2(),
        rotation=0.0,
        scale=glm.vec2(1.0),
        vu=None,
        model=None,
        brain=None,
        physics=DynamicPhysics(),
        geom=HullGeom(),
    ):
        super().__init__(position, rotation, scale, vu, model, brain, physics, geom)
