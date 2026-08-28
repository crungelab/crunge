from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.math import Rect2

from crunge.engine.d2.entity import PhysicsEntity2D, DynamicEntity2D
from crunge.engine.d2.physics import HullGeom
from crunge.engine.d2.physics import MotionState

from crunge.engine.d2.sprite import Sprite, SpriteVu

from ..constants import *
from .. import globe

from ..character.controller import DynamicCharacterController

#PLAYER_MASS = 70
PLAYER_MASS = 20


class DynamicCharacter(DynamicEntity2D):
    model: Sprite
    def __init__(self, position=glm.vec2(), model=None, brain=None):
        super().__init__(position, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS
        self.mass_data: b2.MassData = None

    def _create(self):
        super()._create()
        self.lock_rotation()

    def create_shapes(self, clip: Rect2 = None):
        x = -(self.width / 2)
        y = 0
        width = self.width
        height = self.height / 2
        clip = Rect2(x, y, width, height)
        logger.debug(f"clip: {clip}")
        return super().create_shapes(clip=clip)

    def lock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, True))

    def unlock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, False))

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        logger.debug(f"mounting: node={node}, point={point}")
        self.motion_state = MotionState.MOUNTED
        self.unlock_rotation()
        logger.debug(f"mounting at {self.position}")

        self.mass_data = self.body.mass_data
        mass_data = self.body.mass_data

        logger.debug(f"mass data: mass={mass_data.mass}, center={mass_data.center}, inertia={mass_data.rotational_inertia}")
        mass_data.mass = 0.1
        com = mass_data.center
        mass_data.center = b2.Vec2(com.x, com.y - 1)
        self.body.mass_data = mass_data

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        logger.debug(f"dismounting from {node}")
        self.motion_state = MotionState.FALLING
        self.lock_rotation()
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        self.rotation = 0

        logger.debug(f"mass data: mass={self.mass_data.mass}, center={self.mass_data.center}, inertia={self.mass_data.rotational_inertia}")
        self.body.mass_data = self.mass_data

        logger.debug(f"applied mass data: mass={self.body.mass_data.mass}, center={self.body.mass_data.center}, inertia={self.body.mass_data.rotational_inertia}")
        self.body.linear_velocity = b2.Vec2(0, 0)
        #self.body.transform = b2.Transform(p=b2.Vec2(*self.position))
        self.body.set_transform(b2.Vec2(*self.position), b2.make_rot(0))
        #self.body.angle = 0
        #self.body.angular_velocity = 0 # Stop any residual spin
        self.lock_rotation() # Re-lock rotation
        globe.app.pop_avatar()

    def control(self):
        return DynamicCharacterController(self)
