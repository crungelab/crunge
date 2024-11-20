from loguru import logger
import pymunk

from crunge.engine import Base

from . import globe

from .constants import GRAVITY

from .draw_options import DrawOptions


class PhysicsEngine(Base):
    def __init__(
        self, gravity=GRAVITY, iterations=35, draw_options: DrawOptions = None
    ):
        super().__init__()
        logger.debug("PhysicsEngine.__init__")
        globe.physics_engine = self
        self.gravity = gravity
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.iterations = iterations
        self.draw_options = draw_options

    def update(self, delta_time=1 / 60.0):
        # logger.debug('PhysicsEngine.update')
        self.space.step(delta_time)

    def debug_draw(self, renderer):
        self.space.debug_draw(self.draw_options)
