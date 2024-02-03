from loguru import logger

import math
import glm
import pymunk

from .constants import *
from . import globals
from . import physics
from . import geom
from .node_2d import Node2D
from .vu_2d import Vu2D


class Model2D(Node2D):
    def __init__(self, position=glm.vec2(), vu: Vu2D = None, brain=None):
        super().__init__(position, vu)
        self.layer = None
        self.brain = brain
        self.radius = 0

        """
        if vu:
            self.width = sprite.width * TILE_SCALING
            self.height = sprite.height * TILE_SCALING
            self.radius = self.width / 2
            self.angle = sprite.angle
        """

    """
    def create(self, layer):
        self.layer = layer
        self.do_create()
    """

    def create(self):
        self.do_create()
        self.post_create()

    def do_create(self):
        pass

    def post_create(self):
        pass

    def do_create(self):
        pass
        """
        if self.sprite and len(self.sprite.sprite_lists) == 0:
            self.layer.add_sprite(self.sprite)
        """

    def update(self, delta_time: float):
        super().update(delta_time)
        self.update_brain(delta_time)
        self.update_physics(delta_time)
        # self.update_sprite(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)

    def update_physics(self, delta_time):
        pass


class Group2D(Model2D):
    id_counter = 1

    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def do_create(self):
        super().do_create()
        for model in self.models:
            model.gid = self.id
            self.layer.add_model(model)


class PhysicsModel2D(Model2D):
    def __init__(
        self,
        position=glm.vec2(),
        vu=None,
        brain=None,
        physics=physics.StaticPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, vu, brain)
        self.body = None
        self.body_offset = None
        self.shapes = []
        self._physics = physics()
        self.geom = geom()
        self.mass = DEFAULT_MASS
        self.geom_transform = self.create_geom_transform()

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

    def do_create(self):
        super().do_create()
        self.body = self.create_body()
        self.shapes = self.create_shapes()

    def post_create(self):
        self.add_shapes()

    def update_physics(self, delta_time=1 / 60):
        if self.body:
            self.position = glm.vec2(self.body.position.x, self.body.position.y)
            self.angle = math.degrees(self.body.angle)
            #logger.debug(f"position: {self.position}")
            #logger.debug(f"angle: {self.angle}")

    def create_body(self, offset=None):
        return self.physics.create_body(self, offset)

    def create_shapes(self, transform=None):
        return self.geom.create_shapes(self)

    def add_shapes(self):
        for shape in self.shapes:
            logger.debug(f"shape: {shape}")
            shape.collision_type = self.physics.kind
            logger.debug(f"shape.collision_type: {shape.collision_type}")
            globals.physics_engine.space.add(self.body, shape)

    def remove_shapes(self):
        for shape in self.shapes:
            globals.physics_engine.space.remove(self.body, shape)

    def get_tx_point(self, offset):
        body_pos = self.body.position
        angle = self.body.angle
        tx = glm.mat4()
        tx = glm.rotate(tx, angle, glm.vec3(0, 0, 1))
        rel_pos = tx * glm.vec4(offset[0], offset[1], 0, 1)
        pos = rel_pos + glm.vec4(body_pos[0], body_pos[1], 0, 1)
        return (pos[0], pos[1])

    def create_geom_transform(self):
        vu = self.vu
        if not vu:
            return None
        # a = sprite.width / sprite.texture.width
        a = self.width / vu.width
        # d = sprite.height / sprite.texture.height
        d = self.height / vu.height
        t = pymunk.Transform(a=a, d=d)
        return t


class PhysicsGroup2D(PhysicsModel2D):
    id_counter = 1

    def __init__(
        self, position=glm.vec2(), physics=physics.GroupPhysics, geom=geom.GroupGeom
    ):
        super().__init__(position, physics=physics, geom=geom)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def do_create(self):
        super().do_create()
        for model in self.models:
            model.gid = self.id
            # model.physics = self.physics
            self.layer.add_model(model)

    def post_create(self):
        pass


class StaticModel2D(PhysicsModel2D):
    def __init__(
        self,
        position=glm.vec2(),
        vu=None,
        brain=None,
        physics=physics.StaticPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, vu, brain, physics, geom)


class DynamicModel2D(PhysicsModel2D):
    def __init__(
        self,
        position=glm.vec2(),
        vu=None,
        brain=None,
        physics=physics.DynamicPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, vu, brain, physics, geom)


class KinematicModel(PhysicsModel2D):
    def __init__(
        self,
        position=glm.vec2(),
        vu=None,
        brain=None,
        physics=physics.KinematicPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, vu, brain, physics, geom)

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        if not self.laddered:
            self.body.velocity += (0, int(GRAVITY[1] * delta_time))

    def create_body(self):
        sprite = self.sprite
        position = sprite.position
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = DEFAULT_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        # moment = pymunk.moment_for_poly(mass, points)
        self.body = body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)
        body.position = position
        body.model = self
        return body


class ModelFactory:
    def __init__(self, layer):
        self.layer = layer
