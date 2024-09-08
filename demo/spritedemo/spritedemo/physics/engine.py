from loguru import logger
import pymunk

from crunge.engine import Base

from .. import globals

from ..constants import *

class PhysicsEngine(Base):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
        logger.debug('PhysicsEngine.__init__')
        globals.physics_engine = self
        self.gravity = gravity
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations

    def update(self, delta_time=1/60.0):
        #logger.debug('PhysicsEngine.update')
        self.space.step(delta_time)
