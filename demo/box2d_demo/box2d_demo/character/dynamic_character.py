from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.math import Rect2

from ..entity import PhysicsEntity2D, DynamicEntity2D
from ..physics import HullGeom
from ..physics.physics import MotionState

from crunge.engine.d2.sprite import Sprite, SpriteVu

from ..constants import *
from .. import globe

from ..character.controller import DynamicCharacterController

PLAYER_MASS = 70


class DynamicCharacter(DynamicEntity2D):
    model: Sprite
    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS

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

    '''
    def create_shapes(self, clip: Rect2 = None):
        x = 0
        y = self.height / 4
        #y = -(self.y + self.height / 4)
        width = self.width
        height = self.height
        clip = Rect2(x, y, width, height)
        logger.debug(f"clip: {clip}")
        return super().create_shapes(clip=clip)
        #return super().create_shapes()
    '''

    '''
    def create_shapes(self, clip: Rect2 = None):
        #clip = Rect2(self.x, self.y + self.height / 2, self.width, self.height / 2)
        model = self.model
        rect = model.rect
        x = rect.x - rect.width / 2
        y = -(rect.y + rect.height / 4)
        #y = rect.y - rect.height / 2
        width = rect.width
        height = rect.height / 2
        clip = Rect2(x, y, width, height)
        logger.debug(f"clip: {clip}")
        return super().create_shapes(clip=clip)
    '''

    def lock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, True))

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.MOUNTED
        #self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2 + 4))
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2 + 0.125))
        logger.debug(f"mounting at {self.position}")
        self.body.position = tuple(self.position)
        self.angle = node.angle
        # logger.debug('on_mount')
        logger.debug(f"shapes: {self.shapes}")

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.FALLING
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        self.angle = 0
        self.body.velocity = (0, 0)
        self.body.angle = 0
        self.body.angular_velocity = 0 # Stop any residual spin
        self.lock_rotation() # Re-lock rotation
        globe.screen.pop_avatar()

    def control(self):
        return DynamicCharacterController(self)
