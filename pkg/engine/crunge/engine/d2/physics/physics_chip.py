from enum import Flag, auto

import glm

from crunge import box2d

from crunge.engine.chip import Chip
from crunge.engine.d2.physics.geom import Geom


class BodyType(Flag):
    STATIC = auto()
    KINEMATIC = auto()
    DYNAMIC = auto()


class PhysicsChip(Chip):
    """Owns a Box2D body on behalf of its node. Geom describes the shape;
    this chip owns the handle, the world registration, and transform sync."""

    def __init__(
        self,
        geom: Geom,
        body_type: BodyType = BodyType.DYNAMIC,
        fixed_rotation: bool = False,
        gravity_scale: float = 1.0,
    ) -> None:
        super().__init__()
        self.geom = geom
        self.body_type = body_type
        self.fixed_rotation = fixed_rotation
        self.gravity_scale = gravity_scale

        self.body = None
        self.shapes = []
        self.world = None

        self._syncing = False

    # -- lifecycle ---------------------------------------------------------

    def _seat(self) -> None:
        super()._seat()
        self.node.transform_changed.connect(self.on_transform_changed)

    def plug(self) -> None:
        super().plug()
        self.world = self.node.scene.world  # ASSUMPTION: scene exposes .world
        self.mark_dirty(Dirt.BODY)

    def unplug(self) -> None:
        self._destroy_body()
        self.world = None
        super().unplug()

    def _unseat(self) -> None:
        self.node.transform_changed.disconnect(self.on_transform_changed)
        super()._unseat()

    # -- deferred creation -------------------------------------------------

    def _flush_body(self) -> None:
        if self.world is None:
            return  # retry next flush, same as _flush_gpu

        body_def = box2d.default_body_def()
        body_def.type = self._native_body_type()
        body_def.position = box2d.Vec2(*self.node.position)
        body_def.rotation = box2d.make_rot(self.node.angle)  # ASSUMPTION: b2MakeRot
        body_def.fixed_rotation = self.fixed_rotation
        body_def.gravity_scale = self.gravity_scale
        body_def.user_data = self  # ASSUMPTION: PyHolder-backed

        self.body = self.world.create_body(body_def)
        self.shapes = self.geom.attach(self.body)  # ASSUMPTION: Geom builds shapes
        self.clear_dirty(Dirt.BODY)

    def _destroy_body(self) -> None:
        if self.body is None:
            return
        self.body.destroy()
        self.body = None
        self.shapes = []

    def _native_body_type(self):
        return {
            BodyType.STATIC: box2d.BodyType.STATIC,
            BodyType.KINEMATIC: box2d.BodyType.KINEMATIC,
            BodyType.DYNAMIC: box2d.BodyType.DYNAMIC,
        }[self.body_type]

    # -- sync --------------------------------------------------------------

    def update(self, dt: float) -> None:
        if self.body is None or self.body_type is BodyType.STATIC:
            return
        if not self.body.is_awake:
            return

        position = self.body.position
        self._syncing = True
        try:
            self.node.position = glm.vec2(position.x, position.y)
            self.node.angle = self.body.rotation_angle  # ASSUMPTION: b2Rot_GetAngle
        finally:
            self._syncing = False

    def on_transform_changed(self) -> None:
        if self._syncing or self.body is None:
            return
        self.body.set_transform(
            box2d.Vec2(*self.node.position),
            box2d.make_rot(self.node.angle),
        )
        self.body.wake()

    # -- forces ------------------------------------------------------------

    def apply_impulse(self, impulse: glm.vec2) -> None:
        if self.body is None:
            return
        self.body.apply_linear_impulse_to_center(
            box2d.Vec2(impulse.x, impulse.y), True
        )