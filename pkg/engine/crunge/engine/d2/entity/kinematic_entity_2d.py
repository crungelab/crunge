from loguru import logger
import glm

from ..physics.constants import DEFAULT_MASS, GRAVITY

from .. import physics
from ..physics import geom
from ..physics.kinematic import KinematicState
from .physics_entity_2d import PhysicsEntity2D


class KinematicEntity2D(PhysicsEntity2D):
    def __init__(
        self,
        position=glm.vec2(),
        rotation=0.0,
        scale=glm.vec2(1.0),
        vu=None,
        model=None,
        brain=None,
        physics=physics.KinematicPhysics(),
        geom=geom.HullGeom(),
    ):
        super().__init__(position, rotation, scale, vu, model, brain, physics, geom)
        self.kinematic_state = KinematicState.GROUNDED

    @property
    def grounded(self):
        return self.kinematic_state == KinematicState.GROUNDED

    @property
    def jumping(self):
        return self.kinematic_state == KinematicState.JUMPING

    @property
    def climbing(self):
        return self.kinematic_state == KinematicState.CLIMBING

    @property
    def falling(self):
        return self.kinematic_state == KinematicState.FALLING

    @property
    def mounted(self):
        return self.kinematic_state == KinematicState.MOUNTED

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        if not self.climbing and not self.mounted and not self.jumping:
            self.body.velocity += (0, GRAVITY[1] * delta_time)
