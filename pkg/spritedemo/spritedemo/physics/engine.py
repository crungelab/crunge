from loguru import logger
import pymunk

from .. import globals

from ..constants import *

class PhysicsEngine:
    def __init__(self, gravity=GRAVITY, iterations=35):
        logger.debug('PhysicsEngine.__init__')
        globals.physics_engine = self
        self.gravity = gravity
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations
    
    def create(self):
        pass

    def update(self, delta_time=1/60.0):
        #logger.debug('PhysicsEngine.update')
        self.space.step(delta_time)
