from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.math import Rect2

from crunge.engine.d2.entity import PhysicsEntity2D, DynamicEntity2D
from crunge.engine.d2.physics import HullGeom
from crunge.engine.d2.physics import MotionState

from crunge.engine.d2.sprite import Sprite, SpriteVu

from ... import globe

from .controller import DynamicCharacterController

PLAYER_MASS = 20


class DynamicCharacter(DynamicEntity2D):
    model: Sprite
    geom_class = HullGeom

    def __init__(self, position=None, model=None, brain=None):
        super().__init__(position, model=model, brain=brain)
        self.mass = PLAYER_MASS
        self.mass_data: b2.MassData = None

    def _create(self):
        super()._create()
        self.lock_rotation()

    def lock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, True))

    def unlock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, False))

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.MOUNTED
        self.unlock_rotation()

        self.mass_data = self.body.mass_data
        mass_data = self.body.mass_data
        mass_data.mass = 0.1
        com = mass_data.center
        mass_data.center = b2.Vec2(com.x, com.y - 1)
        self.body.mass_data = mass_data

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.FALLING
        self.lock_rotation()
        self.position = node.get_tx_point(
            glm.vec2(point.x, point.y + self.height / 2)
        )
        self.rotation = 0

        self.body.mass_data = self.mass_data
        self.body.linear_velocity = b2.Vec2(0, 0)
        self.body.set_transform(b2.Vec2(*self.position), b2.make_rot(0))
        self.lock_rotation()
        globe.app.pop_avatar()

    def control(self):
        return DynamicCharacterController(self)