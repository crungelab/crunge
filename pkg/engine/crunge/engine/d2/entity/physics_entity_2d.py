from loguru import logger
import glm

from crunge import box2d

from crunge.engine.signal import Signal

from crunge.engine.d2 import SpriteVu
from ..physics.constants import GRAVITY

from crunge.engine.math import Rect2

from ..physics import (
    Physics,
    StaticPhysics,
    DynamicPhysics,
    KinematicPhysics,
    MotionState,
)
from ..physics.geom import HullGeom
from ..physics.material import PhysicsMaterial, DEFAULT_MATERIAL

from .entity_2d import Entity2D


class PhysicsEntity2D(Entity2D):
    geom = HullGeom()

    default_vu = SpriteVu

    def __init__(
        self,
        position: glm.vec2 = None,
        rotation: float = 0.0,
        scale: glm.vec2 = None,
        model=None,
        brain=None,
        geom=None,
        offset: glm.vec2 = None,
        **physics_kwargs,
    ):
        super().__init__(
            glm.vec2() if position is None else position,
            rotation,
            glm.vec2(1.0) if scale is None else scale,
            model=model,
            brain=brain,
        )
        self.geom = self.geom if geom is None else geom
        self._offset = offset
        self._physics_kwargs = physics_kwargs

        self.physics: Physics | None = None

        self.motion_state = MotionState.GROUNDED
        self.motion_state_changed = Signal[MotionState]()

    def _seat(self) -> None:
        super()._seat()
        self.physics = self.add(
            self.physics_class(
                self.geom,
                position=self._offset,
                **self._physics_kwargs,
            )
        )

    # -- physics forwards --------------------------------------------------

    @property
    def body(self) -> "box2d.Body | None":
        return self.physics.body if self.physics else None

    @property
    def shapes(self) -> list:
        return self.physics.shapes if self.physics else []

    @property
    def velocity(self) -> glm.vec2:
        return self.physics.velocity

    @velocity.setter
    def velocity(self, value: glm.vec2) -> None:
        self.physics.velocity = value

    # -- motion state ------------------------------------------------------

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

    # -- motion state ------------------------------------------------------

    def set_motion_state(self, state: MotionState) -> None:
        if state is self.motion_state:
            return
        self.motion_state = state
        self.motion_state_changed.emit(state)

    # -- geometry ----------------------------------------------------------

    @property
    def geom_transform(self) -> box2d.Transform:
        position = -self.physics.offset
        return box2d.Transform(box2d.Vec2(position.x, position.y), box2d.make_rot(0))

    def get_tx_point(self, offset: glm.vec2) -> glm.vec2:
        body_pos = self.body.position
        tx = glm.rotate(glm.mat4(), self.body.angle, glm.vec3(0, 0, 1))
        rel = tx * glm.vec4(offset.x, offset.y, 0, 1)
        return glm.vec2(rel.x + body_pos.x, rel.y + body_pos.y)


class StaticEntity2D(PhysicsEntity2D):
    physics_class = StaticPhysics


class DynamicEntity2D(PhysicsEntity2D):
    physics_class = DynamicPhysics


class KinematicEntity2D(PhysicsEntity2D):
    physics_class = KinematicPhysics

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        if not self.climbing and not self.mounted and not self.jumping:
            self.body.linear_velocity += box2d.Vec2(0, GRAVITY[1] * delta_time)
