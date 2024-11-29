from loguru import logger
import pymunk

from crunge.engine import Base

from ...physics_engine import PhysicsEngine

from . import globe

from .constants import GRAVITY

from .draw_options import DrawOptions


class PhysicsEngine2D(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__()
        logger.debug("PhysicsEngine.__init__")
        globe.physics_engine = self
        self.gravity = gravity
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations

    def update(self, delta_time=1 / 60.0):
        # logger.debug('PhysicsEngine.update')
        self.space.step(delta_time)

    def debug_draw(self, draw_options: DrawOptions):
        self.space.debug_draw(draw_options)
