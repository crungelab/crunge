from typing import TYPE_CHECKING, ClassVar

from loguru import logger
import glm

from crunge import box2d

from crunge.engine.chip import Chip

from .constants import PT_DYNAMIC, PT_KINEMATIC, PT_STATIC, GRAVITY
from .geom import Geom
from .material import PhysicsMaterial, DEFAULT_MATERIAL
from .world import PhysicsWorld2D


class Physics(Chip):
    #default_material: PhysicsMaterial = DEFAULT_MATERIAL
    default_material: PhysicsMaterial = None

    BODY_TYPES = {
        PT_DYNAMIC: box2d.BodyType.DYNAMIC_BODY,
        PT_KINEMATIC: box2d.BodyType.KINEMATIC_BODY,
        PT_STATIC: box2d.BodyType.STATIC_BODY,
    }

    def __init__(
        self,
        kind,
        geom: Geom,
        material: PhysicsMaterial = None,
        position: glm.vec2 = None,
        rotation_locked: bool = False,
        gravity_scale: float = 1.0,
    ) -> None:
        super().__init__()
        self.kind = kind
        self.geom = geom
        self.material = self.default_material if material is None else material
        self.offset = glm.vec2() if position is None else glm.vec2(position)
        self.rotation_locked = rotation_locked
        self.gravity_scale = gravity_scale

        self.world = None
        self.body = None
        self.shapes = []
        self._syncing = False

    # -- lifecycle ---------------------------------------------------------

    def _seat(self) -> None:
        super()._seat()
        self.node.transform_changed.connect(self.on_transform_changed)

    def plug(self) -> None:
        super().plug()
        self.world = PhysicsWorld2D.get_current()
        self.create_body()
        self.shapes = self.geom.create_shapes(self)
        logger.debug(f"Created shapes: {self.shapes}")

    def unplug(self) -> None:
        if self.body is not None and self.body.is_valid():
            self.body.destroy()
        self.body = None
        self.shapes = []
        self.world = None
        super().unplug()

    def _unseat(self) -> None:
        self.node.transform_changed.disconnect(self.on_transform_changed)
        super()._unseat()

    def create_body(self):
        node = self.node
        position = node.position + self.offset
        logger.debug(f"Creating body for node: {node}")

        body_def = box2d.BodyDef(
            type=self.BODY_TYPES[self.kind],
            position=box2d.Vec2(position.x, position.y),
            rotation=box2d.make_rot(node.rotation),
            gravity_scale=self.gravity_scale,
        )
        self.body = self.world.create_body(body_def)
        self.body.user_data = node

        if self.rotation_locked:
            self.lock_rotation()

        return self.body

    # -- rotation locks ----------------------------------------------------

    def lock_rotation(self) -> None:
        self.body.set_motion_locks(box2d.MotionLocks(False, False, True))

    def unlock_rotation(self) -> None:
        self.body.set_motion_locks(box2d.MotionLocks(False, False, False))

    # -- sync --------------------------------------------------------------

    def update(self, dt: float) -> None:
        if self.body is None or self.kind is PT_STATIC:
            return
        if not self.body.is_awake:
            return

        body_position = self.body.position
        angle = self.body.angle
        rotated_offset = glm.rotate(self.offset, angle)

        self._syncing = True
        try:
            self.node.position = (
                glm.vec2(body_position.x, body_position.y) - rotated_offset
            )
            self.node.rotation = angle
        finally:
            self._syncing = False

    def on_transform_changed(self) -> None:
        if self._syncing or self.body is None:
            return
        position = self.node.position + glm.rotate(self.offset, self.node.rotation)
        self.body.set_transform(
            box2d.Vec2(position.x, position.y),
            box2d.make_rot(self.node.rotation),
        )
        self.body.wake()

    # -- state -------------------------------------------------------------

    @property
    def velocity(self) -> glm.vec2:
        if self.body is None:
            return glm.vec2()
        lv = self.body.linear_velocity
        return glm.vec2(lv.x, lv.y)

    @velocity.setter
    def velocity(self, value: glm.vec2) -> None:
        if self.body is None:
            return
        self.body.linear_velocity = box2d.Vec2(value.x, value.y)

    @property
    def geom_transform(self) -> box2d.Transform:
        position = -self.offset
        return box2d.Transform(box2d.Vec2(position.x, position.y), box2d.make_rot(0))

    def get_tx_point(self, offset: glm.vec2) -> glm.vec2:
        body_pos = self.body.position
        tx = glm.rotate(glm.mat4(), self.body.angle, glm.vec3(0, 0, 1))
        rel = tx * glm.vec4(offset.x, offset.y, 0, 1)
        return glm.vec2(rel.x + body_pos.x, rel.y + body_pos.y)

    # -- forces ------------------------------------------------------------

    def apply_impulse(self, impulse: glm.vec2) -> None:
        if self.body is None:
            return
        self.body.apply_linear_impulse_to_center(box2d.Vec2(impulse.x, impulse.y), True)

    def apply_force(self, force: glm.vec2) -> None:
        if self.body is None:
            return
        self.body.apply_force_to_center(box2d.Vec2(force.x, force.y), True)


class DynamicPhysics(Physics):
    def __init__(self, geom: Geom, material: PhysicsMaterial = None, **kwargs):
        super().__init__(PT_DYNAMIC, geom, material, **kwargs)


class KinematicPhysics(Physics):
    def __init__(self, geom: Geom, material: PhysicsMaterial = None, **kwargs):
        super().__init__(PT_KINEMATIC, geom, material, **kwargs)

    """
    def update(self, dt: float) -> None:
        super().update(dt)
        if self.body is None:
            return
        if self.grounded or self.climbing or self.mounted or self.jumping:
            return
        lv = self.body.linear_velocity
        self.body.linear_velocity = box2d.Vec2(lv.x, lv.y + GRAVITY[1] * dt)
    """

class StaticPhysics(Physics):
    def __init__(self, geom: Geom, material: PhysicsMaterial = None, **kwargs):
        super().__init__(PT_STATIC, geom, material, **kwargs)